from AST_Program.Computing_the_Median.SourceCode import Computing_the_Median as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.input_data = [7,8,9,5,1,2,2,3,4,5]
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.median(self.input_data),4.5)
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