import os

# 用兩個Dict紀錄所有檔名，一個紀錄Pass、另一個Fail，然後把每個測試結果分別計算到Dict當中，最後看哪個檔名只存在Pass或Fail。

# --------------------------------------------------------------------
# 宣告變數
# --------------------------------------------------------------------
# 全部的測試案例
T = []


# filter all none-testcase(完全沒被殺死)
FOM_possible_equivalent = []
# filter all testcase(全部被殺死)
FOM_possible_dumb = []
# filter all part-testcase(部分殺死)
FOM_possible_part = []

# 測試結果(Pass)
FOM_pass_dict = {}
# 測試結果(Fail)
FOM_fail_dict = {}
# 測試結果目錄的檔名
FOM_name_list = []

# 殺死各個FOM的TestCase(轉化前)
FOM_killed_testcase_before = {}
# 殺死各個FOM的TestCase(轉化後)
FOM_killed_testcase_after = {}

# FOM Fragility 的字典
FOM_Fragility = {}

# 各個TestCase殺死FOM的字典
testcase_killed_dict = {}

# 根目錄(for FOM)
root_fom_dir = 'AST_TestCase_Result_Folder/AST_FOM_TestCase_Result_Folder/'

# 根目錄(for TestCase)
root_testcase_dir = 'AST_TestCase_Folder/AST_FOM_TestCase_Folder/'

# 測試案例的測試結果目錄
file_dir = []

# 輸出殺死FOM的測試案例的路徑
fom_killed_testcase_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_FOM_Killed_TestCase_Folder'

# 輸出測試案例殺死FOM的路徑
test_killed_fom_dir = 'AST_TestCase_Killed_Mutant_Folder/AST_FOM_Killed_TestCase_Folder'

# 輸出報告路徑
report_dir = 'AST_Report_Folder/AST_FOM_Report_Folder/'


# --------------------------------------------------------------------
# 宣告副程式
# --------------------------------------------------------------------

# 取得TestCase測試結果目錄(root_fom_dir:根目錄(for FOM),root_testcase_dir:根目錄(for TestCase))
def get_root_dir(root_fom_dir,root_testcase_dir):
    for name in os.listdir(root_fom_dir):
        if (os.path.isdir(root_fom_dir + name)):
            file_dir.append(root_fom_dir + name + '/')
        # 鍵立各個TestCase殺死FOM的Key，value設為空List
        testcase_killed_dict[name] = []

# 取得TestCase測試結果目錄的檔名(file_dir:測試案例的測試結果目錄)
def get_file_dir(file_dir):
    for name in os.listdir(file_dir[0]):
        if ('.txt' in name):
            # 去除.txt
            name = name[:-4]
            # 建立測試結果(Pass)字典
            FOM_pass_dict[name] = 0
            # 建立測試結果(Fail)字典
            FOM_fail_dict[name] = 0
            # 建立殺死各個FOM的字典
            FOM_killed_testcase_before[name] = []
            # 建立測試結果目錄的檔名
            FOM_name_list.append(name)

# 取得結果(file_dir:測試案例的測試結果目錄)
def get_testcase_result(file_dir):
    for dir in file_dir:
        # TestCase測試結果路徑底下全部檔名
        test_result_name = os.listdir(dir)

        # 讀取測試結果
        for name in test_result_name:
            if ('.txt' in name):
                with open(dir + str(name), 'r') as file:
                    result = file.readline()
                    if (result == 'Pass'):
                        # 去除.txt
                        name = name[:-4]
                        FOM_pass_dict[name] = FOM_pass_dict[name] + 1
                    elif (result == 'Fail'):
                        # 去除.txt
                        name = name[:-4]
                        FOM_fail_dict[name] = FOM_fail_dict[name] + 1
                        # 紀錄殺死各個FOM的TestCase
                        FOM_killed_testcase_before[name].append(dir)
                    elif (result == '-'):
                        # 去除.txt
                        name = name[:-4]
                        FOM_fail_dict[name] = FOM_fail_dict[name] + 1
                        # 紀錄殺死各個FOM的TestCase
                        FOM_killed_testcase_before[name].append(dir)
                    elif (result == 'infiniteloop'):
                        # 去除.txt
                        name = name[:-4]
                        FOM_fail_dict[name] = FOM_fail_dict[name] + 1
                        # 紀錄殺死各個FOM的TestCase
                        FOM_killed_testcase_before[name].append(dir)
                    else:
                        print(dir, name, 'Err')

