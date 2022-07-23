import os,shutil
import itertools

# ====================================================================
# 宣告變數
# ====================================================================

# 全部的測試案例
T = []

# 殺死FOM的測試案例資料夾路徑
FOM_killed_testcase_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_FOM_Killed_TestCase_Folder/'
# 殺死FOM的測試案例字典
FOM_killed_testcase = {}

# 殺死HOM的測試案例資料夾路徑
HOM_killed_testcase_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_HOM_Killed_TestCase_Folder/'
# 殺死HOM的測試案例字典
HOM_killed_testcase = {}

# 組成HOM的FOM資料夾路徑
HOM_material_dir = 'AST_Mutant_Folder/AST_HOM_Material_Folder/'
# 組成HOM的FOM字典
HOM_material = {}

# HOM類別的資料夾路徑
HOM_classification_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/'


# 輸出報告路徑
report_dir = 'AST_Report_Folder/AST_HOM_Report_Folder/'

# HOM的Name List
HOM_Name = []
# HOM的Fragility字典(Name=HOM名稱,Key=Fitness)
HOM_fra = {}
# HOM的Fitness字典(Name=HOM名稱,Key=Fitness)
HOM_fit = {}

# SHOM字典(Name=SHOM名稱,Key=Fitness)
SHOM_dict = {}

# SHOM
SHOM = []
# SSHOM
SSHOM = []
# WSHOM(Coupled)
WSHOM_Coupled = []
# WSHOM(Decoupled)
WSHOM_Decoupled = []
# NSHOM
NSHOM = []
# Equivalent SHOM
Equivalent_SHOM = []
# Useless SHOM
Useless_SHOM = []

# ====================================================================
# 宣告變數(Data Analysic)
# ====================================================================
# 資料分析用的HOM資料
HOM_Data = {}

# Scatter Marker
Scatter_Marker = itertools.cycle((".","^","1","3","4","s","p","P","*","h","H","+","x","D","_"))


# 生成全部的測試案例代號
def create_testcase_codename(number):
    temp_T = []

    for i in range(1,number+1):
        temp_T.append(str(i))

    return temp_T

# ====================================================================
# 宣告副程式
# ====================================================================

# 讀取HOM Material(dir:組成HOM的FOM資料夾路徑)
def read_hom_material(dir):
    # 每一個組別的資料夾路徑
    trial_dir = []
    # 每個HOM所組成的FOM(Name=HOM名稱,Key=所組成的FOM)
    temp_material = {}
    # 暫存一個組別內所有HOM的名稱
    temp_name = ''

    # 讀取每一個組別的資料夾路徑
    for name in os.listdir(dir):
        if (os.path.isdir(dir+name)):
            trial_dir.append(dir+name)

    # 從每一個組別的資料夾開始
    for dir_name in trial_dir:
        # 組別資料內的資料
        for file_name in os.listdir(dir_name):
            # 如果為.txt檔案
            if('.txt' in file_name):
                # 讀取位置
                file_dir = dir_name + '/' + file_name
                # 開啟檔案
                f = open(file_dir, 'r', encoding='UTF-8')
                # 改名，更改為和HOM同名
                #temp_name = file_dir.replace('AST_Mutant_Folder/AST_HOM_Material_Folder/AST_HOM_Material_Folder_', '')
                #temp_name = temp_name.replace('/AST_HOM_Material_', '_HOM_')
                # 放入HOM所組成的FOM
                temp_material[str(file_name)[:-4]] = eval(f.read())
                f.seek(0)
                f.close()

    return temp_material

# 讀取TestCase of Killed FOM(dir:殺死FOM的測試案例資料夾路徑)
def read_fom_killed_testcase(dir):

    # 每個FOM可殺死自己測試案例(Name=FOM名稱,Key=殺死自己的測試案例)
    temp_killed_testcase = {}

    # 資料內的資料
    for file_name in os.listdir(dir):
            # 如果為.txt檔案
            if ('.txt' in file_name):
                # 讀取位置
                file_dir = dir + file_name
                # 開啟檔案
                f = open(file_dir, 'r', encoding='UTF-8')
                # 讀取測試案例
                read_result = f.read()
                # 如果有測試案例
                if(read_result != 'No'):
                    temp_killed_testcase[file_name[:-4]] = read_result.split(',')
                # 如果沒有測試案例
                else:
                    temp_killed_testcase[file_name[:-4]] = 'No'
                f.seek(0)
                f.close()

    return temp_killed_testcase

