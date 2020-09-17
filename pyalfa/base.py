import sys, os, json, glob, re
import xml.etree.ElementTree as ET
import pandas as pd

class Model:
  '''General class for an MG-ALFA model
  
  Attributes:
    valdate (str): date-like object representing the Valuation Date of the model
    asset_input: instance of :class: AIA
    liability_input: instance of :class: AIL
  
  Examples:
    Create an instance of a model::

      import pyalfa as mg
      m = mg.Model('P:/2020/083120/Assets_083120.ain2')
      
      # See what runs are available for the model
      m.runs

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
          raise FileNotFoundError("Could not find an ALFA model (*.ain2) within '%s'"%full_path_to_model_file)
          self.__model_file = ''
        else:
          # More than one model exists in the provided directory
          raise ValueError("More than one ALFA model exists within '%s'. Please specify which to use by providing its full filename when creating a Model instance."%(full_path_to_model_file))
          self.__model_file = ''
      else:
        # User provided a file. See if it is an ALFA model
        if not full_path_to_model_file.split('.')[-1].lower()=='ain2':
          raise ValueError("'%s' does not appear to be an ALFA model. Proceed with caution and double check what you have entered."%full_path_to_model_file)
        self.__model_file = full_path_to_model_file
    else:
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
  
  def _get_runs(self):
    # return list of runs in the model directory (for the model)
    files = glob.glob(os.path.join(self.dir, '%s.Run.*.Meta*'% self.name))
    return [re.search('Run\.(\d+)\.', f)[1] for f in files]
  
  def run(self, r):
    '''Get specific information for a run, as a run instance
    Args:
      r: Run ID can be a list of ids or a single id

    Returns:
      Instance of class Run
    '''
    # Ensure that r is a valid run
    # TODO: Provide some str-int leniency here
    if r not in self.runs:
      raise ValueError('%s does not appear to be an available run. Check that its output is in "%s"'%(r, self.dir))
      return # Do we even need this
    
    # Read in the XML output from the run
    if os.path.exists(os.path.join(self.dir, '%s.Run.%s.Metadata.xml' %(self.name, r))):
      d = dict()
      tree = ET.parse(os.path.join(self.dir, '%s.Run.%s.Metadata.xml' %(self.name, r)))
      root = tree.getroot()
      for child in root:
        if len(child.attrib)==1:
          # Easiest case
          d[child.attrib['Type']] = child.text
        else:
          if not child.attrib['Type'] in d.keys():
            # First encounter of attribute
            d[child.attrib['Type']] = dict()
          
          d[child.attrib['Type']][child.attrib['Key']] = child.text
    
    # Create instance of Run class using XML data
    return Run(**(self.__dict__), **d)  

  @property
  def runs(self):
    return self._get_runs()

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

class Asset:
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
    

class Liability:
  pass

class Run(Model): # We want to pass some model methods
  '''An ALFA run
  
  Attributes:
    output
    id
    **kwargs (from metadata XML)  
  
  TODO:
    Add '_' prefix to *kwargs, maybe...
      OR: have an attribute called 'meta' that contains all that info. Yeah I like that better...
  '''

  def __init__(self, output=False, **kwargs):
    # TODO: ensure that name and dir are passed by the model
    self.__dict__.update(kwargs)

    self.__id = self.ProjectionId.split('.')[-1]
    # Calling getOutput() takes a long time for asset projections, so pass a parameter specifying whether to do it
    if output:
      self.__output = self._getOutput()
    else:
      self.__output = None

  def _getOutput(self):
    # TODO: What happens when there are both TT and STT??
      # ? Perhaps a dictionary of dataframe values with template as key?
    # ! Use glob() here to get number of output files for Run
    # Use run info to read in the output file
    if os.path.exists(os.path.join(self.dir, '%s.Proj.%s.Run.%s.Rreq.006.Subtotal001.txt'%(self.name,self.id,self.id))):
      return pd.read_csv(
        os.path.join(self.dir, '%s.Proj.%s.Run.%s.Rreq.006.Subtotal001.txt'%(self.name,self.id,self.id))
        , sep = '\t'
      )
    elif os.path.exists(os.path.join(self.dir, '%s.Proj.%s.Run.%s.Rreq.010.Total002.txt'%(self.name,self.id,self.id))):
      return pd.read_csv(
        os.path.join(self.dir, '%s.Proj.%s.Run.%s.Rreq.010.Total002.txt'%(self.name,self.id,self.id))
        , sep = '\t'
      )
    else:
      raise FileNotFoundError("Could not find output for %s.Proj.%s in '%s' ... Its possible that I am not yet equipped to read in the output your looking for."%(self.name, self.id, self.dir))

  def _getLogs(self):
    '''Get debug and grid logs'''
    logs = glob.glob(os.path.join(self.dir, '%s.Run.%s.*.log'% (self.name, self.id)))
    keys = [re.search('run\.\d+\.(.+)\.log', x.lower())[1] for x in logs] if logs else []
    
    # Return a dict with logName and fileName?
    return dict(zip(keys, logs))

  @property
  def id(self):
    return self.__id
  
  @property
  def output(self):
    '''View output from the run in tabular form'''
    return self.__output
  
  @property
  def description(self):
    return self.ProjectionDescription
  
  @property
  def valdate(self):
    return self.ValuationDate
  
  @property
  def logs(self):
    return self._getLogs()
    
