import ast
import astunparse
import astpretty
import random
import os
from random import sample

# ------------------------------------------------------------------
# 宣告變數
# ------------------------------------------------------------------

source = '''
def leap(input_year):
    if (input_year % 4) == 0:
        if (input_year % 100) == 0:
            if (input_year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False
'''

# 可更換的Operator(BinOp)
binop_candidate = ['Add', 'Sub', 'Mult', 'Div', 'Mod', 'BitOr', 'BitXor', 'BitAnd']
# 可更換的Operator(Compare)
compare_candidate = ['Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE']
# 可更換的Operator(UnaryOp)
unaryop_candidate = ['UAdd', 'USub']

# 遍歷AST時，所看到的Operator
temp_node = []

# 用於紀錄現在的遍歷層數(Compare)
temp_ops_layer = 0

# HOM集合
HOM_Set = []
# 取幾個FOM(至少2個)
FOM_material_count = 3
# FOM Pool
FOM_pool = {'FOM_pool_binop':[],
            'FOM_pool_compare':[],
            'FOM_pool_unaryop':[],
            }
FOM_pool_count_max = {'FOM_pool_binop':0,
            'FOM_pool_compare':0,
            'FOM_pool_unaryop':0
                      }



FOM_pool_list = ['BinOp','Compare','UnaryOp']
FOM_pool_list_count = [3,3,0]
FOM_pool_binop = [0, 'Add', 1], [1, 'Add', 2], [2, 'Add', 3], [0, 'Sub', 4], [1, 'Sub', 5], [2, 'Sub', 6], [0, 'Mult', 7], [1, 'Mult', 8], [2, 'Mult', 9], [0, 'Div', 10], [1, 'Div', 11], [2, 'Div', 12], [0, 'BitOr', 13], [1, 'BitOr', 14], [2, 'BitOr', 15], [0, 'BitXor', 16], [1, 'BitXor', 17], [2, 'BitXor', 18], [0, 'BitAnd', 19], [1, 'BitAnd', 20], [2, 'BitAnd', 21]
FOM_pool_compare = [0, 'NotEq', 1, 22], [0, 'NotEq', 2, 23], [0, 'NotEq', 3, 24], [0, 'Lt', 1, 25], [0, 'Lt', 2, 26], [0, 'Lt', 3, 27], [0, 'LtE', 1, 28], [0, 'LtE', 2, 29], [0, 'LtE', 3, 30], [0, 'Gt', 1, 31], [0, 'Gt', 2, 32], [0, 'Gt', 3, 33], [0, 'GtE', 1, 34], [0, 'GtE', 2, 35], [0, 'GtE', 3, 36]
FOM_pool_unaryop = []




# 從FOM Pool挑出的FOM候選
FOM_material_candidate = []
# 每一組FOM候選
FOM_material = []


# 殺死FOM的測試案例路徑
FOM_killed_testcase_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_FOM_Killed_TestCase_Folder/'
# 殺死FOM的測試案例字典
FOM_killed_testcase = {}

# ------------------------------------------------------------------
# 宣告Class
# ------------------------------------------------------------------

