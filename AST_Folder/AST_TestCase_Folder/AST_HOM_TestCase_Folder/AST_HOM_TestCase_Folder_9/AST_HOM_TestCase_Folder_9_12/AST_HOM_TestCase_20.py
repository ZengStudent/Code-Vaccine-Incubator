
import unittest,os
from src.AST_Folder.AST_Mutant_Folder.AST_HOM_Folder.AST_HOM_Folder_12 import HOM_12_20 as hom
order = 20
folder_numbers = 9
trail_numbers = 12
class TestStringMethods(unittest.TestCase):
        def setUp(self):
            self.input_a = 9
            self.result = '-'
            
            print('--------------Setup--------------')

        def test_tri(self):
            print('--------------test_tri--------------')
            try :
                self.assertEqual(hom.fib(self.input_a),34)
                print('Pass')
                self.result='Pass'
            except AssertionError:
                print('AssertionError')
                self.result = 'Fail'
            except:
                print('ExceptError')
                self.result = 'Fail'
            finally:
                path = 'AST_TestCase_Result_Folder/AST_HOM_TestCase_Result_Folder/AST_HOM_TestCase_Result_Folder_' + str(folder_numbers) + '/'
                trial_path = path + 'AST_HOM_TestCase_Result_Folder_' + str(folder_numbers) + '_' + str(trail_numbers) + '/'
                #  新建資料夾
                if(os.path.isdir(path) == False):
                    os.mkdir(path)
                #  新建資料夾
                if(os.path.isdir(trial_path) == False):
                    os.mkdir(trial_path)
                file_dir = trial_path +'AST_HOM_TestCase_Result_'+str(order)+'.txt'
                f = open(file_dir, 'w+', encoding='UTF-8')
                f.write(self.result)
                f.seek(0)
                f.close() 

if __name__ == '__main__':
    unittest.main()
        