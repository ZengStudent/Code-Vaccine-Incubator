import ast
import astunparse
import astpretty
import os,shutil
# 判斷三角形
def tri(a, b, c):
    result = ''
    # 判斷是否可以形成三角形
    if (a + b <= c):
        result = 'No'
    # 判斷是否可以形成銳角三角形
    elif (a * a + b * b < c * c):
        result = 'Obtuse'
    # 判斷是否可以形成直角三角形
    elif (a * a + b * b == c * c):
        result = 'Right'
    # 判斷是否可以形成鈍角三角形
    elif (a * a + b * b > c * c):
        result = 'Acute'
    return result


# --------------------------------------------------------------------------------------------------------------------
# 第一部份
# --------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------
# 宣告變數(For ast.NodeVisitor)
# ----------------------------------------------------------

# 遍歷AST
expr ='''
def tri(a,b,c):
    result = ''
    # 判斷是否可以形成三角形
    if (a + b <= c):
        result = 'No'
    # 判斷是否可以形成銳角三角形
    elif (a * a + b * b < c * c):
        result = 'Obtuse'
    # 判斷是否可以形成直角三角形
    elif (a * a + b * b == c * c):
        result = 'Right'
    # 判斷是否可以形成鈍角三角形
    elif (a * a + b * b > c * c):
        result = 'Acute'
    return result
'''

expr_2 ='''
def fib(input):
    f0 = 0
    f1 = 1
    f2 = 1
    if(input == 0):
        return 0
    elif(input == 1 or input == 2):
        return 1
    else:
       return fib(input - 1) + fib(input - 2)
'''


# 遍歷結果(整體順序)
all_index_list = []