# 讀取TestCase of Killed HOM(dir:殺死HOM的測試案例資料夾路徑)
def read_hom_killed_testcase(dir):

    # 每一個組別的資料夾路徑
    trial_dir = []
    # 每個HOM可殺死自己測試案例(Name=HOM名稱,Key=殺死自己的測試案例)
    temp_killed_testcase = {}

    # 讀取每一個組別的資料夾路徑
    for name in os.listdir(dir):
        if (os.path.isdir(dir + name)):
            trial_dir.append(dir + name)

    # 從每一個組別的資料夾開始
    for dir_name in trial_dir:
        # 組別資料內的資料
        for file_name in os.listdir(dir_name):
            # 如果為.txt檔案
            if ('.txt' in file_name):
                # 讀取位置
                file_dir = dir_name + '/' + file_name
                # 開啟檔案
                f = open(file_dir, 'r', encoding='UTF-8')
                # 讀取測試案例
                read_result = f.read()
                # 如果有測試案例
                if (read_result != 'No'):
                    temp_killed_testcase[file_name[:-4]] = read_result.split(',')
                # 如果沒有測試案例
                else:
                    temp_killed_testcase[file_name[:-4]] = 'No'
                f.seek(0)
                f.close()

    return temp_killed_testcase

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

    #方式一:找出相同的測試案例
    # for i in killed_T:
    #     for j in all_testcase:
    #         if(i==j):
    #             killed_T_value = killed_T_value + 1.0
    #             break

    #方式二:計算測試案例的數量
    if(killed_T == '' or killed_T == 'No'):
        fra = 0.0 / len(all_testcase)
    else:
        fra = len(killed_T) / len(all_testcase)

    return fra

# 計算Fitness
# Fitness = Fragility(M) / Fragility(F)
# M => HOM
# F => 組成M的FOM
# hom_killed => 可殺死此HOM的測試案例
# fom_material => 組成此HOM的FOM
# fom_killed => 殺死此FOM的測試案例
# all_testcase =>  全部測試案例
def cal_fitness(hom_killed,fom_material,fom_killed,all_testcase):
    # 最終Fitness
    fit = 0.0
    # 組成HOM的所有FOM的【Fragility的平均】
    fom_material_fra = 0.0

    # 計算HOM自身的fragility
    hom_fra = cal_fragility(hom_killed,all_testcase)


    # 計算組成此HOM的FOM的fragility
    for material in fom_material:
        file_name = 'AST_FOM_' + str(material[-1])
        fom_material_fra = fom_material_fra + cal_fragility(fom_killed[file_name],all_testcase)
    # 取平均
    fom_material_fra = fom_material_fra / len(fom_material)
    HOM_fra[name] = fom_material_fra

    # 結果
    print('hom_fra: ',hom_fra)
    print('fom_material_fra: ',fom_material_fra)

    # 計算最終Fitness
    try :
        fit = hom_fra / fom_material_fra
    except ZeroDivisionError:
        fit = 0.0
    return fit


# 寫入HOM的Fragility
def write_fragility_report(fragility_dict,dir):
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
    with open(dir + 'Triangle_Fragility_HOM.txt','w+',encoding='utf-8') as f:
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

# 寫入HOM的Fitness
def write_fitness_report(fitness_dict,dir):
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
    with open(dir + 'Triangle_Fitness_HOM.txt','w+',encoding='utf-8') as f:
        for name,value in fitness_dict.items():
            f.write('{:<15}'.format(name)+'\n')
        for name, value in fitness_dict.items():
            f.write('{:<.3f}'.format(value)+'\n')
            if(value>0.0 and value<1.0):
                fra_not_zeor_count = fra_not_zeor_count + 1
                fra_not_zeor_sum = fra_not_zeor_sum + value
    return 'Write Report Done.'




# 搜尋SHOM(undirected search)，(fit_dict:所有HOM的Fitness,fit:目標Fitness)
def search_SHOM_undirected(fit_dict,fit):

    temp_SHOM = {}

    for name,value in fit_dict.items():
        if(value <= fit):
            temp_SHOM[name] = value

    return temp_SHOM

