from AST_Program.Bubble_Sort.SourceCode import Bubble_Sort as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.input_data = [64, 34, 25, 12, 22, 11, 90]
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.bubble_sort(self.input_data),[11, 12, 22, 25, 34, 64, 90])
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