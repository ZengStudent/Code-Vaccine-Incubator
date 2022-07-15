import os


# ====================================================================
# 宣告變數
# ====================================================================





# filter all none-testcase(完全沒被殺死)
HOM_possible_equivalent = {}
# filter all testcase(全部被殺死)
HOM_possible_dumb = {}
# filter all part-testcase(部分殺死)
HOM_possible_part = {}

# 測試結果(Pass)
HOM_pass_dict = {}
# 測試結果(Fail)
HOM_fail_dict = {}
# 測試結果目錄的檔名
HOM_name_list = []

# 殺死各個HOM的TestCase(轉化前)
HOM_killed_testcase_before = {}
# 殺死各個HOM的TestCase(轉化後)
HOM_killed_testcase_after = {}

# 根目錄
root_dir = 'AST_TestCase_Result_Folder/AST_HOM_TestCase_Result_Folder/'
# 組別資料夾
trail_dir = []
# TestCase測試結果目錄
file_dir = []

# 殺死各個HOM的TestCase(轉化前)
HOM_killed_testcase_before = {}
# 殺死各個HOM的TestCase(轉化後)
HOM_killed_testcase_after = {}

# 輸出殺死FOM的測試案例的路徑
hom_killed_testcase_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_HOM_Killed_TestCase_Folder/'



# ====================================================================
# 宣告副程式
# ====================================================================


# 取得AST_HOM_TestCase_Result_Folder底下的測試結果資料夾
def get_trail_dir(root_dir,trail_dir):
    for name in os.listdir(root_dir):
        if (os.path.isdir(root_dir + name)):
            trail_dir.append(root_dir + name + '/')

# 取得組別資料夾
def get_file_dir(trail_dir,file_dir):
    temp_file_dir = []
    for trail in trail_dir:
        for name in os.listdir(trail):
            temp_file_dir.append(trail + name)
        file_dir.append(temp_file_dir)
        temp_file_dir = []

# 取得測試結果檔名
def get_file(file_dir):
    order = 1
    for file_dir_name in file_dir:
       for file_name in file_dir_name:
            if(os.path.isdir(file_name) == False): continue
            for name in os.listdir(file_name):
                _position = file_name.rfind('_') + 1
                if ('.txt' in name):
                    # 去除.txt
                    name = file_name[_position:]  +'/'+ name[:-4]
                    # 建立測試結果(Pass)字典
                    HOM_pass_dict[name] = 0
                    # 建立測試結果(Fail)字典
                    HOM_fail_dict[name] = 0
                    # 建立殺死各個FOM的字典
                    HOM_killed_testcase_before[name] = []
                    # 建立測試結果目錄的檔名
                    HOM_name_list.append(name)
            #
            order = order + 1
       order = 1

# 取得測試結果
def get_testcase_result(file_dir):
    order = 1
    for file_dir_name in file_dir:
        for file_name in file_dir_name:
            if (os.path.isdir(file_name) == False):
                continue
            # TestCase測試結果路徑底下全部檔名
            test_result_name = os.listdir(file_name)
            for name in test_result_name:
                _position = file_name.rfind('_') + 1
                if ('.txt' in name):
                    with open(file_name[:_position] + str(order) + '/' + name, 'r') as file:
                        result = file.readline()
                        if (result == 'Pass'):
                            # 去除.txt
                            name = file_name[_position:] + '/' + name[:-4]
                            HOM_pass_dict[name] = HOM_pass_dict[name] + 1
                        elif (result == 'Fail'):
                            # 去除.txt
                            name = file_name[_position:] + '/' + name[:-4]
                            HOM_fail_dict[name] = HOM_fail_dict[name] + 1
                            # 紀錄殺死各個HOM的TestCase
                            testname = file_name[:_position-1]
                            #print(testname[testname.rfind('_')+1:])
                            HOM_killed_testcase_before[name].append(testname[testname.rfind('_')+1:])
                        elif (result == '-'):
                            # 去除.txt
                            name = file_name[_position:] + '/' + name[:-4]
                            HOM_fail_dict[name] = HOM_fail_dict[name] + 1
                            # 紀錄殺死各個HOM的TestCase
                            testname = file_name[:_position - 1]
                            # print(testname[testname.rfind('_')+1:])
                            HOM_killed_testcase_before[name].append(testname[testname.rfind('_') + 1:])
                        elif (result == 'infiniteloop'):
                            # 去除.txt
                            name = file_name[_position:] + '/' + name[:-4]
                            HOM_fail_dict[name] = HOM_fail_dict[name] + 1
                            # 紀錄殺死各個HOM的TestCase
                            testname = file_name[:_position - 1]
                            # print(testname[testname.rfind('_')+1:])
                            HOM_killed_testcase_before[name].append(testname[testname.rfind('_') + 1:])
                        else:
                            print(file_name, name, 'Err')
            #
            order = order + 1
        order = 1