# 搜尋SHOM(Genetic Algorithm)，(fit_dict:所有HOM的Fitness,fitness_value,fom_material)
def search_SHOM_GA(fit_dict,fitness_value,fom_material):

    temp_SHOM = {}

    # 各Trail的Fitness平均
    trial_fitness = {}
    # selection
    trial_selection = {}

    # ------------------------------------------------------
    # 計算各Trail的Fitness平均
    # ------------------------------------------------------
    for name,value in fit_dict.items():
        trial_fitness[name[0]] = 0.0
    for name,value in fit_dict.items():
        trial_fitness[name[0]] = trial_fitness[name[0]] + value
    for name, value in trial_fitness.items():
        trial_fitness[name] = trial_fitness[name] / 10.0
    print(trial_fitness)

    # ------------------------------------------------------
    # Selection
    # ------------------------------------------------------
    # 競爭式選擇(Tournament Selection)
    if(len(trial_fitness)%2 == 0):
        print('偶數')
        for round in range(1,len(trial_fitness),2):
            if(trial_fitness[str(round)] > trial_fitness[str(round+1)]):
                trial_selection[str(round+1)] = trial_fitness[str(round+1)]
            elif(trial_fitness[str(round)] < trial_fitness[str(round+1)]):
                trial_selection[str(round)] = trial_fitness[str(round)]
            else:
                trial_selection[str(round)] = trial_fitness[str(round)]
    else:
        print('奇數')
        for round in range(1,len(trial_fitness),2):
            if(trial_fitness[str(round)] > trial_fitness[str(round+1)]):
                trial_selection[str(round+1)] = trial_fitness[str(round+1)]
            elif(trial_fitness[str(round)] < trial_fitness[str(round+1)]):
                trial_selection[str(round)] = trial_fitness[str(round)]
            else:
                trial_selection[str(round)] = trial_fitness[str(round)]

        trial_selection[len(trial_fitness)] = trial_fitness[str(len(trial_fitness))]


    print(trial_selection)


    #------------------------------------------------------
    # Crossover
    #------------------------------------------------------
    # 單點交配(one-point crossover method)

    # 同一trail進行crossover
    count = 1
    temp_hom = []
    temp_hom_list = []
    temp_hom_dict = {}

    for name, value in fom_material.items():
        if(name[0]=='2' or name[0]=='3' or name[0]=='5'):
            if (count % 2 == 0):
                temp_hom.append(name)
                temp_hom_dict[name] = value
                temp_hom_dict[temp_hom[0]][3:],temp_hom_dict[temp_hom[1]][3:] = temp_hom_dict[temp_hom[1]][3:],temp_hom_dict[temp_hom[0]][3:]
                temp_hom = []
                count = count + 1
            else:
                temp_hom.append(name)
                temp_hom_dict[name] = value
                count = count + 1

    count = 1

    for name, value in temp_hom_dict.items():
        print(name,'  ',value)
        path = 'AST_Mutant_Folder/AST_HOM_GA_Material_Folder/AST_HOM_GA_Material_Folder_' + name[0] + '/'
        # 新建資料夾
        if(os.path.isdir(path) == False):
            os.mkdir(path)

        # 寫入
        file_dir = path + 'AST_HOM_GA_Material_' + str(count) + '.txt'
        f = open(file_dir, 'w+')
        f.write(str(value))
        f.seek(0)
        f.close()
        count = count + 1
        if(count >10):count = 1

    # ------------------------------------------------------
    # Mutation
    # ------------------------------------------------------

    # 突變率以前面Selection步驟算出的Fitness為主
    # 定義突變率為2.2以下，發生突變
    # 突變位置則隨機
    # 突變的FOM也隨機


    return None

# 找出SHOM(轉成list)，(SHOM_dict:所有SHOM的Fitness)
def find_SHOM(SHOM_dict):

    temp_SHOM = []

    for name,value in SHOM_dict.items():
        temp_SHOM.append(name)

    return temp_SHOM

# 找出SSHOM(SHOM_dict:所有SHOM的Fitness,hom_killed:所有HOM可殺死自己的測試案例,fom_killed:所有FOM可殺死自己的測試案例,hom_material:組成HOM的FOM)
def find_SSHOM(SHOM_dict,hom_killed,fom_killed,hom_material):

    # 符合SSHOM的SHOM
    temp_SSHOM = []
    # 可殺死HOM的測試案例
    temp_hom_killed_set = set()
    # 組合成HOM的FOM的測試案例
    temp_fom_killed_setlist = []


    # 每個SHOM
    for name,value in SHOM_dict.items():
        # 重置
        temp_hom_killed_set = set()
        temp_fom_killed_setlist = []
        temp_result = []

        # 可殺死HOM的測試案例
        temp_hom_killed_set = set(hom_killed[name])
        # 組成此HOM的FOM的測試案例
        for material in hom_material[name]:
            file_name = 'AST_FOM_' + str(material[-1])
            temp_fom_killed_setlist.append(set(fom_killed[file_name]))

        # 判斷標準(以下都為True，則為SSHOM)
        # 條件1. 可殺死HOM的測試案例的集合不是空集合。
        is_notempty = False
        # 條件2. 可殺死HOM的測試案例的集合 是 組成此HOM的所有FOM的測試案例的交集的子集合
        is_subset = False

        # ------------------------------------------------------------------------
        # (條件1) 檢查HOM的測試案例是否為空集合
        # ------------------------------------------------------------------------
        # 如果為空集合，則不符合條件
        if (temp_hom_killed_set != set()):
            is_notempty = True
        else:
            # 下一個SHOM
            continue

        # ------------------------------------------------------------------------
        # (條件2) 檢查可殺死HOM的測試案例的集合 是 組成此HOM的所有FOM的測試案例的交集的子集合
        # ------------------------------------------------------------------------
        # 全部FOM測試案例的交集
        temp_result = temp_fom_killed_setlist[0]
        for killed_testcase in temp_fom_killed_setlist:
            temp_result = set(temp_result).intersection(killed_testcase)

        # HOM的測試案例是否屬於全部FOM測試案例的交集的子集合
        if (temp_hom_killed_set.issubset(temp_result) == True):
            is_subset = True
        else:
            continue

        # ------------------------------------------------------------------------
        # 如果符合，則視為SSHOM
        # ------------------------------------------------------------------------
        if(is_notempty == True and is_subset == True):
            temp_SSHOM.append(name)



    #print('SSHOM', len(temp_SSHOM),temp_SSHOM)
    return temp_SSHOM