# 可更換的Operator(BinOp)
binop_candidate = ['Add', 'Sub', 'Mult', 'Div', 'Mod', 'BitOr', 'BitXor', 'BitAnd']
# ast所有的Operator(BinOp)
binop_name = ['Add', 'Sub', 'Mult', 'MatMult', 'Div', 'Mod', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd','FloorDiv']
# 遍歷結果(整體順序、BinOp)
binop_list = []
# 遍歷結果(數量、BinOp)
binop_dict = {'Add': 0, 'Sub': 0, 'Mult': 0, 'MatMult': 0, 'Div': 0, 'Mod': 0, 'Pow': 0, 'LShift': 0, 'RShift': 0,
              'BitOr': 0, 'BitXor': 0, 'BitAnd': 0, 'FloorDiv': 0}
# 遍歷結果(個別順序、BinOp)
binop_index_dict = {'Add': [], 'Sub': [], 'Mult': [], 'MatMult': [], 'Div': [], 'Mod': [], 'Pow': [], 'LShift': [],
                    'RShift': [], 'BitOr': [], 'BitXor': [], 'BitAnd': [], 'FloorDiv': []}

# 可更換的Operator(Compare)
compare_candidate = ['Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE']
# ast所有的Operator(Compare)
compare_name = ['Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'Is', 'IsNot', 'In', 'NotIn']
# 遍歷結果(整體順序、Compare)
compare_list = []
# 遍歷結果(數量、Compare)
compare_dict = {'Eq': 0, 'NotEq': 0, 'Lt': 0, 'LtE': 0, 'Gt': 0, 'GtE': 0, 'Is': 0, 'IsNot': 0, 'In': 0, 'NotIn': 0}
# 遍歷結果(個別順序、Compare)
compare_index_dict = {'Eq': [], 'NotEq': [], 'Lt': [], 'LtE': [], 'Gt': [], 'GtE': [], 'Is': [], 'IsNot': [], 'In': [],
                      'NotIn': []}

# 可更換的Operator(UnaryOp)
unaryop_candidate = ['UAdd', 'USub']
# ast所有的Operator(UnaryOp)
unaryop_name = ['UAdd', 'USub', 'Not', 'Invert']
# 遍歷結果(整體順序、UnaryOp)
unaryop_list = []
# 遍歷結果(數量、UnaryOp)
unaryop_dict = {'UAdd': 0, 'USub': 0, 'Not': 0, 'Invert': 0}
# 遍歷結果(個別順序、UnaryOp)
unaryop_index_dict = {'UAdd': [], 'USub': [], 'Not': [], 'Invert': []}

# 更換位置、更換的Operator(binop)
FOM_binop_record = []
# 更換位置、更換的Operator、更換的層數(compare)
FOM_compare_record = []
# 更換位置、更換的Operator(unaryop)
FOM_unaryop_record = []


# Visit Source Code Ast
class FOM_Visitor(ast.NodeVisitor):
    def generic_visit(self, node):
        if (node.__class__.__name__ in binop_name):
            binop_dict[node.__class__.__name__] = binop_dict[node.__class__.__name__] + 1
            binop_list.append(node.__class__.__name__)
            binop_index_dict[node.__class__.__name__].append(len(binop_list))
            all_index_list.append(node.__class__.__name__)

        if (node.__class__.__name__ in compare_name):
            compare_dict[node.__class__.__name__] = compare_dict[node.__class__.__name__] + 1
            compare_list.append(node.__class__.__name__)
            compare_index_dict[node.__class__.__name__].append(len(compare_list))
            all_index_list.append(node.__class__.__name__)

        if (node.__class__.__name__ in unaryop_name):
            unaryop_dict[node.__class__.__name__] = unaryop_dict[node.__class__.__name__] + 1
            unaryop_list.append(node.__class__.__name__)
            unaryop_index_dict[node.__class__.__name__].append(len(unaryop_list))
            all_index_list.append(node.__class__.__name__)

        ast.NodeVisitor.generic_visit(self, node)


Vis = FOM_Visitor()
Vis.visit(ast.parse(expr_2))
print(binop_list)
print(binop_dict)
print(binop_index_dict)
print()
print(compare_list)
print(compare_dict)
print(compare_index_dict)
print()
print(unaryop_list)
print(unaryop_dict)
print(unaryop_index_dict)
print(all_index_list)


# --------------------------------------------------------------------------------------------------------------------
# 第二部份
# --------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------
# 宣告變數(For ast.NodeTransformer)
# ----------------------------------------------------------

# FOM
FOM_Set = []
# 遍歷AST時，所看到的Operator
temp_node = []
# 現在遍歷的位置
temp_node_pos = 0
# 想要更換Operator的位置
want_node_pos = 0
# 現在更換的Operator候選
temp_now_op = ''
# 是否符合FOM的條件，True:符合 False:不符合
temp_FOM_Set_Add = True
# 暫存FOM更換位置和更換的Operator
temp_record = []
# 是否已經換過operator(compare)，True:換過 False:沒換過
compare_ischange = False
# 計算某個Operator的第幾次更換
temp_node_count = 0
# 現在compare的遍歷層數
temp_ops_layer = 0

# 更換Operator : Add(+)
class FOM_Transformer_Add(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node)-1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.Add()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : Sub(-)
class FOM_Transformer_Sub(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.Sub()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : Mult(*)
class FOM_Transformer_Mult(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.Mult()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : Div(/)
class FOM_Transformer_Div(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.Div()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : Mod(%)
class FOM_Transformer_Mod(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.Mod()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : BitOr(|)
class FOM_Transformer_BitOr(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node)-1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.BitOr()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : BitXor(^)
class FOM_Transformer_BitXor(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.BitXor()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node

# 更換Operator : BitAnd(&)
class FOM_Transformer_BitAnd(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1
        # print('node: ', node.op)
        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            # 更換次數+1
            #temp_node_count = temp_node_count + 1
            # 更換Operator
            node.op = ast.BitAnd()
            # 記錄更換次數和更換的Operator
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')
        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# Ast Transformer(op=AST的名稱)
# BinOp
def binop_operator(op):
    if op == 'Add':
        return FOM_Transformer_Add()
    elif op == 'Sub':
        return FOM_Transformer_Sub()
    elif op == 'Mult':
        return FOM_Transformer_Mult()
    elif op == 'Div':
        return FOM_Transformer_Div()
    elif op == 'Mod':
        return FOM_Transformer_Mod()
    elif op == 'BitOr':
        return FOM_Transformer_BitOr()
    elif op == 'BitXor':
        return FOM_Transformer_BitXor()
    elif op == 'BitAnd':
        return FOM_Transformer_BitAnd()
    else:
        return FOM_Transformer_Add()


# 更換Operator : Eq(==)
class FOM_Transformer_Eq(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global compare_ischange
        # 防止 UnboundLocalError
        global temp_ops_layer

        # 將這一層的Operator放入
        temp_node.append(node.ops)
        # 現在遍歷的位置
        temp_node_pos = want_node_pos
        # 現在遍歷的總長度
        temp_node_length = 0
        # 要變更的節點所在的層數
        temp_layer = 0
        # 是否找到要變更的節點所在的層數，True:找到 False:未找到
        layer_bool = False
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1
        # 如果未換過operator(compare)
        if (compare_ischange == False):
            # 找出要變更的節點所在的層數
            for layer in range(len(temp_node)):
                # 計算現在遍歷的總長度，每個node.ops的長度的總和
                temp_node_length = temp_node_length + len(temp_node[layer])
                # 如果總長度 >= 想要更換Operator的位置，代表已到達要變更的節點所在的層數
                if (temp_node_length - 1 >= want_node_pos):
                    # 紀錄要變更的節點所在的層數
                    temp_layer = layer
                    # 找到要變更的節點所在的層數
                    layer_bool = True
                    break
                # 反之，未到達要變更的節點所在的層數
                else:
                    layer_bool = False
        # 如果 到達要變更的節點所在的層數 且 未換過operator(compare)
        if (layer_bool == True and compare_ischange == False):
            # 計算是這一層的第幾個節點要進行更換
            for want_layer in range(temp_layer):
                temp_node_pos = temp_node_pos - len(temp_node[want_layer])

            # Compare 是一次遍歷全部的node，並回傳node.ops，代表全部的Compare，並從第一個節點開始
            # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
            if (node.ops[temp_node_pos].__class__.__name__ == temp_now_op):
                temp_FOM_Set_Add = False
                compare_ischange = True
                # print('Same')
            # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
            elif (node.ops[temp_node_pos].__class__.__name__ != temp_now_op):
                temp_FOM_Set_Add = True
                compare_ischange = True
                node.ops[temp_node_pos] = ast.Eq()
                # 記錄改變的更換位置和更換的Operator
                temp_record = [temp_node_pos, temp_now_op,temp_ops_layer]

                print('want_node_pos: ', temp_node_pos)

        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# 更換Operator : NotEq(!=)
class FOM_Transformer_NotEq(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global compare_ischange
        # 防止 UnboundLocalError
        global temp_ops_layer

        # 將這一層的Operator放入
        temp_node.append(node.ops)
        # 現在遍歷的位置
        temp_node_pos = want_node_pos
        # 現在遍歷的總長度
        temp_node_length = 0
        # 要變更的節點所在的層數
        temp_layer = 0
        # 是否找到要變更的節點所在的層數，True:找到 False:未找到
        layer_bool = False
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1
        # 如果未換過operator(compare)
        if (compare_ischange == False):
            # 找出要變更的節點所在的層數
            for layer in range(len(temp_node)):
                # 計算現在遍歷的總長度，每個node.ops的長度的總和
                temp_node_length = temp_node_length + len(temp_node[layer])
                # 如果總長度 >= 想要更換Operator的位置，代表已到達要變更的節點所在的層數
                if (temp_node_length - 1 >= want_node_pos):
                    # 紀錄要變更的節點所在的層數
                    temp_layer = layer
                    # 找到要變更的節點所在的層數
                    layer_bool = True
                    break
                # 反之，未到達要變更的節點所在的層數
                else:
                    layer_bool = False
        # 如果 到達要變更的節點所在的層數 且 未換過operator(compare)
        if (layer_bool == True and compare_ischange == False):
            # 計算是這一層的第幾個節點要進行更換
            for want_layer in range(temp_layer):
                temp_node_pos = temp_node_pos - len(temp_node[want_layer])

            # Compare 是一次遍歷全部的node，並回傳node.ops，代表全部的Compare，並從第一個節點開始
            # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
            if (node.ops[temp_node_pos].__class__.__name__ == temp_now_op):
                temp_FOM_Set_Add = False
                compare_ischange = True
                # print('Same')
            # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
            elif (node.ops[temp_node_pos].__class__.__name__ != temp_now_op):
                temp_FOM_Set_Add = True
                compare_ischange = True
                node.ops[temp_node_pos] = ast.NotEq()
                # 記錄改變的更換位置和更換的Operator
                temp_record = [temp_node_pos, temp_now_op,temp_ops_layer]

                print('want_node_pos: ', temp_node_pos)

        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# 更換Operator : Lt(<)
class FOM_Transformer_Lt(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global compare_ischange
        # 防止 UnboundLocalError
        global temp_ops_layer

        # 將這一層的Operator放入
        temp_node.append(node.ops)
        # 現在遍歷的位置
        temp_node_pos = want_node_pos
        # 現在遍歷的總長度
        temp_node_length = 0
        # 要變更的節點所在的層數
        temp_layer = 0
        # 是否找到要變更的節點所在的層數，True:找到 False:未找到
        layer_bool = False
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1
        # 如果未換過operator(compare)
        if (compare_ischange == False):
            # 找出要變更的節點所在的層數
            for layer in range(len(temp_node)):
                # 計算現在遍歷的總長度，每個node.ops的長度的總和
                temp_node_length = temp_node_length + len(temp_node[layer])
                # 如果總長度 >= 想要更換Operator的位置，代表已到達要變更的節點所在的層數
                if (temp_node_length - 1 >= want_node_pos):
                    # 紀錄要變更的節點所在的層數
                    temp_layer = layer
                    # 找到要變更的節點所在的層數
                    layer_bool = True
                    break
                # 反之，未到達要變更的節點所在的層數
                else:
                    layer_bool = False
        # 如果 到達要變更的節點所在的層數 且 未換過operator(compare)
        if (layer_bool == True and compare_ischange == False):
            # 計算是這一層的第幾個節點要進行更換
            for want_layer in range(temp_layer):
                temp_node_pos = temp_node_pos - len(temp_node[want_layer])

            # Compare 是一次遍歷全部的node，並回傳node.ops，代表全部的Compare，並從第一個節點開始
            # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
            if (node.ops[temp_node_pos].__class__.__name__ == temp_now_op):
                temp_FOM_Set_Add = False
                compare_ischange = True
                # print('Same')
            # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
            elif (node.ops[temp_node_pos].__class__.__name__ != temp_now_op):
                temp_FOM_Set_Add = True
                compare_ischange = True
                node.ops[temp_node_pos] = ast.Lt()
                # 記錄改變的更換位置和更換的Operator
                temp_record = [temp_node_pos, temp_now_op,temp_ops_layer]

                print('want_node_pos: ', temp_node_pos)

        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# 更換Operator : LtE(<=)
class FOM_Transformer_LtE(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global compare_ischange
        # 防止 UnboundLocalError
        global temp_ops_layer

        # 將這一層的Operator放入
        temp_node.append(node.ops)
        # 現在遍歷的位置
        temp_node_pos = want_node_pos
        # 現在遍歷的總長度
        temp_node_length = 0
        # 要變更的節點所在的層數
        temp_layer = 0
        # 是否找到要變更的節點所在的層數，True:找到 False:未找到
        layer_bool = False
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1
        # 如果未換過operator(compare)
        if (compare_ischange == False):
            # 找出要變更的節點所在的層數
            for layer in range(len(temp_node)):
                # 計算現在遍歷的總長度，每個node.ops的長度的總和
                temp_node_length = temp_node_length + len(temp_node[layer])
                # 如果總長度 >= 想要更換Operator的位置，代表已到達要變更的節點所在的層數
                if (temp_node_length - 1 >= want_node_pos):
                    # 紀錄要變更的節點所在的層數
                    temp_layer = layer
                    # 找到要變更的節點所在的層數
                    layer_bool = True
                    break
                # 反之，未到達要變更的節點所在的層數
                else:
                    layer_bool = False
        # 如果 到達要變更的節點所在的層數 且 未換過operator(compare)
        if (layer_bool == True and compare_ischange == False):
            # 計算是這一層的第幾個節點要進行更換
            for want_layer in range(temp_layer):
                temp_node_pos = temp_node_pos - len(temp_node[want_layer])

            # Compare 是一次遍歷全部的node，並回傳node.ops，代表全部的Compare，並從第一個節點開始
            # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
            if (node.ops[temp_node_pos].__class__.__name__ == temp_now_op):
                temp_FOM_Set_Add = False
                compare_ischange = True
                # print('Same')
            # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
            elif (node.ops[temp_node_pos].__class__.__name__ != temp_now_op):
                temp_FOM_Set_Add = True
                compare_ischange = True
                node.ops[temp_node_pos] = ast.LtE()
                # 記錄改變的更換位置和更換的Operator
                temp_record = [temp_node_pos, temp_now_op,temp_ops_layer]

                print('want_node_pos: ', temp_node_pos)

        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# 更換Operator : Gt(>)
class FOM_Transformer_Gt(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global compare_ischange
        # 防止 UnboundLocalError
        global temp_ops_layer

        # 將這一層的Operator放入
        temp_node.append(node.ops)
        # 現在遍歷的位置
        temp_node_pos = want_node_pos
        # 現在遍歷的總長度
        temp_node_length = 0
        # 要變更的節點所在的層數
        temp_layer = 0
        # 是否找到要變更的節點所在的層數，True:找到 False:未找到
        layer_bool = False
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1
        # 如果未換過operator(compare)
        if (compare_ischange == False):
            # 找出要變更的節點所在的層數
            for layer in range(len(temp_node)):
                # 計算現在遍歷的總長度，每個node.ops的長度的總和
                temp_node_length = temp_node_length + len(temp_node[layer])
                # 如果總長度 >= 想要更換Operator的位置，代表已到達要變更的節點所在的層數
                if (temp_node_length - 1 >= want_node_pos):
                    # 紀錄要變更的節點所在的層數
                    temp_layer = layer
                    # 找到要變更的節點所在的層數
                    layer_bool = True
                    break
                # 反之，未到達要變更的節點所在的層數
                else:
                    layer_bool = False
        # 如果 到達要變更的節點所在的層數 且 未換過operator(compare)
        if (layer_bool == True and compare_ischange == False):
            # 計算是這一層的第幾個節點要進行更換
            for want_layer in range(temp_layer):
                temp_node_pos = temp_node_pos - len(temp_node[want_layer])

            # Compare 是一次遍歷全部的node，並回傳node.ops，代表全部的Compare，並從第一個節點開始
            # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
            if (node.ops[temp_node_pos].__class__.__name__ == temp_now_op):
                temp_FOM_Set_Add = False
                compare_ischange = True
                # print('Same')
            # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
            elif (node.ops[temp_node_pos].__class__.__name__ != temp_now_op):
                temp_FOM_Set_Add = True
                compare_ischange = True
                node.ops[temp_node_pos] = ast.Gt()
                # 記錄改變的更換位置和更換的Operator
                temp_record = [temp_node_pos, temp_now_op,temp_ops_layer]

                print('want_node_pos: ', temp_node_pos)

        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# 更換Operator : GtE(>=)
class FOM_Transformer_GtE(ast.NodeTransformer):
    def visit_Compare(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global compare_ischange
        # 防止 UnboundLocalError
        global temp_ops_layer

        # 將這一層的Operator放入
        temp_node.append(node.ops)
        # 現在遍歷的位置
        temp_node_pos = want_node_pos
        # 現在遍歷的總長度
        temp_node_length = 0
        # 要變更的節點所在的層數
        temp_layer = 0
        # 是否找到要變更的節點所在的層數，True:找到 False:未找到
        layer_bool = False
        # 現在遍歷層數，每次+1層
        temp_ops_layer = temp_ops_layer + 1
        # 如果未換過operator(compare)
        if (compare_ischange == False):
            # 找出要變更的節點所在的層數
            for layer in range(len(temp_node)):
                # 計算現在遍歷的總長度，每個node.ops的長度的總和
                temp_node_length = temp_node_length + len(temp_node[layer])
                # 如果總長度 >= 想要更換Operator的位置，代表已到達要變更的節點所在的層數
                if (temp_node_length - 1 >= want_node_pos):
                    # 紀錄要變更的節點所在的層數
                    temp_layer = layer
                    # 找到要變更的節點所在的層數
                    layer_bool = True
                    break
                # 反之，未到達要變更的節點所在的層數
                else:
                    layer_bool = False
        # 如果 到達要變更的節點所在的層數 且 未換過operator(compare)
        if (layer_bool == True and compare_ischange == False):
            # 計算是這一層的第幾個節點要進行更換
            for want_layer in range(temp_layer):
                temp_node_pos = temp_node_pos - len(temp_node[want_layer])

            # Compare 是一次遍歷全部的node，並回傳node.ops，代表全部的Compare，並從第一個節點開始
            # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
            if (node.ops[temp_node_pos].__class__.__name__ == temp_now_op):
                temp_FOM_Set_Add = False
                compare_ischange = True
                # print('Same')
            # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
            # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
            # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
            elif (node.ops[temp_node_pos].__class__.__name__ != temp_now_op):
                temp_FOM_Set_Add = True
                compare_ischange = True
                node.ops[temp_node_pos] = ast.GtE()
                # 記錄改變的更換位置和更換的Operator
                temp_record = [temp_node_pos, temp_now_op,temp_ops_layer]

                print('want_node_pos: ', temp_node_pos)

        # 下一層節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# Ast Transformer(op=AST的名稱)
# Compare
def compare_operator(op):
    if op == 'Eq':
        return FOM_Transformer_Eq()
    elif op == 'NotEq':
        return FOM_Transformer_NotEq()
    elif op == 'Lt':
        return FOM_Transformer_Lt()
    elif op == 'LtE':
        return FOM_Transformer_LtE()
    elif op == 'Gt':
        return FOM_Transformer_Gt()
    elif op == 'GtE':
        return FOM_Transformer_GtE()
    else:
        return FOM_Transformer_Eq()


# 更換Operator : UAdd(U+)
class FOM_Transformer_UAdd(ast.NodeTransformer):
    def visit_UnaryOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置(同Binop)
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1

        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            #temp_node_count = temp_node_count + 1
            node.op = ast.UAdd()
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')

        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# 更換Operator : UAdd(U-)
class FOM_Transformer_USub(ast.NodeTransformer):
    def visit_UnaryOp(self, node):
        # 防止 UnboundLocalError
        global want_node_pos
        # 防止 UnboundLocalError
        global temp_FOM_Set_Add
        # 防止 UnboundLocalError
        global temp_record
        # 防止 UnboundLocalError
        global temp_node_count

        # 將看到的Operator放入
        temp_node.append(node.op)
        # 現在遍歷的位置(同Binop)
        # BinOp 是一次遍歷一個的node，並回傳node.op，代表當下node的Operator，並從最後一個節點開始
        temp_node_pos = len(temp_node) - 1

        # 如果這個Operator == 現在更換的Operator候選(代表和原本的Source Code的Operator相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator相同，所以不需更換
        if (node.op.__class__.__name__ == temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = False
            # print('Same')
        # 如果這個Operator != 現在更換的Operator候選(代表和原本的Source Code的Operator不相同)
        # 想要更換Operator的位置 == 想要更換的位置(代表和原本的Source Code的Operator的位置相同)
        # 上述兩行代表會將Operator換成跟原本的Source Code的Operator不相同，所以需更換
        elif (node.op.__class__.__name__ != temp_now_op and temp_node_pos == want_node_pos):
            temp_FOM_Set_Add = True
            #temp_node_count = temp_node_count + 1
            node.op = ast.USub()
            temp_record = [temp_node_pos, temp_now_op]
            print('want_node_pos: ', want_node_pos)
        # 如果都不符合代表著不是要更換的位置，會生成HOM
        else:
            print('Skip')

        # 下一個節點
        ast.NodeVisitor.generic_visit(self, node)
        # 遍歷完成才會回傳
        return node


# Ast Transformer(op=AST的名稱)
# UnaryOp
def unary_operator(op):
    if op == 'UAdd':
        return FOM_Transformer_UAdd()
    elif op == 'USub':
        return FOM_Transformer_USub()
    else:
        return FOM_Transformer_UAdd()

# FOM生成(Binop)
def create_FOM_Binop():
    global temp_FOM_Set_Add
    global temp_record
    global FOM_Set
    global temp_now_op
    global want_node_pos
    global temp_node
    global temp_node_pos
    global temp_node_count

    for i in binop_candidate:
        # 依照 Source Code 的Operator的數量，決定更換的次數
        for index in range(0, len(binop_list)):
            print('OP:', i)
            temp_now_op = i
            want_node_pos = index
            # 依照Operator候選，生成Transformer
            temp_FOM_Transformer = binop_operator(i)
            # 開始更換Operator
            temp_FOM = temp_FOM_Transformer.visit(ast.parse(astunparse.unparse(ast.parse(expr_2))))
            # 如果符合FOM的條件，則放入FOM_Set、FOM_binop_record
            if (temp_FOM_Set_Add == True):
                # FOM_Set.add(temp_FOM)
                FOM_Set.append(temp_FOM)
                # 第幾個FOM
                temp_record.append(len(FOM_Set))
                # 紀錄改變位置、Operator、編號
                FOM_binop_record.append(temp_record)
            print()
            # 重置
            temp_FOM = None
            want_node_pos = 0
            temp_node = []
            temp_node_pos = 0
            temp_FOM_Set_Add = False
            temp_record = []
        temp_node_count = 0
    return None

# FOM生成(Compare)
def create_FOM_Compare():
    global temp_FOM_Set_Add
    global temp_record
    global FOM_Set
    global temp_now_op
    global want_node_pos
    global temp_node
    global temp_node_pos
    global temp_node_count
    global compare_ischange
    global temp_ops_layer

    for i in compare_candidate:
        for index in range(len(compare_list)):
            print('OP:', i)
            temp_now_op = i
            want_node_pos = index
            # 依照Operator候選，生成Transformer
            temp_FOM_Transformer = compare_operator(i)
            # 開始更換Operator
            temp_FOM = temp_FOM_Transformer.visit(ast.parse(astunparse.unparse(ast.parse(expr_2))))
            # 如果符合FOM的條件，則放入FOM_Set、FOM_compare_record
            if (temp_FOM_Set_Add == True):
                # FOM_Set.add(temp_FOM)
                FOM_Set.append(temp_FOM)
                # 第幾個FOM
                temp_record.append(len(FOM_Set))
                # 紀錄改變位置、Operator、層數、編號
                FOM_compare_record.append(temp_record)
            print(len(FOM_Set))
            print()

            # 重置
            temp_FOM = None
            want_node_pos = 0
            temp_node = []
            temp_node_pos = 0
            temp_FOM_Set_Add = False
            temp_record = []
            compare_ischange = False
            temp_ops_layer = 0
    return None

# FOM生成(Unaryop)
def create_FOM_Unaryop():
    global temp_FOM_Set_Add
    global temp_record
    global FOM_Set
    global temp_now_op
    global want_node_pos
    global temp_node
    global temp_node_pos
    global temp_node_count

    for i in unaryop_candidate:
        # 依照 Source Code 的Operator的數量，決定更換的次數
        for index in range(0, len(unaryop_list)):
            print('OP:', i)
            temp_now_op = i
            want_node_pos = index
            # 依照Operator候選，生成Transformer
            temp_FOM_Transformer = unary_operator(i)
            # 開始更換Operator
            temp_FOM = temp_FOM_Transformer.visit(ast.parse(astunparse.unparse(ast.parse(expr_2))))
            # 如果符合FOM的條件，則放入FOM_Set、FOM_unaryop_record
            if (temp_FOM_Set_Add == True):
                # 放入 FOM
                FOM_Set.append(temp_FOM)
                # 第幾個FOM
                temp_record.append(len(FOM_Set))
                # 紀錄改變位置、Operator、編號
                FOM_unaryop_record.append(temp_record)
            print()
            # 重置
            temp_FOM = None
            want_node_pos = 0
            temp_node = []
            temp_node_pos = 0
            temp_FOM_Set_Add = False
            temp_record = []
        temp_node_count = 0
    return None


# FOM生成(統整)
def create_FOM(asttype):
    if(asttype == 'Binop'):
        create_FOM_Binop()
    elif(asttype == 'Compare'):
        create_FOM_Compare()
    elif(asttype == 'Unaryop'):
        create_FOM_Unaryop()
    else:
        print('asttype Mistake!!!')
    return None

# FOM寫入
def write_FOM(FOM_Set):
    for number, content in enumerate(FOM_Set):
        try:
            file_dir = 'AST_Mutant_Folder/AST_FOM_Folder/' + 'AST_FOM_' + str(number + 1) + '.py'
            f = open(file_dir, 'w+')
            f.write(str(astunparse.unparse(content)).replace('\n', '', 2))
            f.seek(0)
            f.close()
        except AttributeError:
            print('AttributeError')

    return None


# 清除資料夾
def clean_folder():
    file_dir = 'AST_Mutant_Folder/'
    if(os.path.isdir(file_dir) == True):
        shutil.rmtree(file_dir)
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_FOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_GA_Material_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Material_Folder'
    os.mkdir(file_dir)

    # file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder'
    # shutil.rmtree(file_dir)

    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_Equivalent_SHOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_NSHOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_SHOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_SSHOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_Useless_SHOM_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_WSHOM_Coupled_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Folder/AST_HOM_Classification_Folder/AST_WSHOM_Decoupled_Folder'
    os.mkdir(file_dir)

    file_dir = 'AST_Mutant_Killed_TestCase_Folder/'
    shutil.rmtree(file_dir)
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_FOM_Killed_TestCase_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_Mutant_Killed_TestCase_Folder/AST_HOM_Killed_TestCase_Folder'
    os.mkdir(file_dir)

    file_dir = 'AST_TestCase_Killed_Mutant_Folder/'
    shutil.rmtree(file_dir)
    os.mkdir(file_dir)
    file_dir = 'AST_TestCase_Killed_Mutant_Folder/AST_FOM_Killed_TestCase_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_TestCase_Killed_Mutant_Folder/AST_HOM_Killed_TestCase_Folder'
    os.mkdir(file_dir)

    file_dir = 'AST_TestCase_Folder/'
    shutil.rmtree(file_dir)
    os.mkdir(file_dir)
    file_dir = 'AST_TestCase_Folder/AST_FOM_TestCase_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_TestCase_Folder/AST_HOM_TestCase_Folder'
    os.mkdir(file_dir)

    file_dir = 'AST_TestCase_Result_Folder/'
    shutil.rmtree(file_dir)
    os.mkdir(file_dir)
    file_dir = 'AST_TestCase_Result_Folder/AST_FOM_TestCase_Result_Folder'
    os.mkdir(file_dir)
    file_dir = 'AST_TestCase_Result_Folder/AST_HOM_TestCase_Result_Folder'
    os.mkdir(file_dir)

    return None

# ----------------------------------------------------------
# 執行
# ----------------------------------------------------------
# ----------------------------------------------------------
# FOM 生成(Binop)
# ----------------------------------------------------------
clean_folder()


# ----------------------------------------------------------
# FOM 生成(Binop)
# ----------------------------------------------------------
create_FOM('Binop')

# 重置
temp_FOM = None
want_node_pos = 0
temp_node = []
temp_node_pos = 0
temp_FOM_Set_Add = False
temp_record = []
temp_node_count = 0

# ----------------------------------------------------------
# FOM 生成(Compare)
# ----------------------------------------------------------
create_FOM('Compare')

# 重置
temp_FOM = None
want_node_pos = 0
temp_node = []
temp_node_pos = 0
temp_FOM_Set_Add = False
temp_record = []
compare_ischange = False
temp_node_count = 0

# ----------------------------------------------------------
# FOM 生成(Unaryop)
# ----------------------------------------------------------
create_FOM('Unaryop')


# ----------------------------------------------------------
# 印出訊息
# ----------------------------------------------------------
print('FOM_Set(Count): ', len(FOM_Set))
print()
print('FOM_binop_record(Count): ', len(FOM_binop_record))
print('FOM_binop_record: ', FOM_binop_record)
print()
print('FOM_compare_record(Count): ', len(FOM_compare_record))
print('FOM_compare_record: ', FOM_compare_record)
print()
print('FOM_unaryop_record(Count): ', len(FOM_unaryop_record))
print('FOM_unaryop_record: ', FOM_unaryop_record)

# ----------------------------------------------------------
# FOM寫入
# ----------------------------------------------------------
write_FOM(FOM_Set)
