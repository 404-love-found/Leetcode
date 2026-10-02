from faker import Faker
import random

#Python 用 def 关键字定义函数
#注意 Python 不需要声明参数类型和返回值类型——因为 Python 是动态类型语言，变量的类型在运行时自动确定。你传什么进去，它就是什么类型。
#还有一点，Python 是用缩进来划分代码块的。def 下面缩进的部分就是函数体，缩进结束函数就结束了。一般用 4 个空格缩进


#默认参数:定义函数时可以给参数设置默认值，调用时如果不传这个参数，就用默认值


#可变参数 
#有时候你不确定函数会接收多少个参数,Python 提供了两种方式来处理：
#  语法	        说明
#  *args	        接收任意多个位置参数，打包成一个元组（类似列表但不可修改，下一篇会讲）
#  **kwargs	    接收任意多个关键字参数，打包成一个字典



#                                                     可变参数 *args 
'''
def my_sum(*args):
    print(args)  # 打印传入的参数，args 是一个元组
    total = 0
    for num in args:
        total += num
    return total


print(my_sum(1, 2, 3))  # 输出: 6
'''


#                                                   可变参数 **kwargs
# **kwargs 把多余的关键字参数打包成字典
'''
def print_info(**kwargs):
    print("收到的参数：", kwargs)
    for key, value in kwargs.items():  #要同时拿键和值
        print(f"  {key} = {value}")


# 2. 在函数内部拿所有的键（Key）
    print("所有键：", list(kwargs.keys()))    

    # 3. 在函数内部拿所有的值（Value）
    print("所有值：", list(kwargs.values()))

# 调用函数（参数名 name 和 age 就会成为字典里的 key）
print_info(name="张三", age=23)

'''


#   安全取值：kwargs.get(key, 默认值)（极高频）
#   如果你直接用中括号 kwargs["gender"] 取一个不存在的键，程序会直接崩溃报错（KeyError）。
#   用 .get() 可以安全读取，如果找不到就返回默认值（不写默认值就返回 None）：
#   如果用户传了 'country'，就用用户传的；如果没传，默认就是 '未知国家'

'''
def print_info(**kwargs):
    print("收到的原始参数：", kwargs)
    
    # 遍历打印传入的所有键值对
    for key, value in kwargs.items():
        print(f"  {key} = {value}")

    # 使用 kwargs.get(key, 默认值) 安全提取可能没有传的参数
    # 如果用户传了 'country'，就用用户传的；如果没传，默认就是 '未知国家'
    country = kwargs.get("country", "未知国家")
    
    # 如果用户传了 'role'（角色），没传默认是 '普通用户'
    role = kwargs.get("role", "普通用户")
    
    print(f"--> 解析结果：国家是【{country}】，身份是【{role}】\n")


# ---------------- 测试调用 ----------------

# 情况 1：没有传 country，也没有传 role
print("【第 1 次调用】")
print_info(name="张三", age=18)

# 情况 2：传了 country，但依然没有传 role
print("【第 2 次调用】")
print_info(name="李四", age=22, country="加拿大")

#*args 和 **kwargs 只是约定俗成的名字，你也可以叫 *numbers 或 **options，关键是前面的 * 和 **
'''


#                                                                       多返回值
'''
#Python 的函数可以返回多个值，本质上是返回一个元组，然后用拆包的方式接收.多返回值在刷算法题时很实用，比如一个函数既要返回最大值，又要返回最大值的下标，用多返回值就很方便

def get_max_and_index(numbers):
    return a,b

# 返回商和余数
def divide(a, b):
    return a // b, a % b

# 用两个变量接收两个返回值（元组拆包）
q, r = divide(10, 3)
# 输出：商 = 3, 余数 = 1
print(f"商 = {q}, 余数 = {r}")

# 其实返回的是一个元组
result = divide(10, 3)
# 输出：(3, 1)
print(result)

'''

#                                                                  lambda 表达式
#                                                lambda 是一种创建匿名函数的简洁写法，适合写那些只用一次的简单函数
'''
def add_func(a,b):
    return a + b

lam_func = lambda a, b: a * b

print("C is ",add_func(1, 2))
print("C is ",lam_func(1, 2))

# 一组学生，每个人是 (姓名, 成绩) 的元组
students = [("Alice", 88), ("Bob", 95), ("Charlie", 72), ("Diana", 91)]

# 按成绩从高到低排序
# key 参数告诉 sorted 用什么规则排序
# lambda x: x[1] 表示取每个元组的第二个元素（成绩）
ranked = sorted(students, key=lambda x: x[1], reverse=True)
# 输出：[('Bob', 95), ('Diana', 91), ('Alice', 88), ('Charlie', 72)]
print(ranked)

# 按姓名长度排序
by_name_len = sorted(students, key=lambda x: len(x[0]))
# 输出：[('Bob', 95), ('Alice', 88), ('Diana', 91), ('Charlie', 72)]
print(by_name_len)

# 对普通列表也行：按绝对值排序
nums = [-3, 1, -4, 1, 5, -9, 2, -6]
sorted_nums = sorted(nums, key=lambda x: abs(x))
# 输出：[1, 1, 2, -3, -4, 5, -6, -9]
print(sorted_nums)
#刷算法题时 sorted + lambda 的组合用得非常频繁，一定要熟练掌握。
'''


#                     列表推导式（List Comprehension）: Python 中非常有特色的语法，能用一行代码生成一个列表。


#(1)生成 0~9 每个数的平方
'''
squares = [x**2 for x in range(10)]
print(squares)  
'''

# 生成字符串列表
'''
fake = Faker()
# 1. 生成包含 (姓名) 的列表
students = [fake.first_name() for _ in range(random.randint(1,100))]

# 2. 一步到位：提取名字并直接转换成大写
upper_names = [student.upper() for student in students]
print(upper_names)
'''



#                                               嵌套推导式
#                                       列表推导式可以嵌套，最常见的用途是创建二维列表

# 创建 3 行 4 列的二维列表，初始值都是 0
# 外层循环 3 次（行），内层循环 4 次（列）
'''
matrix = [[0 for j in range(4)] for i in range(3)]

for row in matrix:
    print(row)

'''
#这里要特别注意一个坑：创建二维列表不能用 [[0]*4]*3 这种写法。
#因为 *3 复制的是引用，三行指向的是同一个列表对象，修改一行其他行也会变。
#用列表推导式 [[0 for j in range(4)] for i in range(3)] 才是正确的做法，每行都是独立的列表。
#这个坑在刷算法题时非常容易踩，一定要记住。


#字典推导式 / 集合推导式
#既然列表有推导式，字典和集合自然也有。语法几乎一样，只是把 [] 换成 {}
#:是 Python 字典中用来分隔“键 (Key)”和“值 (Value)”的专属符号。

# 集合推导式：{表达式 for 变量 in 可迭代对象}
# 注意集合会自动去重
''''
nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x ** 2 for x in nums}
# 输出：{16, 1, 4, 9}（集合无序）
print(unique_squares)
'''