# 找出WSHOM(Coupled)，(SHOM_dict:所有SHOM的Fitness,hom_killed:所有HOM可殺死自己的測試案例,fom_killed:所有FOM可殺死自己的測試案例,hom_material:組成HOM的FOM,all_testcase:全部測試案例)
def find_WSHOM_Coupled(SHOM_dict,hom_killed,fom_killed,hom_material,all_testcase):

    # 符合WSHOM的SHOM
    temp_WSHOM = []
    # 可殺死HOM的測試案例
    temp_hom_killed_set = set()
    # 組合成HOM的FOM的測試案例
    temp_fom_killed_setlist = []

    # 每個SHOM
    for name, value in SHOM_dict.items():

        # 重置
        temp_hom_killed_set = set()
        temp_fom_killed_setlist = []
        temp_result = []


        # 可殺死HOM的測試案例
        temp_hom_killed_set = set(hom_killed[name])
        # 組成此HOM的FOM的測試案例
        for material in hom_material[name]:
            file_name = 'AST_FOM_' + str(material[-1])
            temp_fom_killed_setlist.append(set(fom_killed[file_name]))

        # 判斷標準(以下都為True，則為WSHOM)
        # 條件1. HOM的測試案例不為空集合
        is_notempty = False
        # 條件2. 和每個FOM的測試案例都有交集
        is_every_intersection = True
        # 條件3. 全部測試案例和所有FOM的測試案例的連集的差集有交集
        is_differ = False
        # 條件4. HOM測試案例的數量 < 所有FOM的測試案例的連集的試案例的數量
        is_less_than = False

        # ------------------------------------------------------------------------
        # (條件1) 檢查HOM的測試案例是否為空集合
        # ------------------------------------------------------------------------
        # 如果為空集合，則不符合條件
        if(temp_hom_killed_set != set()):
            is_notempty = True
        else:
            # 下一個SHOM
            continue

        # ------------------------------------------------------------------------
        # (條件2) 檢查和每個FOM的測試案例是否都有交集
        # ------------------------------------------------------------------------
        for killed_testcase in temp_fom_killed_setlist:
            temp_result = killed_testcase

            # 如果和任一個FOM的測試案例沒有交集，則不符合條件
            if(temp_hom_killed_set.intersection(temp_result)==set()):
                is_every_intersection = False
                break


        # ------------------------------------------------------------------------
        # (條件3) 檢查全部測試案例和所有FOM的測試案例的連集的差集是否有交集
        # ------------------------------------------------------------------------
        # 如果前面的條件沒有符合，則下一個SHOM
        if(is_every_intersection == False):
            continue

        # 設置第一個，用於和其他的測試案例進行聯集
        temp_result = temp_fom_killed_setlist[0]
        # 所有FOM的測試案例的聯集
        for killed_testcase in temp_fom_killed_setlist:
            # 跟其他FOM測試案例進行聯集
            temp_result = temp_result.union(temp_result)


        # 檢查SHOM的測試案例和全部測試案例以及所有FOM的測試案例的連集的差集是否有交集
        # 如果沒有交集，則不符合條件
        if (temp_hom_killed_set.intersection(set(all_testcase).difference(temp_result)) == set()):
            # 下一個SHOM
            continue
        else:
            is_differ = True

        # ------------------------------------------------------------------------
        # (條件4) HOM測試案例的數量少於所有FOM的測試案例的連集的試案例的數量
        # ------------------------------------------------------------------------
        # 如果HOM測試案例的數量 >= 所有FOM的測試案例的連集的試案例的數量，則不符合條件
        if (len(temp_hom_killed_set) >= len(temp_result)):
            # 下一個SHOM
            continue
        else:
            is_less_than = True

        # ------------------------------------------------------------------------
        # 如果符合，則視為WSHOM
        # ------------------------------------------------------------------------
        if (is_notempty and is_every_intersection and is_differ and is_less_than):
            temp_WSHOM.append(name)

    #print('WSHOM(Coupled)',len(temp_WSHOM),temp_WSHOM)
    return temp_WSHOM

