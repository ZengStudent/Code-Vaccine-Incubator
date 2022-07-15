import os
import subprocess
import time
from threading import Timer

# ====================================================================
# 宣告變數
# ====================================================================
# 資料夾數量(TestCase總數量)
total_folder_numbers = 50
# 組別數量(HOM組別總數量)
total_trail_numbers = 15
# 1組HOM的數量
numbers = 20


# 資料夾編號
folder_numbers = '1'
# 組別編號
trail_numbers = '1'

# 資料夾路徑(TestCase Sample)
sample_path = 'AST_TestCase_Sample_Folder/AST_HOM_TestCase_Sample_Folder'

# 資料夾路徑
path = 'AST_TestCase_Folder/AST_HOM_TestCase_Folder/AST_HOM_TestCase_Folder_' + folder_numbers + '/'
# 資料夾路徑(組別)
trial_path = path + 'AST_HOM_TestCase_Folder_' + folder_numbers + '_' + trail_numbers + '/'



import_unittest = '''
import unittest,os
'''
import_mutnat = ''''''

import_order = ''''''

import_class ='''
class TestStringMethods(unittest.TestCase):
    def setUp(self):
       self.test_a = 5
       self.test_b = 5
       self.test_c = 5
       self.result = ''
       print('--------------Setup--------------')

    def test_tri(self):
        print('--------------test_tri--------------')
        try :
            self.assertEqual(hom.tri(self.test_a,self.test_b,self.test_c),'Acute')
            print('Pass')
            self.result='Pass'
        except AssertionError:
            print('Fail')
            self.result = 'Fail'
        except:
            print('Fail')
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


# ====================================================================
# 宣告副程式
# ====================================================================
# 讀取TestCase Sample
def read_testcase_sample(folder_numbers):
    f = open(sample_path + '/AST_HOM_TestCase_Sample_' + str(folder_numbers) + '.txt', 'r+', encoding='UTF-8')
    contetnt = f.read()
    f.close()
    return contetnt


# 建立TestCase
def create_testcase(path,trial_path,folder_numbers,trail_numbers,numbers,import_class):
    for number in range(numbers):
        #  新建資料夾
        if (os.path.isdir(path) == False):
            os.mkdir(path)
        #  新建資料夾(trial)
        if (os.path.isdir(trial_path) == False):
            os.mkdir(trial_path)
        import_mutnat = 'from src.AST_Folder.AST_Mutant_Folder.AST_HOM_Folder.AST_HOM_Folder_' + str(trail_numbers) + ' import ' + 'HOM_'+str(trail_numbers) + '_' + str(number + 1) + ' as hom\n'
        import_variable = 'order = ' + str(number + 1) + '\n' + 'folder_numbers = ' + str(folder_numbers) + '\n' + 'trail_numbers = ' + str(trail_numbers) + '\n'
        file_dir = trial_path + 'AST_HOM_TestCase_' + str(number + 1) + '.py'
        f = open(file_dir, 'w+', encoding='UTF-8')
        f.write(import_unittest + import_mutnat + import_variable + import_class)
        f.seek(0)
        f.close()

# 進行單元測試
def do_unittest(trial_path,folder_numbers,trail_numbers,numbers):
    for number in range(numbers):
        retcode = -1
        print('folder_numbers: ',folder_numbers,' trail_numbers: ',trail_numbers,' number: ', number + 1)
        file_dir = trial_path + 'AST_HOM_TestCase_' + str(number + 1) + '.py'
        #os.system('python ' + file_dir)

        # 執行
        operation_code = ['python', file_dir]
        # 建立一個subprocess，執行operation_code
        f = subprocess.Popen(operation_code, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 建立一個timer(thread)，計時2s，2s後殺掉subprocess
        # 如果subprocess執行時間超過2s
        timer = Timer(1.0, f.kill)
        # 啟用timer
        timer.start()

        # print(f.stdout.read().decode('utf-8'))
        # print(f.stderr.read().decode('utf-8'))

        # 如果編譯成功，returncode會回傳0
        # 如果編譯失敗，returncode會回傳正整數負整數
        # 如果returncode一直保持0或-1代表沒有編譯失敗的情況
        if (retcode == 0 or retcode == -1):
            # 檢查碼(兩行一定要一起)
            res = f.communicate()
            retcode = f.returncode

        # 如果編譯失敗 且 無法執行TestCase的finally
        if (retcode != 0):
            # 預設為是發生While Loop
            print('infinite loop')
            # 由於無法抵達TestCase的finally，需在外部自行建立單元測試結果
            errpath = 'AST_TestCase_Result_Folder/AST_HOM_TestCase_Result_Folder/AST_HOM_TestCase_Result_Folder_' + str(folder_numbers) + '/'
            trial_errpath = errpath + 'AST_HOM_TestCase_Result_Folder_' + str(folder_numbers) + '_' + str(trail_numbers) + '/'
            #  新建資料夾
            if (os.path.isdir(errpath) == False):
                os.mkdir(errpath)
            #  新建資料夾
            if (os.path.isdir(trial_errpath) == False):
                os.mkdir(trial_errpath)
            file_dir = trial_errpath + 'AST_HOM_TestCase_Result_' + str(number + 1) + '.txt'
            f = open(file_dir, 'w+', encoding='UTF-8')
            f.write('infiniteloop')
            f.seek(0)
            f.close()




# 統整
def do_main():
    for i in range(total_folder_numbers):
        folder_numbers = str(i+1)
        # 去除zwnbsp字符
        import_class = str(read_testcase_sample(folder_numbers)[0:]).replace(u'\ufeff', '')
        # if(str(read_testcase_sample(folder_numbers)[0] == 0xFEFF)):
        #     import_class = str(read_testcase_sample(folder_numbers)[1:])
        # else:
        #     import_class = str(read_testcase_sample(folder_numbers)[0:])

        for j in range(total_trail_numbers):
            trail_numbers = str(j+1)
            path = 'AST_TestCase_Folder/AST_HOM_TestCase_Folder/AST_HOM_TestCase_Folder_' + folder_numbers + '/'
            trial_path = path + 'AST_HOM_TestCase_Folder_' + folder_numbers + '_' + trail_numbers + '/'

            create_testcase(path,trial_path,folder_numbers,trail_numbers,numbers,import_class)
            do_unittest(trial_path,folder_numbers,trail_numbers,numbers)




# ====================================================================
# 執行
# ====================================================================

do_main()