# 更換Operator : Binop
class HOM_Transformer_Binop(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        temp_node_pos = len(temp_node) - 1
        # 暫存FOM_material
        temp_FOM_material = FOM_material

        # 依照遍歷位置去做更換Operator
        for material in temp_FOM_material:
            # 如果不是BinOp的Operator
            if (material[1] not in binop_candidate): continue
            # 如果符合更換位置
            if(temp_node_pos == material[0]):
                if(material[1]=='Add'):
                    node.op = ast.Add()
                elif(material[1]=='Sub'):
                    node.op = ast.Sub()
                elif (material[1] == 'Mult'):
                    node.op = ast.Mult()
                elif (material[1] == 'Div'):
                    node.op = ast.Div()
                elif (material[1] == 'Mod'):
                    node.op = ast.Mod()
                elif (material[1] == 'BitOr'):
                    node.op = ast.BitOr()
                elif (material[1] == 'BitXor'):
                    node.op = ast.BitXor()
                elif (material[1] == 'BitAnd'):
                    node.op = ast.BitAnd()
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : Compare
class HOM_Transformer_Compare(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 將看到的Operator放入
        temp_node.append(node.ops)

        # 暫存FOM_material
        temp_FOM_material = FOM_material

        # 防止 UnboundLocalError
        global temp_ops_layer
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1

        # 開始遍歷
        for material in temp_FOM_material:
            # 如果不是Compare的Operator
            if(material[1] not in compare_candidate):continue
            # 如果到達有需要更換Operator的層數
            if(material[2] == temp_ops_layer):
                # 將符合該層數的Operator進行更換
                for index in range(0,len(temp_node[temp_ops_layer-1])):
                    if(material[0] == index):
                        if(material[1] == 'Eq'):
                            node.ops[material[0]] = ast.Eq()
                        elif(material[1] == 'NotEq'):
                            node.ops[material[0]] = ast.NotEq()
                        elif (material[1] == 'Lt'):
                            node.ops[material[0]] = ast.Lt()
                        elif (material[1] == 'LtE'):
                            node.ops[material[0]] = ast.LtE()
                        elif (material[1] == 'Gt'):
                            node.ops[material[0]] = ast.Gt()
                        elif (material[1] == 'GtE'):
                            node.ops[material[0]] = ast.GtE()
        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : Unaryop
class HOM_Transformer_Unaryop(ast.NodeTransformer):
    def visit_UnaryOp(self, node):
        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        temp_node_pos = len(temp_node) - 1
        # 暫存FOM_material
        temp_FOM_material = FOM_material
        # 依照遍歷位置去做更換Operator
        for material in temp_FOM_material:
            # 如果不是UnaryOp的Operator
            if (material[1] not in unaryop_candidate): continue
            # 如果符合更換位置
            if (temp_node_pos == material[0]):
                if (material[1] == 'UAdd'):
                    node.op = ast.UAdd()
                elif (material[1] == 'USub'):
                    node.op = ast.USub()
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# ------------------------------------------------------------------
# 宣告副程式
# ------------------------------------------------------------------

# 檢查挑選的FOM是否重複(一組FOM候選)，(True:重複，False:沒有重複)
# 第一順位，檢查是否有相同編號的FOM。
# 第二順位，檢查同種的Operator(BinOp、Compare、UnaryOp)是否有相同位置。
#    BinOp，只檢查位置。
#    Compare，先檢查層數，再檢查位置。
#    UnaryOp，只檢查位置。

# 讀取TestCase of Killed FOM(dir:讀取位置)
def read_fom_killed_testcase(dir):

    temp_killed_testcase = {}

    for file_name in os.listdir(dir):
            if ('.txt' in file_name):
                # 讀取
                file_dir = dir + file_name
                f = open(file_dir, 'r', encoding='UTF-8')
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

# 檢查挑選的FOM是否重複(temp_material:同一組已挑選的FOM、new_FOM:新挑選的FOM)(一組FOM候選)，(True:重複，False:沒有重複)
def check_isrepeat_single(temp_material,new_FOM):
    #print('check_isrepeat_single',new_FOM[0])
    # 第一順位，編號
    for material in temp_material:
        if(material[-1] == new_FOM[-1]):
            #print('Repeat: ',material,new_FOM)
            # print('第一順位')
            return True
    # 第二順位，相同Operator且相同位置
    for material in temp_material:
        # BinOp
        if(material[1] in binop_candidate and new_FOM[1] in binop_candidate):
            if(material[0] == new_FOM[0]):
                # print('Repeat: ',material, new_FOM)
                # print(len(temp_material),temp_material)
                # print(material,new_FOM,'第二順位BinOp')
                return True
        # Compare
        elif(material[1] in compare_candidate and new_FOM[1] in compare_candidate):
            # 如果層數相同
            if(material[2] == new_FOM[2]):
                # 如果位置相同
                if (material[0] == new_FOM[0]):
                    #print('Repeat: ',material, new_FOM)
                    # print(len(temp_material),temp_material)
                    # print(material,new_FOM,'第二順位Compare')
                    return True
        # UnaryOp
        elif(material[1] in unaryop_candidate and new_FOM[1] in unaryop_candidate):
            if (material[0] == new_FOM[0]):
                #print('Repeat: ',material, new_FOM)
                # print(len(temp_material),temp_material)
                # print(material,new_FOM,'第二順位UnaryOp')
                return True

    # 如果沒有重複
    return False

# 檢查挑選的FOM是否重複(temp_material:同一組已挑選的FOM、new_FOM:新挑選的FOM、FOM_material_candidate:其他組別的FOM)(全部FOM候選)，(True:重複，False:沒有重複)
def check_isrepeat_all(temp_material,new_FOM,FOM_material_candidate):
    #print('check_isrepeat_all',new_FOM[0])
    # 暫存放入新的FOM候選，新建是為了防止共用Address
    sorted_temp_material = []
    sorted_temp_material.extend(temp_material)
    sorted_temp_material.append(new_FOM)

    # 因為==只要順序不同就代表不同，所以進行排序
    sorted_temp_list = sorted(sorted_temp_material)

    # 進行比較
    for index,material in enumerate(FOM_material_candidate):
        # 如果有重複
        if(sorted_temp_list == sorted(material)):
            return True

    # 如果沒有重複
    return False

# 檢查挑選的FOM是否重複(temp_material:同一組已挑選的FOM、new_FOM:新挑選的FOM、FOM_material_candidate:其他組別的FOM)(統整)，(True:重複，False:沒有重複)
def check_isrepeat(temp_material,new_FOM,FOM_material_candidate):
    #print('check_isrepeat', new_FOM[0])
    single_bool = check_isrepeat_single(temp_material,new_FOM)
    if(single_bool != False):
        #print('single_bool')
        return True

    all_bool = check_isrepeat_all(temp_material,new_FOM,FOM_material_candidate)
    if(all_bool != False):
        #print('all_bool')
        return True

    return False

# 檢查檢查挑選的FOM是否不能殺死(fom_killed:每個FOM可殺死自己的測試案例,new_FOM:新挑選的FOM)，(True:不可殺死，False:可殺死)
def check_isequivalent(fom_killed,new_FOM):
    #print('check_isequivalent', new_FOM[0])
    name = 'AST_FOM_' + str(new_FOM[-1])
    if(str(fom_killed[name]) != 'No'):
        return False
    else:
       return True

    return False

# 挑選FOM(amount:幾組FOM候選,fom_killed:可殺死FOM的測試案例,min_quantity:一個HOM最少幾個FOM,max_quantity:一個HOM最多幾個FOM)
def choose_FOM(amount,fom_killed,fom_pool_count_max,min_quantity,max_quantity):
    # 從FOM_pool挑出的FOM數量
    count = 0
    # 產生幾組FOM_material
    numbers = amount
    # 隨機一個FOM_pool的material
    FOM_pool_count = -1
    # 暫存每一組FOM候選
    temp_material = []
    # 暫存所有從FOM Pool挑出的FOM候選
    temp_FOM_material_candidate = []

    #
    temp_choice = ''
    temp_binop_max = 0
    temp_compare_max = 0
    temp_unaryop_max = 0

    # 挑選FOM
    for index in range(1,numbers+1):
        # 每一組FOM候選的數量
        count = random.randint(min_quantity, max_quantity)

        # 如果沒有產生重複的FOM候選，則temp_material的數量會增加
        while (len(temp_material) < count):
            #print(len(temp_material),count)
            # 從FOM Pool挑選
            for i in range(1,count+1):
                # 如果temp_material已經符合一組FOM候選的數量
                if (len(temp_material) >= count):
                    break

                while(FOM_pool_count == -1):
                    # 從 BinOp、Compaer、UnaryOp當中選擇要哪一組
                    temp_choice = random.choice(list(FOM_pool.keys()))
                    if(temp_choice == 'FOM_pool_binop'):
                        if( (temp_binop_max+1) <= fom_pool_count_max[temp_choice]):
                            FOM_pool_count = random.randint(0, len(FOM_pool[temp_choice]) - 1)
                            temp_binop_max = temp_binop_max + 1
                            break
                        else:
                            FOM_pool_count = -1
                    elif(temp_choice == 'FOM_pool_compare'):
                        if( (temp_compare_max+1) <= fom_pool_count_max[temp_choice]):
                            FOM_pool_count = random.randint(0, len(FOM_pool[temp_choice]) - 1)
                            temp_compare_max = temp_compare_max + 1
                            break
                        else:
                            FOM_pool_count = -1
                    elif (temp_choice == 'FOM_pool_unaryop'):
                        if ((temp_unaryop_max + 1) <= fom_pool_count_max[temp_choice]):
                            FOM_pool_count = random.randint(0, len(FOM_pool[temp_choice]) - 1)
                            temp_unaryop_max = temp_unaryop_max + 1
                            break
                        else:
                            FOM_pool_count = -1


                # 放入FOM候選(如果不重複)
                if(check_isequivalent(fom_killed,FOM_pool[temp_choice][FOM_pool_count]) == False and check_isrepeat(temp_material,FOM_pool[temp_choice][FOM_pool_count],temp_FOM_material_candidate) == False):
                    temp_material.append(FOM_pool[temp_choice][FOM_pool_count])

                # 重置
                temp_choice = ''
                FOM_pool_count = -1

            temp_binop_max = 0
            temp_compare_max = 0
            temp_unaryop_max = 0

        # 將一組FOM候選放入
        temp_FOM_material_candidate.append(temp_material)
        # 重置
        temp_material = []
        temp_choice = ''
        FOM_pool_count = -1
        temp_binop_max = 0
        temp_compare_max = 0
        temp_unaryop_max = 0


    # 回傳全部從FOM Pool挑出的FOM候選
    return temp_FOM_material_candidate

# 組合HOM(統整)，(asttype:ast transformer的類型，source_code:原始碼)
def create_HOM(asttype,source_code):
    if asttype == 'BinOp':
        return create_HOM_BinOp(source_code)
    elif asttype == 'Compare':
        return create_HOM_Compare(source_code)
    elif asttype == 'Unaryop':
        return create_HOM_Unaryop(source_code)
    else :
        print('Create HOM Error.')

# 組合HOM(BinOp)，(source_code:原始碼)
def create_HOM_BinOp(source_code):
    # 更換Operator : BinOp
    temp_HOM_Transformer = HOM_Transformer_Binop()
    # 開始更換Operator
    temp_HOM = temp_HOM_Transformer.visit(ast.parse(astunparse.unparse(ast.parse(source_code))))
    # ast->Code
    temp_HOM = astunparse.unparse(temp_HOM)

    #print('Create HOM(BinOp) OK.')
    return temp_HOM

# 組合HOM(Compare)，(source_code:原始碼)
def create_HOM_Compare(source_code):
    # 更換Operator : Compare
    temp_HOM_Transformer = HOM_Transformer_Compare()
    # 開始更換Operator
    temp_HOM = temp_HOM_Transformer.visit(ast.parse(astunparse.unparse(ast.parse(source_code))))
    # ast->Code
    temp_HOM = astunparse.unparse(temp_HOM)

    #print('Create HOM(Compare) OK.')
    return temp_HOM

# 組合HOM(Unaryop)，(source_code:原始碼)
def create_HOM_Unaryop(source_code):
    # 更換Operator : Unaryop
    temp_HOM_Transformer = HOM_Transformer_Unaryop()
    # 開始更換Operator
    temp_HOM = temp_HOM_Transformer.visit(ast.parse(astunparse.unparse(ast.parse(source_code))))
    # ast->Code
    temp_HOM = astunparse.unparse(temp_HOM)

    #print('Create HOM(Unaryop) OK.')
    return temp_HOM

# 寫入HOM(path:HOM寫入位置、path_material:HOM所組成的FOM寫入位置、trial:組別、HOM_Set:全部HOM、FOM_material_candidate:HOM所組成的FOM)
def write_file_HOM(path,path_material,trial,HOM_Set,FOM_material_candidate):
    #  新建資料夾
    if(os.path.isdir(path) == False):
        os.mkdir(path)

    # 寫入HOM
    for number, content in enumerate(HOM_Set):
        try:
            file_dir = path + '/' + 'HOM_' + str(trial) + '_' + str(number + 1) + '.py'
            f = open(file_dir, 'w+')
            f.write(str(content).replace('\n', '', 2) + '#'+str(FOM_material_candidate[number]))
            f.seek(0)
            f.close()
        except AttributeError:
            print('AttributeError')

    #  新建資料夾
    if (os.path.isdir(path_material) == False):
        os.mkdir(path_material)

    # 寫入HOM(FOM Material)
    for number, content in enumerate(HOM_Set):
        try:
            file_dir = path_material + '/' + 'HOM_' + str(trial) + '_' + str(number + 1) + '.txt'
            f = open(file_dir, 'w+')
            f.write(str(FOM_material_candidate[number]))
            f.seek(0)
            f.close()
        except AttributeError:
            print('AttributeError')

# 組合HOM(code:原始碼、FOM_pool:各個AST Module的FOM、FOM_pool_count_max:各個AST Module的FOM的選擇上限、trials:幾組HOM、numbers:一組幾個HOM、min_quantity:一個HOM最少幾個FOM、max_quantity:一個HOM最多幾個FOM(只能是FOM_pool_count_max的總和))
def do_create_HOM(code,FOM_pool,FOM_pool_count_max,trials,numbers,min_quantity,max_quantity):

    expr_2 = code

    # 使用 global variable HOM_Set
    global HOM_Set
    # 使用 global variable FOM_material
    global FOM_material
    # 使用 global variable temp_node
    global temp_node
    # 使用 global variable temp_ops_layer
    global temp_ops_layer
    # 使用 global variable
    global FOM_killed_testcase
    # 使用 global variable
    global FOM_killed_testcase_dir

    # 讀取FOM
    FOM_pool['FOM_pool_binop'] = FOM_pool_binop
    FOM_pool['FOM_pool_compare'] = FOM_pool_compare
    FOM_pool['FOM_pool_unaryop'] = FOM_pool_unaryop

    FOM_pool_count_max['FOM_pool_binop'] = FOM_pool_list_count[0]
    FOM_pool_count_max['FOM_pool_compare'] = FOM_pool_list_count[1]
    FOM_pool_count_max['FOM_pool_unaryop'] = FOM_pool_list_count[2]

    # 讀取TestCase of Killed FOM
    FOM_killed_testcase = read_fom_killed_testcase(FOM_killed_testcase_dir)

    # 100 trials,10,000 Numbers

    for trial in range(1,trials+1):
        print('[',(trial),']', '.......................trials')

        # HOM寫入位置
        path = 'AST_Mutant_Folder/AST_HOM_Folder/' + 'AST_HOM_Folder_' + str(trial)
        # HOM寫入位置(FOM Material)
        path_material = 'AST_Mutant_Folder/AST_HOM_Material_Folder/' + 'AST_HOM_Material_Folder_' + str(trial)

        # 挑選FOM
        FOM_material_candidate = choose_FOM(numbers,FOM_killed_testcase,FOM_pool_count_max,min_quantity, max_quantity)

        # 組合HOM
        for order, temp in enumerate(FOM_material_candidate):
            # 一組FOM候選
            FOM_material = temp
            for material in FOM_material:
                print(material,FOM_killed_testcase['AST_FOM_' + str(material[-1])])
                print()

            # 組合HOM(BinOp)
            expr_2 = create_HOM('BinOp', expr_2)
            temp_node = []
            temp_ops_layer = 0


            # 組合HOM(Compare)
            expr_2 = create_HOM('Compare', expr_2)
            temp_node = []
            temp_ops_layer = 0

            # 組合HOM(Unaryop)
            expr_2 = create_HOM('Unaryop', expr_2)
            temp_node = []
            temp_ops_layer = 0

            # 組合結果
            print(order + 1, '..........', FOM_material)
            # 放入 HOM_Set
            HOM_Set.append(expr_2)
            #print(expr_2)
            # 重置
            expr_2 = code

        # 寫入
        write_file_HOM(path,path_material,trial,HOM_Set,FOM_material_candidate)



        # 重置
        print('\n')
        expr_2 = code
        FOM_material_candidate = []
        temp_node = []
        temp_ops_layer = 0
        HOM_Set = []

    print('Create HOM Done.')


# --------------------------------------------------------
# 執行
# --------------------------------------------------------
do_create_HOM(source,FOM_pool,FOM_pool_count_max,15,20,2,10)