# 找出WSHOM(Decoupled)，(SHOM_dict:所有SHOM的Fitness,hom_killed:所有HOM可殺死自己的測試案例,fom_killed:所有FOM可殺死自己的測試案例,hom_material:組成HOM的FOM,all_testcase:全部測試案例)
def find_WSHOM_Deoupled(SHOM_dict,hom_killed,fom_killed,hom_material,all_testcase):

    # 符合WSHOM的SHOM
    temp_WSHOM = []
    # 可殺死HOM的測試案例
    temp_hom_killed_set = set()
    # 組合成HOM的FOM的測試案例
    temp_fom_killed_setlist = []

    # 每個SHOM
    for name, value in SHOM_dict.items():

        # 重置
        temp_hom_killed_set = set()
        temp_fom_killed_setlist = []
        temp_result = []


        # 可殺死HOM的測試案例
        temp_hom_killed_set = set(hom_killed[name])

        # 組成此HOM的FOM的測試案例
        for material in hom_material[name]:
            file_name = 'AST_FOM_' + str(material[-1])
            temp_fom_killed_setlist.append(set(fom_killed[file_name]))

        # 判斷標準(以下都為True，則為WSHOM)
        # 條件1. HOM的測試案例不為空集合
        is_notempty = False
        # 條件2. 和每個FOM的測試案例都沒有交集
        is_every_no_intersection = True
        # 條件3. 全部測試案例和所有FOM的測試案例的連集的差集有交集
        is_differ = False
        # 條件4. HOM測試案例的數量 < 所有FOM的測試案例的連集的試案例的數量
        is_less_than = False



        # ------------------------------------------------------------------------
        # (條件1) 檢查HOM的測試案例是否為空集合
        # ------------------------------------------------------------------------
        # 如果為空集合，則不符合條件
        if(temp_hom_killed_set != set()):
            is_notempty = True
        else:
            # 下一個SHOM
            continue

        # ------------------------------------------------------------------------
        # (條件2) 檢查和每個FOM的測試案例是否都沒有交集
        # ------------------------------------------------------------------------
        for killed_testcase in temp_fom_killed_setlist:
            temp_result = killed_testcase

            # 如果和任一個FOM的測試案例有交集，則不符合條件
            if(temp_hom_killed_set.intersection(temp_result)!=set()):
                is_every_no_intersection = False
                break

        # ------------------------------------------------------------------------
        # (條件3) 檢查全部測試案例和所有FOM的測試案例的連集的差集是否有交集
        # ------------------------------------------------------------------------
        # 如果前面的條件沒有符合，則下一個SHOM
        if(is_every_no_intersection == False):
            continue

        # 設置第一個，用於和其他的測試案例進行聯集
        temp_result = temp_fom_killed_setlist[0]
        # 所有FOM的測試案例的聯集
        for killed_testcase in temp_fom_killed_setlist:
            # 跟其他FOM測試案例進行聯集
            temp_result = temp_result.union(temp_result)

        # 檢查SHOM的測試案例和全部測試案例以及所有FOM的測試案例的連集的差集是否有交集
        # 如果沒有交集，則不符合條件
        if (temp_hom_killed_set.intersection(set(all_testcase).difference(temp_result)) == set()):
            # 下一個SHOM
            continue
        else:
            is_differ = True

        # ------------------------------------------------------------------------
        # (條件4) HOM測試案例的數量少於所有FOM的測試案例的連集的試案例的數量
        # ------------------------------------------------------------------------
        # 如果HOM測試案例的數量 >= 所有FOM的測試案例的連集的試案例的數量
        if(len(temp_hom_killed_set) >= len(temp_result)):
            # 下一個SHOM
            continue
        else:
            is_less_than = True


        # ------------------------------------------------------------------------
        # 如果符合，則視為WSHOM
        # ------------------------------------------------------------------------
        if (is_notempty and is_every_no_intersection and is_differ and is_less_than):
            temp_WSHOM.append(name)


    #print('WSHOM(Decoupled)',len(temp_WSHOM),temp_WSHOM)
    return temp_WSHOM

