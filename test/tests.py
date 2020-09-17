import unittest
import sys, shutil, os
sys.path.append('../pyalfa')
sys.path.append('..')
sys.path.append('pyalfa')
from base import Model, AIA

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

  # Create AIA definitions in model directory
  with open(os.path.join(model_dir, 'AIA_Definitions.JSON'), 'w') as f:
    f.write(
      '''
      {
   "Bond": {
      "ck.Cusip": {
         "Value": "[a_cusip_cd]",
         "Index": 0,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.YrsToMat": {
         "Value": "[YTM]",
         "Index": 1,
         "Format": "ZeroPad(3)",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.AssetGroup": {
         "Value": "[AssetGroup]",
         "Index": 2,
         "Format": "ZeroPad(2)",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.AVRCat": {
         "Value": "[AVR]",
         "Index": 3,
         "Format": "ZeroPad(2)",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.QualRating": {
         "Value": "[a_naic_wt_nmbr]",
         "Index": 4,
         "Format": "Integer",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.NAICSVO": {
         "Value": "[numeric_rtg]",
         "Index": 5,
         "Format": "Integer",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.GAAPCat": {
         "Value": "_",
         "Index": 6,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char2": {
         "Value": "[int_rtg_char]",
         "Index": 7,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char3": {
         "Value": "[fpc_rtg_char]",
         "Index": 8,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char4": {
         "Value": "[mw_char]",
         "Index": 9,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char5": {
         "Value": "[sp_credit_cd]",
         "Index": 10,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char6": {
         "Value": "[sp_intrt_cd]",
         "Index": 11,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char7": {
         "Value": "_",
         "Index": 12,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ck.Char8": {
         "Value": "_",
         "Index": 13,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ParVal": {
         "Value": "[ParVal]",
         "Index": 14,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "BookValInit": {
         "Value": "[BookVal]",
         "Index": 15,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "MarketValInit": {
         "Value": "[MarketVal]",
         "Index": 16,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "IssueDate": {
         "Value": "[IssueDate]",
         "Index": 17,
         "Format": "Date",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "PaymentDate": {
         "Value": "[PaymentDate]",
         "Index": 18,
         "Format": "Date",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "BookMatDate": {
         "Value": "[BookMatDate]",
         "Index": 19,
         "Format": "Date",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ParRate": {
         "Value": "[ParRate]",
         "Index": 20,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "PaymentFreq": {
         "Value": "[a_int_mode_rec_nmbr]",
         "Index": 21,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "PaymentTime": {
         "Value": "[PaymentTime]",
         "Index": 22,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "TaxableIntPct": {
         "Value": "[TaxableIntPct]",
         "Index": 23,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "FirstCallDate": {
         "Value": "[FirstCallDate]",
         "Index": 24,
         "Format": "Date",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "FirstCallPremPer": {
         "Value": "[FirstCallPremPer]",
         "Index": 25,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ParCallDate": {
         "Value": "[ParCallDate]",
         "Index": 26,
         "Format": "Date",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "SalePriority": {
         "Value": "[SalePriority]",
         "Index": 27,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "GAAPSFAS115Type": {
         "Value": "[GAAPSFAS115Type]",
         "Index": 28,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "LiquidityRank": {
         "Value": "[LiquidityRank]",
         "Index": 29,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "yieldinp": {
         "Value": "[nom_yld_rt]",
         "Index": 30,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "InvExpPer": {
         "Value": "[InvExpPer]",
         "Index": 31,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "FPCC1SubFlg": {
         "Value": "[FPCSub_Flag]",
         "Index": 32,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "StatClass": {
         "Value": "[StatClass]",
         "Index": 33,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "FPCC1BVFlg": {
         "Value": "[FPCBV_Flag]",
         "Index": 34,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "CallModelFlg": {
         "Value": "[CallModel_Flag]",
         "Index": 35,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "MuniFlg": {
         "Value": "[Muni_Flag]",
         "Index": 36,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "FloatFlg": {
         "Value": "[Float_Flag]",
         "Index": 37,
         "Format": "Integer",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "PreRefundFlg": {
         "Value": "[PreRefund_Flag]",
         "Index": 38,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "GroupID": {
         "Value": "[AssetGroup]",
         "Index": 39,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "obvACallSpreadInp": {
         "Value": "[OAS]",
         "Index": 40,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "C1Flg": {
         "Value": "[C1_flg]",
         "Index": 41,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      },
      "ScalarFlg": {
         "Value": "[Scalar]",
         "Index": 42,
         "Format": "None",
         "Source": "TODO",
         "Description": "None",
         "Notes": "None",
         "Needed": "TODO"
      }
   }
  }   '''
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

class Test_AIA_init(unittest.TestCase):
  def test_AIA_fine(self):
    result = AIA('Bond')
    self.assertIsInstance(result, AIA)
    self.assertIsNone(result.model)
  
  def test_AIA_badModel(self):
    with self.assertRaises(ValueError):
      result = AIA('Bond', 'string')

  def test_AIA_goodModel(self):
    result = AIA('Bond', Model('FAKE_MODEL_DIR/TestModel.ain2'))
    self.assertIsInstance(result.model, Model)

class Test_AIA_attrs(unittest.TestCase):
   '''
   TODO:
      - No AIA defs file in directory
      - AIA name not in defs file
   '''
   def test_aia_fields(self):
      result = AIA('Bond', Model('FAKE_MODEL_DIR/TestModel.ain2'))
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