# 篩選(FOM_name_list:測試結果目錄的檔名,FOM_pass_dict:測試結果,FOM_fail_dict測試結果,FOM_possible_part:部分殺死的FOM,FOM_possible_equivalent:完全沒被殺死的FOM,FOM_possible_dumb:全部被殺死的FOM)
def filter_FOM(FOM_name_list,FOM_pass_dict,FOM_fail_dict,FOM_possible_part,FOM_possible_equivalent,FOM_possible_dumb):
    for name in FOM_name_list:
        # (部分殺死)
        if (FOM_pass_dict[name] >= 1 and FOM_fail_dict[name] >= 1):
            FOM_possible_part.append(name.replace('_FOM_TestCase_Result_', '_Mutant_'))
            continue
        # (完全沒被殺死)
        elif (FOM_pass_dict[name] >= 1 and FOM_fail_dict[name] <= 0):
            FOM_possible_equivalent.append(name.replace('_FOM_TestCase_Result_', '_Mutant_'))
            continue
        # (全部被殺死)
        elif (FOM_pass_dict[name] <= 0 and FOM_fail_dict[name] >= 1):
            FOM_possible_dumb.append(name.replace('_FOM_TestCase_Result_', '_Mutant_'))
            continue

# 轉化殺死各個FOM的字典(FOM_killed_testcase_before:殺死各個FOM的TestCase(轉化前), testcase_killed_dict:各個TestCase殺死FOM的字典)
def convert_FOM_killed_testcase(FOM_killed_testcase_before,testcase_killed_dict):
    # 暫存殺死各個FOM的TestCase(轉化後)
    temp_FOM_killed_testcase_after = {}


    # 轉化殺死各個FOM的字典
    for name, killed in FOM_killed_testcase_before.items():
        # 改名
        fom_name = name.replace('_FOM_TestCase_Result_', '_FOM_')
        temp_FOM_killed_testcase_after[fom_name] = []
        # 改名
        for killed_testcase in killed:
            killed_testcase_name = killed_testcase.replace('AST_TestCase_Result_Folder/AST_FOM_TestCase_Result_Folder/AST_FOM_TestCase_Result_Folder_', '')
            killed_testcase_name = killed_testcase_name.replace('/', '')
            temp_FOM_killed_testcase_after[fom_name].append(killed_testcase_name)
            # 同時讓TestCase紀錄可殺死的FOM
            testcase_killed_dict['AST_FOM_TestCase_Result_Folder_' + killed_testcase_name].append(fom_name)
        # 如果沒有測試案例可殺死
        if(len(temp_FOM_killed_testcase_after[fom_name]) < 1):
            temp_FOM_killed_testcase_after[fom_name].append('No')

    return temp_FOM_killed_testcase_after,testcase_killed_dict

# 寫入各個FOM可以殺死自己的測試案例(dir:輸出殺死FOM的測試案例的路徑 , FOM_killed_testcase_before:殺死各個FOM的TestCase(轉化前))
def write_killed_testcase(dir,FOM_killed_testcase_after):
    for name,killed in FOM_killed_testcase_after.items():
        file_dir = dir + '/' + name + '.txt'
        f = open(file_dir, 'w+', encoding='UTF-8')
        f.write(','.join(map(str, killed)))
        f.seek(0)
        f.close()
    return None


# 寫入各個測試案例可以殺死的FOM(dir:輸出測試案例殺死FOM的路徑,testcase_killed_dict:各個TestCase殺死FOM的字典)
def write_killed_fom(dir,testcase_killed_dict):
    for name, killed in testcase_killed_dict.items():
        file_name = name.replace('AST_FOM_TestCase_Result_Folder_','AST_TestCase_')
        file_dir = dir + '/' + file_name + '.txt'
        f = open(file_dir, 'w+', encoding='UTF-8')
        f.write(','.join(map(str, killed)))
        f.seek(0)
        f.close()


# 寫入FOM的Fragility
def write_report(fragility_dict,dir):
    # 檔案數量
    file_count = 0
    # 計算檔案數量
    for file_name in os.listdir(dir):
        file_count = file_count + 1


    # Fragility not zero count
    fra_not_zeor_count = 0
    # Fragility not zero sum
    fra_not_zeor_sum = 0.0
    #'FOM_Report' + str(file_count+1)
    with open(dir + 'Triangle_Extend_FOM.txt','w+',encoding='utf-8') as f:
        for name,value in fragility_dict.items():
            f.write('{:<15}'.format(name)+'\n')
        for name, value in fragility_dict.items():
            f.write('{:<.3f}'.format(value)+'\n')
            if(value>0.0 and value<1.0):
                fra_not_zeor_count = fra_not_zeor_count + 1
                fra_not_zeor_sum = fra_not_zeor_sum + value

        # 包含Equival, Dumb
        f.write('{:<20}'.format('Average(Non-Trial, Equivalent, Dumb)')+'\n')
        # 包含Equival, Dumb
        f.write('{:<.5f}'.format(sum(fragility_dict.values()) / len(fragility_dict.keys()))+'\n')
        # 不包含Equival, Dumb
        f.write('{:<20}'.format('Average(Non-Trial)') + '\n')
        try:
            # 不包含Equival, Dumb
            f.write('{:<.5f}'.format((fra_not_zeor_sum / fra_not_zeor_count)) + '\n')
        except ZeroDivisionError:
            f.write('{:<.5f}'.format(0) + '\n')


    return 'Write Report Done.'

