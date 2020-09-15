import sys, os

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
    # TODO: Look for *.ain2 as the actual model
    # ensure the model exists
    if os.path.exists(full_path_to_model_file):
      self.__model_file = full_path_to_model_file
    else:
      print("Could not initialize model at '%s'\nMake sure you entered the path correctly and that it can be accessed by you."%full_path_to_model_file)
      raise FileNotFoundError("Could not initialize model at '%s'\nMake sure you entered the path correctly and that it can be accessed by you."%full_path_to_model_file)
    
    # Give the model a valuation date, even though it won't really be useful in practice
  
  def _get_tableFiles(self):
    '''return a list of tables files used by the model'''
    l = []
    for filename in os.listdir(self.__model_file):
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
    '''Get list of table files present for the model

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
    name (str): name of the asset input, e.g. Bond
    fields (list): list of fields used by the AIA file
    data: Underlying data for the AIA (all available segments)
    output_dest (str): Where to save the \*.aia2 files upon building
  '''
  def __init__(self, name):
    self.name = name
  
  def build(self, segs='all'):
    '''Build the AIAs using the data attribute

    Args:
      seg (optional list): Default is 'all'. Use to specify which segments to build. Each segment has its own file for output.
    
    '''
    if segs.lower()=='all':
      df = self.__data
      for seg in df['segment'].unique():
        
        outfile = '%s_%s.aia2'%(seg, self.__name)
        segment_subset = df.loc[df.segment==seg]

        # Output the AIA data to text file
        segment_subset.to_csv(outfile, sep = '\t', index = False, header=False)
    
    else:
      # Ensure a list of segments was passed
      pass

class AIL:
  pass

class Output:
  '''Output from an ALFA run
  
  '''
  def __init__(self, **kwargs):
    pass