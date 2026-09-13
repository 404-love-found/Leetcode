#input() 从控制台读取一行输入，返回的永远是字符串。
'''
age = input("请输入你的年龄：")
print(f"你输入的年龄是：{age}，类型是：{type(age)}")

age = int(input("请输入你的年龄：")) 
print(f"你输入的年龄是：{age}，类型是：{type(age)}")
'''


#一行读取多个值
'''
a,b = map(int,input("请输入两个整数，用空格隔开：").split())
print(f"你输入的两个整数是：{a}，{b}，类型分别是：{type(a)}，{type(b)}")
print(f"{a} + {b} = {a + b}")

a,b = map(str,input("请输入两个字符串，用空格隔开：").split())
print(f"你输入的两个字符串是：{a}，{b}，类型分别是：{type(a)}，{type(b)}")
print(f"{a} + {b} = {a + b}")
'''

#  这个 map(int, input().split()) 是 Python 算法题中的标准输入套路，建议记住。拆解一下：
#  input() 读取一行，比如 "3 5"
#  .split() 按空格切分成列表 ["3", "5"]
#  map(int, ...) 对列表中每个元素调用 int() 转换
#  a, b = ... 把结果拆包赋值给两个变量

'''
#如果一行有很多数字需要存到列表里，可以这样：
nums = list(map(int, input().split()))
print(nums)
print(f"共 {len(nums)} 个数，总和 = {sum(nums)}")
'''