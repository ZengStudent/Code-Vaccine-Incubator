
import unittest,os
from src.AST_Folder.AST_Mutant_Folder.AST_FOM_Folder import AST_FOM_18 as amutant
order = 18
folder_numbers = 25
class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.input_a = 25
        self.result = '-'
        
        print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.fib(self.input_a),75025)
            print('Pass')
            self.result='Pass'
        except AssertionError:
            print('AssertionError')
            self.result = 'Fail'
        except:
            print('ExceptError')
            self.result = 'Fail'
        finally:
            path = 'AST_TestCase_Result_Folder/AST_FOM_TestCase_Result_Folder/AST_FOM_TestCase_Result_Folder_'+ str(folder_numbers) + '/'
            #  新建資料夾
            if(os.path.isdir(path) == False):
                os.mkdir(path)
            file_dir = path +'AST_FOM_TestCase_Result_'+str(order)+'.txt'
            f = open(file_dir, 'w+', encoding='UTF-8')
            f.write(self.result)
            f.seek(0)
            f.close() 

if __name__ == '__main__':
    unittest.main()
    