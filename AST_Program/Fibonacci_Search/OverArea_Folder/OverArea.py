from AST_Program.Fibonacci_Search.SourceCode import Fibonacci_Search as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.input_data = [10, 22, 30, 44, 56, 58, 60, 70, 100, 110, 130]
       self.number = 60
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.FibonacciSearch(self.input_data,self.number),6)
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