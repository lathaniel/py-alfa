import sys, os, json, glob

class Model:
  '''General class for an MG-ALFA model
  
  Attributes:
    valdate (str): date-like object representing the Valuation Date of the model
    asset_input: instance of :class: AIA
    liability_input: instance of :class: AIL
  
  Examples:
    Create an instance of a model::

      x = Model('P:/2020/083120')
      # Output

  '''
  def __init__(self, full_path_to_model_file, valdate = None):
    # ensure the provided path exists
    if os.path.exists(full_path_to_model_file):
      # See if a file or directory was provided.
      if full_path_to_model_file.split('.')==[full_path_to_model_file]:
        # User provided a directory, so look for an ALFA model within
        files = glob.glob(os.path.join(full_path_to_model_file, '*.ain2'))
        if len(files)==1:
          self.__model_file = files[0]
        elif len(files)==0:
          raise FileNotFoundError("Could not find an AFLA model (*.ain2) within '%s'"%full_path_to_model_file)
          self.__model_file = ''
        else:
          # More than one model exists in the provided directory
          raise ValueError("More than one ALFA model exists within '%s'. Please specify which to use by providing its full filename when creating a Model instance.")
          self.__model_file = ''
      else:
        # User provided a file. See if it is an ALFA model
        if not full_path_to_model_file.split('.')[-1].lower()=='ain2':
          raise ValueError("'%s' does not appear to be an ALFA model. Proceed with caution and double check what you have entered."%full_path_to_model_file)
        self.__model_file = full_path_to_model_file
    else:
      print("Could not initialize model at '%s'\nMake sure you entered the path correctly and that it can be accessed by you."%full_path_to_model_file)
      raise FileNotFoundError("Could not initialize model at '%s'\nMake sure you entered the path correctly and that it can be accessed by you."%full_path_to_model_file)
    
    # Give the model a valuation date, even though it won't really be useful in practice
  
  def _get_tableFiles(self):
    '''Return a list of tables files used by the model'''
    l = []
    for filename in os.listdir(self.dir):
      if filename.split('.')[-1].lower()=='atb2x':
        l.append(filename)
    
    return l
  
  def _get_modelName(self):
    # Get list of .ain2 files in model directory
    return os.path.split(self.__model_file)[1].split('.')[0]

  def _get_modelDir(self):
    return os.path.split(self.__model_file)[0]
  
  def _isLocked(self):
    return os.path.exists(os.path.join(self.dir, '%s'%(self.filename + '.lock')))
  
  def _get_modelFile(self):
    return os.path.split(self.__model_file)[1]

  @property
  def output(self):
    '''List of available output from model

    Returns:
      Dataframe of outputs
    '''
    pass

  @property
  def dir(self):
    '''Path to model 

    '''
    return self._get_modelDir()
  
  @property
  def tables(self):
    '''Get list of ALFA Table Files present for the model

    Returns:
      List of filenames as strings
    '''
    return self._get_tableFiles()
  
  @property
  def name(self):
    '''Name of the model, without the \*.ain2 extension'''
    return self._get_modelName()
  
  @ property
  def filename(self):
    '''Name of the model file, with the \*.ain2 extension'''
    return self._get_modelFile()
  
  @property
  def locked(self):
    '''
    Returns:
      True if someone is using the model in ALFA, otherwise False
    '''
    return self._isLocked()

class AIA:
  '''Instance of ALFA Input Asset. These are basically just text files

  Attributes:
    data: Underlying data for the AIA (all available segments)
    output_dest (str): Where to save the \*.aia2 files upon building
  '''
  def __init__(self, name, mod = None):
    self.__name = name
    self.__model = mod # Underlying model for which these AIAs are used
    self.__outfile_name = '%s_%s.aia2' %('SEGNUMBER', self.__name)
    if mod:
      if isinstance(mod, Model):
        # User provided a Model instance
        self.__outputDest = mod.dir
        # TODO: Let the following be dynamic
        self.defs_file = os.path.join(mod.dir, 'AIA_Definitions.JSON')
      else:
        raise ValueError("mod parameter provided, but is not a Model instance.")
  
  def _get_fields(self):
    # Read in the JSON definitions file
    with open(self.defs_file, 'r') as f:
      j = json.load(f)
    
    # Use self.name to get the aia definitions
    return list(j[self.name].keys())

  @property
  def output_dest(self):
    return self.__outputDest
  
  @output_dest.setter
  def output_dest(self, val):
    # Ensure that val is a valid location
    if os.path.exists(val):
      self.__outputDest = val
    else: 
      raise NotADirectoryError('Must provide a directory for output_dest')
  
  @property
  def outfile_name(self):
    '''Tells user how the AIA output file will be named'''
    return self.__outfile_name
  
  @outfile_name.setter
  def outfile_name(self, val):
    '''This will be the name of the resulting AIA outfile'''
    if isinstance(val, str):
      self.__outfile_name = val
    else:
      raise ValueError('Must provide a string value!')

  @ property
  def model(self):
    return self.__model

  @property
  def name(self):
    return self.__name
  
  @ property
  def fields(self):
    '''
    Returns:
      List of fields used by the AIA, per the definitions file

    '''
    return self._get_fields()
  
  def build(self, segs='all'):
    '''Build the AIAs using the data attribute

    Args:
      seg (optional list): Default is 'all'. Use to specify which segments to build. Each segment has its own file for output.
    
    TODO:
      Provide str-int flexibility (and zeropadness)
      Use AIA Definitions file 
    '''
    # Handle provided segments
    if isinstance(segs, str):
      segs = [segs] if segs.lower() != 'all' else list(self.__data['segment'].unique())
      
    elif not isinstance(segs, list):
      raise ValueError('Segments should be a str or a list of strings.')
    
    # Get the data we want
    df = self.__data
    
    ## Filter Data to desired segments
    subset = df.loc[df['segment'].isin(segs)]

    # Determine if we should aggregate the data
    if 'SEGNUMBER_' in self.outfile_name:
      # Create separate files for each segment
      # Loop through segments
      for seg in segs:
        outfile = self.outfile_name.replace('SEGNUMBER', seg)
        sub = subset.loc[subset['segment']==seg]
        sub.to_csv(outfile, sep = '\t', index = False, header=False)     
    else:
      # Put everything into the same file for the provided segments
      outfile = self.outfile_name
      # Output the AIA data to text file
      subset.to_csv(outfile, sep = '\t', index = False, header=False)      
    

class AIL:
  pass

class Output:
  '''Output from an ALFA run
  
  '''
  def __init__(self, **kwargs):
    pass