# 篩選
def filter_HOM():
    for name in HOM_name_list:
        # (部分殺死)
        if (HOM_pass_dict[name] >= 1 and HOM_fail_dict[name] >= 1):
            #HOM_possible_part.append(name.replace('_HOM_TestCase_Result_', '_HOM_'))
            HOM_possible_part[name.replace('_HOM_TestCase_Result_', '_HOM_')] = 0
            continue
        # (完全沒被殺死)
        elif (HOM_pass_dict[name] >= 1 and HOM_fail_dict[name] <= 0):
            #HOM_possible_equivalent.append(name.replace('_HOM_TestCase_Result_', '_HOM_'))
            HOM_possible_equivalent[name.replace('_HOM_TestCase_Result_', '_HOM_')] = 0
            continue
        # (全部被殺死)
        elif (HOM_pass_dict[name] <= 0 and HOM_fail_dict[name] >= 1):
            #HOM_possible_dumb.append(name.replace('_HOM_TestCase_Result_', '_HOM_'))
            HOM_possible_dumb[name.replace('_HOM_TestCase_Result_', '_HOM_')] = 0
            continue

# 轉化殺死各個HOM的字典
def convert_HOM_killed_testcase():
    # 暫存殺死各個HOM的TestCase(轉化後)
    temp_HOM_killed_testcase_after = {}

    # 轉化殺死各個HOM的字典
    for name, killed in HOM_killed_testcase_before.items():
        # 組別
        _leftposition = 0
        # 編號
        _rightposition = 0
        # 改名
        hom_name = name.replace('/AST_HOM_TestCase_Result_', '_HOM_')
        _leftposition = hom_name.find('_')
        _rightposition = hom_name.rfind('_')
        hom_name = 'HOM_' + hom_name[:_leftposition] + '_' + hom_name[_rightposition+1:]
        temp_HOM_killed_testcase_after[hom_name] = killed

    return temp_HOM_killed_testcase_after

# 寫入各個HOM可以殺死自己的測試案例
def write_killed_testcase(dir,HOM_killed_testcase_after):

    for name,killed in HOM_killed_testcase_after.items():
        _leftposition = name.find('_')
        _rightposition = name.rfind('_')
        trial_dir = dir + ('AST_HOM_Killed_TestCase_Folder_' + name[_leftposition+1:_rightposition])
        #print(name,'  ',name[_leftposition+1:_rightposition],name[_rightposition:])

        # 建立組別資料夾
        if (os.path.isdir(trial_dir) == False):
            os.mkdir(trial_dir)
        # 寫入
        file_dir = trial_dir + '/' + name + '.txt'
        f = open(file_dir, 'w+', encoding='UTF-8')
        f.write(','.join(map(str, killed)))
        f.seek(0)
        f.close()

    return None

#
def do_report(non_trial,equival,dumb):
    report_file = 'report' + '.txt'
    f_report = open(report_file,'a+',encoding='utf-8')
    f_report.write( str(non_trial) + '  ' + str(equival) + '  '  + str(dumb) + '\n')
    f_report.seek(0)
    f_report.close()



# ====================================================================
# 執行
# ====================================================================


get_trail_dir(root_dir,trail_dir)

get_file_dir(trail_dir,file_dir)

get_file(file_dir)

print('HOM_pass_dict: \n',HOM_pass_dict)
print('HOM_fail_dict: \n',HOM_fail_dict)
print('HOM_test_result_name_list: \n',len(HOM_name_list))


get_testcase_result(file_dir)


# 印出測試結果
print('......Pass')
print(HOM_pass_dict)
print()

print('......Fail')
print(HOM_fail_dict)
print()

filter_HOM()

print('......HOM_possible_part(HOM被部分測試案例殺死)')
print(len(HOM_possible_part))
print(HOM_possible_part)
print()

print('......HOM_possible_equivalent(HOM完全沒被測試案例殺死)')
print(len(HOM_possible_equivalent))
print(HOM_possible_equivalent)
print()

print('......HOM_possible_dumb(HOM被全部測試案例殺死)')
print(len(HOM_possible_dumb))
print(HOM_possible_dumb)
print()

for name, killed in HOM_killed_testcase_before.items():
        print(name,'  ',killed)

# 轉化殺死各個HOM的字典
HOM_killed_testcase_after = convert_HOM_killed_testcase()
print('......各個HOM可以殺死自己的測試案例')
for name, killed in HOM_killed_testcase_after.items():
        print(name, '  ', killed)
# 寫入
write_killed_testcase(hom_killed_testcase_dir,HOM_killed_testcase_after)



do_report(len(HOM_possible_part),len(HOM_possible_equivalent),len(HOM_possible_dumb))