# 寫入測試案例的變異分數
def write_testcase_report(mutationscore_dict,dir):
    # 檔案數量
    file_count = 0
    # 計算檔案數量
    for file_name in os.listdir(dir):
        file_count = file_count + 1


    # Fragility not zero count
    fra_not_zeor_count = 0
    # Fragility not zero sum
    fra_not_zeor_sum = 0.0

    with open(dir + 'Fibonacci_Number_Test.txt','w+',encoding='utf-8') as f:
        for name,value in mutationscore_dict.items():
            f.write('{:<15}'.format(name)+'\n')
        for name, value in mutationscore_dict.items():
            f.write('{:<.3f}'.format(len(value))+'\n')


    return 'Write Report Done.'


# 生成全部的測試案例代號
def create_testcase_codename(number):
    temp_T = []

    for i in range(1,number+1):
        temp_T.append(str(i))

    return temp_T

# 計算Fragility
# Fragility = kill(M) / T
# kill(M) => 可殺掉變異體(FOM、HOM)的測試案例
# all_testcase => 全部測試案例
# killed_T => 可殺掉變異體(FOM、HOM)的測試案例
def cal_fragility(killed_T,all_testcase):
    # 最終Fragility
    fra = 0.0
    # 可殺掉變異體(FOM、HOM)的測試案例數量
    killed_T_value = 0.0

    #方式二:計算測試案例的數量
    if(len(killed_T) == 0 or killed_T[0] == 'No'):
        fra = 0.0 / len(all_testcase)
    else:
        fra = len(killed_T) / len(all_testcase)

    return fra



# 寫入FOM報告(non_trial:部份被殺死的FOM的數量,equival:完全沒被殺死的FOM的數量,dumb:全部被殺死的FOM的數量)
def do_report(non_trial,equival,dumb):
    report_file = 'report' + '.txt'
    f_report = open(report_file,'a+',encoding='utf-8')
    f_report.write('Fibonacci Number 50\n' + str(non_trial) + '  ' + str(equival) + '  '  + str(dumb) + '\n')
    f_report.seek(0)
    f_report.close()


# --------------------------------------------------------------------
# 執行
# --------------------------------------------------------------------

# 取得TestCase測試結果目錄
get_root_dir(root_fom_dir,root_testcase_dir)

# 取得TestCase測試結果目錄的檔名
get_file_dir(file_dir)

# 測試結果目錄
get_testcase_result(file_dir)

# 印出測試結果
print('......Pass')
print(FOM_pass_dict)
print()

print('......Fail')
print(FOM_fail_dict)
print()

# --------------------------------------------------------------------
# 篩選
# --------------------------------------------------------------------
filter_FOM(FOM_name_list,FOM_pass_dict,FOM_fail_dict,FOM_possible_part,FOM_possible_equivalent,FOM_possible_dumb)

# --------------------------------------------------------------------
# 印出訊息
# --------------------------------------------------------------------
print('......FOM_possible_part')
print(len(FOM_possible_part))
print(FOM_possible_part)
print()

print('......FOM_possible_equivalent')
print(len(FOM_possible_equivalent))
print(FOM_possible_equivalent)
print()

print('......FOM_possible_dumb')
print(len(FOM_possible_dumb))
print(FOM_possible_dumb)
print()

# --------------------------------------------------------------------
# 轉化殺死各個FOM的字典
# --------------------------------------------------------------------
T = create_testcase_codename(30)

FOM_killed_testcase_after,testcase_killed_dict = convert_FOM_killed_testcase(FOM_killed_testcase_before,testcase_killed_dict)
print('......各個FOM可以殺死自己的測試案例')
for name, killed in FOM_killed_testcase_after.items():
        print(name, '  ', len(killed), killed)
        FOM_Fragility[name] = 0.0
        FOM_Fragility[name] = cal_fragility(killed,T)

write_report(FOM_Fragility,report_dir)


print('......各個測試案例可以殺死的FOM')
for name,value in testcase_killed_dict.items():
    print(name,'  ', len(value),value,'  ')

write_testcase_report(testcase_killed_dict,report_dir)


# --------------------------------------------------------------------
# 寫入各個測試案例可以殺死的FOM
# --------------------------------------------------------------------
write_killed_testcase(fom_killed_testcase_dir,FOM_killed_testcase_after)

# --------------------------------------------------------------------
# 寫入各個FOM可以殺死自己的測試案例
# --------------------------------------------------------------------
write_killed_fom(test_killed_fom_dir,testcase_killed_dict)


# --------------------------------------------------------------------
# 寫入這次的FOM報告
# --------------------------------------------------------------------
do_report(len(FOM_possible_part),len(FOM_possible_equivalent),len(FOM_possible_dumb))
