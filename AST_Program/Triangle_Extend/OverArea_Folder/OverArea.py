from AST_Program.Triangle_Extend.SourceCode import Triangle_Extend as amutant
import unittest,os


class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.test_a = 3
       self.test_b = 4
       self.test_c = 5
       self.result = '-'
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.tri(self.test_a,self.test_b,self.test_c),'Right Scalane')
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