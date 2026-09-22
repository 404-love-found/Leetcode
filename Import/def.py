#Python 用 def 关键字定义函数
#注意 Python 不需要声明参数类型和返回值类型——因为 Python 是动态类型语言，变量的类型在运行时自动确定。你传什么进去，它就是什么类型。
#还有一点，Python 是用缩进来划分代码块的。def 下面缩进的部分就是函数体，缩进结束函数就结束了。一般用 4 个空格缩进


#默认参数:定义函数时可以给参数设置默认值，调用时如果不传这个参数，就用默认值


#可变参数 
#有时候你不确定函数会接收多少个参数,Python 提供了两种方式来处理：
#  语法	        说明
#  *args	        接收任意多个位置参数，打包成一个元组（类似列表但不可修改，下一篇会讲）
#  **kwargs	    接收任意多个关键字参数，打包成一个字典



#可变参数 *args 
'''
def my_sum(*args):
    print(args)  # 打印传入的参数，args 是一个元组
    total = 0
    for num in args:
        total += num
    return total


print(my_sum(1, 2, 3))  # 输出: 6
'''


#可变参数 **kwargs
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

#安全取值：kwargs.get(key, 默认值)（极高频）
#如果你直接用中括号 kwargs["gender"] 取一个不存在的键，程序会直接崩溃报错（KeyError）。
#用 .get() 可以安全读取，如果找不到就返回默认值（不写默认值就返回 None）：
# 如果用户传了 'country'，就用用户传的；如果没传，默认就是 '未知国家'
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

#多返回值
#Python 的函数可以返回多个值，本质上是返回一个元组，然后用拆包的方式接收.多返回值在刷算法题时很实用，比如一个函数既要返回最大值，又要返回最大值的下标，用多返回值就很方便
'''
def get_max_and_index(numbers):
    return a,b









'''
def add_func(a,b):
    return a + b

lam_func = lambda a, b: a * b 

print("C is ",add_func(1, 2)) 
print("C is ",lam_func(1, 2))
'''