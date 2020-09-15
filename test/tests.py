import unittest
import sys, shutil, os
sys.path.append('../pyalfa')
sys.path.append('..')
sys.path.append('pyalfa')
from base import Model

def create_dummy_model_folder(model_dir):
  # Create the model directory for testing
  if not os.path.exists(model_dir):
    os.mkdir(model_dir)

  # Create test files within model directory
  open(os.path.join(model_dir, 'TestModel.ain2'), 'a').close()
  open(os.path.join(model_dir, 'TableFile01.xlsx'), 'a').close()
  open(os.path.join(model_dir, 'TableFile01.xlsx.atB2X'), 'a').close()
  open(os.path.join(model_dir, 'AssetInput01.aia2'), 'a').close()
  open(os.path.join(model_dir, 'AssetInput02.aia2'), 'a').close()
  open(os.path.join(model_dir, 'LiabInput01.ail2'), 'a').close()
  open(os.path.join(model_dir, 'LiabInput02.ail2'), 'a').close()

def clear_dummy_model_folder(model_dir):
  shutil.rmtree(model_dir)

class Test_Model_Init(unittest.TestCase):
  
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
  
  def test_model_dir(self):
    m = Model('FAKE_MODEL_DIR/TestModel.ain2')
    self.assertEqual(m.dir, 'FAKE_MODEL_DIR', 'This should be the path to the model')

  def test_table_files(self):
    pass    

  def test_model_output(self):
    pass

class Test_AIA_init(unittest.TestCase):
  def test_AIA_fine(self):
    pass

class Test_AIL_init(unittest.TestCase):
  pass

class Test_Output_init(unittest.TestCase):
  pass

if __name__=="__main__":
  create_dummy_model_folder(model_dir='FAKE_MODEL_DIR')
  unittest.main(exit=False)
  clear_dummy_model_folder(model_dir='FAKE_MODEL_DIR')