import os, shutil
import random
from AST_Program.Computing_the_Median.SourceCode import Computing_the_Median as amutant


def create_folder(path, name, numbers):
    for i in range(1, numbers + 1):
        file_name = path + name + str(i) + '.txt'
        if os.path.isfile(file_name) == False:
            with open(file_name, 'w+', encoding='utf-8') as f:
                f.write('')

    return None


def create_testdata():
    #
    input_data = {}
    output_data = {}
    numbers = 50
    input_numbers = 50
    temp_input = random.randint(5,20)
    temp_output = 0
    #
    for i in range(1, numbers + 1):
        input_data[str(i)] = []
        output_data[str(i)] = []
        # input_data
        for j in range(1, input_numbers + 1):
            input_data[str(i)].append(temp_input)

            # greater than
            if (random.randint(1, 3) == 1):
                print('greater than')
                temp_input = random.randint(temp_input + random.randint(1, 10), temp_input + random.randint(11, 20))
            # less than
            elif (random.randint(1, 3) == 2):
                print('less than')
                temp_input = random.randint(temp_input - random.randint(11, 20), temp_input - random.randint(1, 10))
            # equal
            else:
                print('equal')
                temp_input = temp_input

        # output_data
        temp_output = amutant.median(input_data[str(i)])
        output_data[str(i)] = temp_output

    return input_data, output_data


def create_testcase():
    # 宣告 Loacl Variable
    # input
    input_data = {}
    # output
    output_data = {}
    # Generator input,output
    input_data, output_data = create_testdata()

    # TestData
    for name, value in sorted(input_data.items()):
        with open('TestData.txt','a+',encoding='utf-8') as td:
            td.write(str(value) + '\n' + str(output_data[name]) + '\n')

    # FOM
    for name, value in input_data.items():
        # part one
        part_one = '''class TestStringMethods(unittest.TestCase):
    def setUp(self):'''
        # part two
        part_two = '''
        self.input_a = ''' + str(value) + '''
        self.result = '-'
        '''
        # part three
        part_three = '''
        print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(amutant.'''
        # part four
        part_four = '''median(self.input_a),''' + str(output_data[name]) + ')'
        # part five
        part_five = '''\n            print('Pass')
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
    '''
        # 寫檔
        with open('AST_FOM_TestCase_Sample_' + str(name) + '.txt', 'w+', encoding='utf-8') as f:
            f.write(part_one + part_two + part_three + part_four + part_five)

        # HOM
        for name, value in input_data.items():
            # part one
            part_one = '''class TestStringMethods(unittest.TestCase):
        def setUp(self):'''
            # part two
            part_two = '''
            self.input_a = ''' + str(value) + '''
            self.result = '-'
            '''
            # part three
            part_three = '''
            print('--------------Setup--------------')

        def test_tri(self):
            print('--------------test_tri--------------')
            try :
                self.assertEqual(hom.'''
            # part four
            part_four = '''median(self.input_a),''' + str(output_data[name]) + ')'
            # part five
            part_five = '''\n                print('Pass')
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
        '''
            # 寫檔
            with open('AST_HOM_TestCase_Sample_' + str(name) + '.txt', 'w+', encoding='utf-8') as f:
                f.write(part_one + part_two + part_three + part_four + part_five)
    return None


create_folder('', 'AST_FOM_TestCase_Sample_', 50)
create_folder('', 'AST_HOM_TestCase_Sample_', 50)
create_testcase()