# 找出NSHOM，(SHOM_dict:所有SHOM的Fitness,hom_killed:所有HOM可殺死自己的測試案例,fom_killed:所有FOM可殺死自己的測試案例,hom_material:組成HOM的FOM,all_testcase:全部測試案例)
def find_NSHOM(SHOM_dict,hom_killed,fom_killed,hom_material,all_testcase):
    # 符合NSHOM的SHOM
    temp_NSHOM_list = []
    # 可殺死HOM的測試案例
    temp_hom_killed_set = set()
    # 組合成HOM的FOM的測試案例
    temp_fom_killed_setlist = []

    # 每個SHOM
    for name, value in SHOM_dict.items():

        # 重置
        temp_hom_killed_set = set()
        temp_fom_killed_setlist = []
        temp_result = []

        # 可殺死HOM的測試案例
        temp_hom_killed_set = set(hom_killed[name])
        # 組成此HOM的FOM的測試案例
        for material in hom_material[name]:
            file_name = 'AST_FOM_' + str(material[-1])
            temp_fom_killed_setlist.append(set(fom_killed[file_name]))

        # 判斷標準(以下都為True，則為NSHOM)
        # 條件1. HOM的測試案例不為空集合
        is_notempty = False
        # 條件2. 和每個FOM的測試案例都沒有交集
        is_every_no_intersection = True
        # 條件3. 全部測試案例和所有FOM的測試案例的連集的差集有交集
        is_differ = False
        # 條件4. HOM測試案例的數量 >= 所有FOM的測試案例的連集的試案例的數量
        is_greater_than = False

        # ------------------------------------------------------------------------
        # (條件1) 檢查HOM的測試案例是否為空集合
        # ------------------------------------------------------------------------
        # 如果為空集合，則不符合條件
        if (temp_hom_killed_set != set()):
            is_notempty = True
        else:
            # 下一個SHOM
            continue

        # ------------------------------------------------------------------------
        # (條件2) 檢查和每個FOM的測試案例是否都沒有交集
        # ------------------------------------------------------------------------
        for killed_testcase in temp_fom_killed_setlist:
            temp_result = killed_testcase

            # 如果和任一個FOM的測試案例有交集，則不符合條件
            if (temp_hom_killed_set.intersection(temp_result) != set()):
                is_every_no_intersection = False
                break

        # ------------------------------------------------------------------------
        # (條件3) 檢查全部測試案例和所有FOM的測試案例的連集的差集是否有交集
        # ------------------------------------------------------------------------
        # 如果前面的條件沒有符合，則下一個SHOM
        if (is_every_no_intersection == False):
            continue

        # 設置第一個，用於和其他的測試案例進行聯集
        temp_result = temp_fom_killed_setlist[0]
        # 所有FOM的測試案例的聯集
        for killed_testcase in temp_fom_killed_setlist:
            # 跟其他FOM測試案例進行聯集
            temp_result = temp_result.union(temp_result)

        # 檢查SHOM的測試案例和全部測試案例以及所有FOM的測試案例的連集的差集是否有交集
        # 如果沒有交集，則不符合條件
        if (temp_hom_killed_set.intersection(set(all_testcase).difference(temp_result)) == set()):
            # 下一個SHOM
            continue
        else:
            is_differ = True

        # ------------------------------------------------------------------------
        # (條件4) HOM測試案例的數量少於所有FOM的測試案例的連集的試案例的數量
        # ------------------------------------------------------------------------
        # 如果HOM測試案例的數量 < 所有FOM的測試案例的連集的試案例的數量
        if (len(temp_hom_killed_set) < len(temp_result)):
            # 下一個SHOM
            continue
        else:
            is_greater_than = True

        # ------------------------------------------------------------------------
        # 如果符合，則視為NSHOM
        # ------------------------------------------------------------------------
        if (is_notempty and is_every_no_intersection and is_differ and is_greater_than):
            temp_NSHOM_list.append(name)

    #print('NSHOM', len(temp_NSHOM_list), temp_NSHOM_list)
    return temp_NSHOM_list

# 找出 Equivalent(NSHOM-Decoupled)，(SHOM_dict:所有SHOM的Fitness,hom_killed:所有HOM可殺死自己的測試案例)
def find_Equivalent_SHOM(SHOM_dict,hom_killed):
    # 符合Equivalent的SHOM
    temp_Equivalent = []
    # 可殺死HOM的測試案例
    temp_hom_killed_set = set()

    # 每個SHOM
    for name, value in SHOM_dict.items():
        # 重置
        temp_hom_killed_set = set()
        temp_fom_killed_setlist = []

        # 可殺死HOM的測試案例
        temp_hom_killed_set = set(hom_killed[name])

        # 判斷標準(以下都為True，則為WSHOM)
        # 條件1. HOM的測試案例為空集合
        is_empty = False

        # ------------------------------------------------------------------------
        # (條件1) 檢查HOM的測試案例是否為空集合
        # ------------------------------------------------------------------------
        # 如果不為空集合，則不符合條件
        if (temp_hom_killed_set != set()):
            # 下一個SHOM
            continue
        else:
            is_empty = True

        # ------------------------------------------------------------------------
        # 如果符合，則視為Equivalent
        # ------------------------------------------------------------------------
        if (is_empty):
            temp_Equivalent.append(name)

    #print('temp_Equivalent', len(temp_Equivalent), temp_Equivalent)
    return temp_Equivalent

# 找出 Useless(NSHOM-Coupled)，(SHOM_list:所有的SHOM,SSHOM_list:所有的SSHOM,WSHOM_Coupled_list:所有的WSHOM(Coupled),WSHOM_Decoupled_list:所有的WSHOM(Decoupled),NSHOM_lsit:所有的NSHOM,Equivalent_SHOM_lsit:所有的Equivalent SHOM)
def find_Useless_SHOM(SHOM_list,SSHOM_list,WSHOM_Coupled_list,WSHOM_Decoupled_list,NSHOM_lsit,Equivalent_SHOM_lsit):

    # 符合Useless的SHOM
    temp_Useless_SHOM = set()

    # 判斷標準(以下都為True，則為Useless)
    # 條件1. 不為前面5種的SHOM

    # ------------------------------------------------------------------------
    # (條件1)不為前面5種的SHOM
    # ------------------------------------------------------------------------
    # 符合Useless的SHOM
    # SHOM和另外5種集合的聯集的差集
    temp_Useless_SHOM = set(SHOM_list).difference(set(SSHOM_list).union(set(WSHOM_Coupled_list),set(WSHOM_Decoupled_list),set(NSHOM_lsit),set(Equivalent_SHOM_lsit)))

    # 轉換為list
    temp_Useless_SHOM = list(temp_Useless_SHOM)
    # 排序
    temp_Useless_SHOM.sort()

    return temp_Useless_SHOM

