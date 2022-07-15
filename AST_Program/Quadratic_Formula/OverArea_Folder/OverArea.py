from AST_Program.Quadratic_Formula.SourceCode import Quadratic_Formula as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.input_a = 2
       self.input_b = 2
       self.input_c = 1
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.quf(self.input_a,self.input_b,self.input_c),'(-0.5-0.5j),(-0.5+0.5j)')
            print('Pass')
            self.result='Pass'
        except AssertionError:
            print('Fail')
            self.result = 'Fail'
        finally:
            file_dir = 'AST_FOM_TestCase_Result_1.txt'
            f = open(file_dir, 'w+', encoding='UTF-8')
            f.write(self.result)
            f.seek(0)
            f.close()

if __name__ == '__main__':
    unittest.main()