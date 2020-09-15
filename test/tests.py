import unittest
import sys
sys.path.append('../pyalfa')
sys.path.append('..')
sys.path.append('pyalfa')
from base import Model

class Test_Model_Init(unittest.TestCase):
  
  def test_init_fine(self):
    m = Model('P:/2020/083120/Assets_083120.ain2')
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
    m = Model('P:/2020/083120/Assets_083120.ain2')
    self.assertEqual(m.name, 'Assets_083120', 'This should be the model name without an extension')    
  
  def test_model_dir(self):
    m = Model('P:/2020/083120/Assets_083120.ain2')
    self.assertEqual(m.dir, 'P:/2020/083120', 'This should be the path to the model')

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
  unittest.main()