# 寫入分類後的HOM(classification_list:要寫入的HOM類別的List,classification_dir:HOM類別的資料夾路徑,classification:要寫入的HOM類別)
def write_hom_classification(classification_list,classification_dir,classification):

    # 類別資料夾路徑
    dir = classification_dir + 'AST_' + classification + '_Folder/'
    # 單一類別資料夾路徑
    single_dir = 'AST_' + classification + '_Folder_'
    # 組別資料夾路徑
    trial_dir = ''
    # 所有HOM的資料夾路徑
    hom_dir = 'AST_Mutant_Folder/AST_HOM_Folder/AST_HOM_Folder_'
    # 組別'_'的位置，用於找出組別
    _leftposition = 0
    # 編號'_'的位置，用於找出編號
    _rightposition = 0
    # 寫入位置
    file_dir = ''
    # 複製檔案位置
    copy_file_dir = ''

    # 將分類後的HOM一一放入
    for hom in classification_list:
        # -------------------------------------------
        # 找出組別、編號
        # EX.'1_HOM_4','2_HOM_3'
        # -------------------------------------------
        # 在此之前為組別
        _leftposition = hom.find('_')
        # 在此之前為編號
        _rightposition = hom.rfind('_')
        #print(hom,hom[_leftposition+1],hom[_rightposition+1:])

        # -------------------------------------------
        # 新建組別資料夾
        # -------------------------------------------
        trial_dir = dir + single_dir + hom[_leftposition+1:_rightposition]
        #print(trial_dir)
        if (os.path.isdir(trial_dir) == False):
            os.mkdir(trial_dir)

        # -------------------------------------------
        # 寫入code(.py) copyfile()
        # 從所有HOM的資料夾複製檔案
        # -------------------------------------------
        # 複製位置
        copy_file_dir = hom_dir + hom[_leftposition+1:_rightposition] + '/HOM_' + hom[_leftposition + 1:] + '.py'
        # 寫入位置
        file_dir = dir + single_dir + hom[_leftposition+1:_rightposition] + '/' + hom +'.py'

        shutil.copyfile(copy_file_dir,file_dir)
        #print(file_dir,'  ',copy_file_dir)

    # -------------------------------------------
    # 寫入名單(.txt)
    # -------------------------------------------
    # 寫入位置
    file_dir = dir + classification +'_NameList'+ '.txt'
    f = open(file_dir, 'w+', encoding='UTF-8')
    f.write('\n'.join(map(str, classification_list)))
    f.seek(0)
    f.close()

    return None

# 生成HOM Data
def create_HOM_Data(hom_name,hom_fra,hom_fit):
    _leftposition = 0
    _rightposition = 0

    temp_HOM_Data = {}

    HOM_Data_CHILD = {
        'name': '',
        'fra': 0.0,
        'fit': 0.0,
        'trials': ''
    }

    for name in hom_name:
        _leftposition = name.find('_')
        _rightposition = name.rfind('_')

        HOM_Data_CHILD['name'] = name
        HOM_Data_CHILD['fra'] = hom_fra[name]
        HOM_Data_CHILD['fit'] = hom_fit[name]
        HOM_Data_CHILD['trials'] = name[_leftposition + 1:_rightposition]

        temp_HOM_Data[name] = dict(HOM_Data_CHILD)


    return temp_HOM_Data

#
def do_report(SHOM_len,SSHOM_len,WSHOM_C_len,WSHOM_De_len,NSHOM_len,Equivalent_SHOM_len,Useless_SHOM_len):
    report_file = 'report' + '.txt'
    f_report = open(report_file,'a+',encoding='utf-8')
    f_report.write(str(SHOM_len) + '  ' + str(SSHOM_len) + '  ' + str(WSHOM_C_len) + '  ' + str(WSHOM_De_len) + '  ' + str(NSHOM_len) +  '  ' + str(Equivalent_SHOM_len) + '  ' + str(Useless_SHOM_len) + '\n' + '===============' + '\n')
    f_report.seek(0)
    f_report.close()






# ====================================================================
# 執行
# ====================================================================

# ----------------------
# 生成全部的測試案例代號
# ----------------------
T = create_testcase_codename(30)


# ----------------------
# 取得每個HOM所組成的FOM
# ----------------------
HOM_material = read_hom_material(HOM_material_dir)
for name,value in HOM_material.items():
    # 取得HOM的name
    HOM_Name.append(name)
    print(name,'  ',type(value),'  ',len(value),'  ',value)

# ----------------------
# 取得每個FOM可以殺死自己的測試案例，並計算 Fragility
# ----------------------
FOM_killed_testcase = read_fom_killed_testcase(FOM_killed_testcase_dir)
for name,value in FOM_killed_testcase.items():
   print(name, ' ',value, ' ','Fra = ',cal_fragility(value,T))

