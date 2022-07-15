from AST_Program.Fibonacci_Number_NonRecursive.SourceCode import Fibonacci_Number_NonRecursive as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.input = 4
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.fib(self.input),[1, 1, 2, 3])
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