import sys, os

class Model:
  '''General class for an MG-ALFA model
  
  Attributes:
    valdate (str): date-like object representing the Valuation Date of the model
    asset_input: instance of :class: AIA
    asset_liability: instance of :class: AIL
    name (str): Optional nickname for the model

  '''
  def __init__(self, model_dir, valdate = None):
    # TODO: Look for *.ain2 as the actual model
    # ensure the model exists
    if os.path.exists(model_dir):
      self.__model_dir = model_dir
    else:
      print("Could not initialize model in directory '%s'\nMake sure you entered the path correctly and that it can be accessed by you."%model_dir)
      return None
    
    # Give the model a valuation date, even though it won't really be useful in practice

  
  def _get_tableFiles(self):
    '''return a list of tables files used by the model'''
    l = []
    for filename in os.listdir(self.__model_dir):
      if filename.split('.')[-1].lower()=='atb2x':
        l.append(filename)
    
    return l

  @property
  def dir(self):
    '''Path to model directory

    '''
    return self.__model_dir
  
  @property
  def tables(self):
    '''Get list of table files present for the model

    Returns:
      List of filenames as strings
    '''
    return self._get_tableFiles()      

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