# ----------------------
# 取得每個HOM可以殺死自己的測試案例，並計算 Fragility
# ----------------------
HOM_killed_testcase = read_hom_killed_testcase(HOM_killed_testcase_dir)
for name,value in HOM_killed_testcase.items():
    HOM_fra[name] = 0.0
    print(name,'  ',value, ' ','Fra = ',cal_fragility(value,T))
    # if(len(value)>=len(T)):
    #     print('\n\n\n')
    #     print(name)
    #     print('\n\n\n')
# ----------------------
# 取得每個HOM所組成的FOM，並計算 Fitness
# ----------------------
for name,value in HOM_killed_testcase.items():
    HOM_fit[name] = cal_fitness(value,HOM_material[name],FOM_killed_testcase,T)
    print(name,' ','Fit = ',HOM_fit[name])
    print()


write_fragility_report(HOM_fra,report_dir)
write_fitness_report(HOM_fit,report_dir)


# ----------------------
# 搜尋SHOM(undirected search)
# ----------------------
SHOM_dict = search_SHOM_undirected(HOM_fit,0.99)
print('SHOM: ',len(SHOM_dict),SHOM_dict)

print('..........')

# ----------------------
# 找出SHOM(轉成list)
# ----------------------
SHOM = find_SHOM(SHOM_dict)
print('SHOM ',len(SHOM),'\n',SHOM)
write_hom_classification(SHOM,HOM_classification_dir,'SHOM')

# ----------------------
# 找出SSHOM
# ----------------------
SSHOM = find_SSHOM(SHOM_dict,HOM_killed_testcase,FOM_killed_testcase,HOM_material)
print('SSHOM ',len(SSHOM),'\n',SSHOM)
write_hom_classification(SSHOM,HOM_classification_dir,'SSHOM')

# ----------------------
# 找出WSHOM(Coupled)
# ----------------------
WSHOM_Coupled = find_WSHOM_Coupled(SHOM_dict,HOM_killed_testcase,FOM_killed_testcase,HOM_material,T)
print('WSHOM(Coupled) ',len(WSHOM_Coupled),'\n',WSHOM_Coupled)
write_hom_classification(WSHOM_Coupled,HOM_classification_dir,'WSHOM_Coupled')

# ----------------------
# 找出WSHOM(Decoupled)
# ----------------------
WSHOM_Decoupled = find_WSHOM_Deoupled(SHOM_dict,HOM_killed_testcase,FOM_killed_testcase,HOM_material,T)
print('WSHOM(Decoupled) ',len(WSHOM_Decoupled),'\n',WSHOM_Decoupled)
write_hom_classification(WSHOM_Decoupled,HOM_classification_dir,'WSHOM_Decoupled')

# ----------------------
# 找出NSHOM
# ----------------------
NSHOM = find_NSHOM(SHOM_dict,HOM_killed_testcase,FOM_killed_testcase,HOM_material,T)
print('NSHOM ',len(NSHOM),'\n',NSHOM)
write_hom_classification(NSHOM,HOM_classification_dir,'NSHOM')

# ----------------------
# 找出Equivalent
# ----------------------
Equivalent_SHOM = find_Equivalent_SHOM(SHOM_dict,HOM_killed_testcase)
print('Equivalent SHOM ',len(Equivalent_SHOM),'\n',Equivalent_SHOM)
write_hom_classification(Equivalent_SHOM,HOM_classification_dir,'Equivalent_SHOM')

# ----------------------
# 找出Useless
# ----------------------
Useless_SHOM = find_Useless_SHOM(SHOM_dict,SSHOM,WSHOM_Coupled,WSHOM_Decoupled,NSHOM,Equivalent_SHOM)
print('Useless SHOM ',len(Useless_SHOM),'\n',Useless_SHOM)
write_hom_classification(Useless_SHOM,HOM_classification_dir,'Useless_SHOM')



do_report(len(SHOM),len(SSHOM),len(WSHOM_Coupled),len(WSHOM_Decoupled),len(NSHOM),len(Equivalent_SHOM),len(Useless_SHOM))

# ====================================================================
# 執行(Data Analysis)
# ====================================================================
# cover_to_csv(HOM_fit,'HOM_fit','AST_DataAnalysis_Folder/')
# cover_to_csv(HOM_fra,'HOM_fra','AST_DataAnalysis_Folder/')
# cover_to_csv(SHOM_dict,'SHOM_dict','AST_DataAnalysis_Folder/')

# for name,value in HOM_fit.items():
#     _leftposition = name.find('_')
#     _rightposition = name.rfind('_')
#     #print(name,name[_leftposition+1:_rightposition],name[_rightposition+1:])
#
#     HOM_FIN_CHILD['name'] = name
#     HOM_FIN_CHILD['fra'] = HOM_fra[name]
#     HOM_FIN_CHILD['fit'] = HOM_fit[name]
#     HOM_FIN_CHILD['trials'] = name[_leftposition+1:_rightposition]
#
#     HOM_FIN[name] = dict(HOM_FIN_CHILD)


#HOM_Data = create_HOM_Data(HOM_Name,HOM_fra,HOM_fit)
