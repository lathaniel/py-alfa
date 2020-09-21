import unittest
import sys, shutil, os
sys.path.append('../pyalfa')
sys.path.append('..')
sys.path.append('pyalfa')
from base import Model, Asset

def create_dummy_model_folder(model_dir):
  # Create the model directory for testing
  if not os.path.exists(model_dir):
    os.mkdir(model_dir)
    os.mkdir(os.path.join(model_dir, 'TheresNoModelHere'))
    os.mkdir(os.path.join(model_dir, 'ThereAreTwoModelsHere'))

  # Create ALFA files within model directory
  open(os.path.join(model_dir, 'TestModel.ain2'), 'a').close()
  open(os.path.join(os.path.join(model_dir, 'ThereAreTwoModelsHere'), 'TestModel1.ain2'), 'a').close()
  open(os.path.join(os.path.join(model_dir, 'ThereAreTwoModelsHere'), 'TestModel2.ain2'), 'a').close()
  open(os.path.join(model_dir, 'TableFile01.xlsx'), 'a').close()
  open(os.path.join(model_dir, 'TableFile01.xlsx.atB2X'), 'a').close()
  open(os.path.join(model_dir, 'AssetInput01.aia2'), 'a').close()
  open(os.path.join(model_dir, 'AssetInput02.aia2'), 'a').close()
  open(os.path.join(model_dir, 'LiabInput01.ail2'), 'a').close()
  open(os.path.join(model_dir, 'LiabInput02.ail2'), 'a').close()

  # Create AIA definitions in model directory (copied from files)
  # Get this file's directory
  test_dir = os.path.dirname(os.path.realpath(__file__))
  shutil.copy(
    os.path.join(test_dir, 'files', 'AIA_Definitions.json')
    ,os.path.join(model_dir, 'AIA_Definitions.json')
  )

def clear_dummy_model_folder(model_dir):
  shutil.rmtree(model_dir)

class Test_Model_Init(unittest.TestCase):
  
  def test_init_NotAModel(self):
    with self.assertRaises(ValueError):
      result = Model('FAKE_MODEL_DIR/AssetInput01.aia2')
  
  def test_init_ProvidedFolderWithModel(self):
    result = result = Model('FAKE_MODEL_DIR')
    self.assertIsInstance(result, Model)
  
  def test_init_ProvidedFolderWithoutModel(self):
    with self.assertRaises(FileNotFoundError):
      result = Model('FAKE_MODEL_DIR/TheresNoModelHere')
  
  def test_init_ProvidedFolderWithMultipleModels(self):
    with self.assertRaises(ValueError):
      result = Model('FAKE_MODEL_DIR/ThereAreTwoModelsHere')

  def test_init_fine(self):
    m = Model('FAKE_MODEL_DIR/TestModel.ain2')
    self.assertIsInstance(m, Model)

  def test_init_path_not_exists(self):    
    with self.assertRaises(FileNotFoundError):
      result = Model('NOTADIRECTORY')

  def test_init_no_model_in_path(self):
    pass

  def test_init_mult_model_in_path(self):
    pass    

class Test_Model_Attrs(unittest.TestCase):
  
  def test_model_name(self):
    m = Model('FAKE_MODEL_DIR/TestModel.ain2')
    self.assertEqual(m.name, 'TestModel', 'This should be the model name without an extension')    
  
  def test_model_file(self):
    m = Model('FAKE_MODEL_DIR/TestModel.ain2')
    self.assertEqual(m.filename, 'TestModel.ain2', 'This should be the model name with an extension')    
  
  def test_model_dir(self):
    m = Model('FAKE_MODEL_DIR/TestModel.ain2')
    self.assertEqual(m.dir, 'FAKE_MODEL_DIR', 'This should be the path to the model')
  
  def test_model_locked(self):
    m = Model('FAKE_MODEL_DIR/TestModel.ain2')
    # Create a lock file, which occurs when a model is open in ALFA
    open(os.path.join(m.dir, 'TestModel.ain2.lock'), 'a').close()
    self.assertTrue(m.locked)

    os.remove(os.path.join(m.dir, 'TestModel.ain2.lock'))
    self.assertFalse(m.locked)  

  def test_table_files_fine(self):
    result = Model('FAKE_MODEL_DIR/TestModel.ain2')
    self.assertEqual(result.tables, ['TableFile01.xlsx.atB2X'])
  
  def test_table_files_empty(self):
    result = Model('FAKE_MODEL_DIR/TestModel.ain2')
    os.remove(os.path.join(result.dir, 'TableFile01.xlsx.atB2X'))
    self.assertEqual(result.tables, [])
    open(os.path.join(result.dir, 'TableFile01.xlsx.atB2X'), 'a').close()

  def test_model_output(self):
    pass

  def test_model_name_setter(self):
    pass

  def test_model_nickname(self):
    pass
  
  def test_exclude_assets(self):
    pass

class Test_AIA_init(unittest.TestCase):
  def test_AIA_fine(self):
    result = Asset('Bond')
    self.assertIsInstance(result, Asset)
    self.assertIsNone(result.model)
  
  def test_AIA_badModel(self):
    with self.assertRaises(ValueError):
      result = Asset('Bond', 'string')

  def test_AIA_goodModel(self):
    result = Asset('Bond', Model('FAKE_MODEL_DIR/TestModel.ain2'))
    self.assertIsInstance(result.model, Model)

class Test_AIA_attrs(unittest.TestCase):
  '''
  TODO:
    - No AIA defs file in directory
    - AIA name not in defs file
  '''
  def test_aia_fields(self):
    result = Asset('Bond', Model('FAKE_MODEL_DIR/TestModel.ain2'))
    self.assertIsInstance(result.fields, list)

  def test_build_segs_param(self):
    # str provided
    # int provided
    # bad type(s) provided
    # list of str
    # list of int
    # list of bad type(s)
    pass

  def test_build_without_data(self):
    pass

  def test_build_good(self):
    pass

  def test_build_empty_data(self):
    pass

  def test_build_without_definitions_file(self):
    pass

class Test_AIL_init(unittest.TestCase):
  pass

class Test_Output_init(unittest.TestCase):
  pass

if __name__=="__main__":
  create_dummy_model_folder(model_dir='FAKE_MODEL_DIR')
  unittest.main(exit=False)
  clear_dummy_model_folder(model_dir='FAKE_MODEL_DIR')