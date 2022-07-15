from AST_Program.Binary_Search.SourceCode import Binary_Search as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.input_data = [ 2,9,30,32,38,47,61,69,79,81 ]
       self.start = 0
       self.maxlen = len(self.input_data)-1
       self.aim = 10
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.binary_search(self.input_data,self.start,self.maxlen,self.aim),-1)
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