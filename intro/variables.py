'''
#None 表示"什么都没有"，判断一个变量是否为 None 推荐用 is 而不是 ==：
result = None
if result is None:
    print("还没有结果")
'''

'''
# bool()：转成布尔值
# 0、0.0、空字符串、None 是 False，其他都是 True
print(bool(0))      # False
print(bool(""))     # False
print(bool(42))     # True
print(bool("hi"))   # True
'''


'''
# 逻辑运算符用英文单词 and、or、not
# and：两个都为真才是真
print(a > 5 and b > 15)    # True
# or：有一个为真就是真
print(a > 100 or b > 15)   # True
# not：取反
print(not (a > 100))        # True
'''

'''
#按位与（Bitwise AND）运算
#在二进制中，偶数的最后一位永远是 0，奇数的最后一位永远是 1

a = 10  # 二进制 1010
b = 12  # 二进制 1100

# & 按位与：两个都是 1 才是 1
# 1010 & 1100 = 1000（十进制 8）
print(f"{a} & {b} = {a & b}")

# | 按位或：有一个是 1 就是 1
# 1010 | 1100 = 1110（十进制 14）
print(f"{a} | {b} = {a | b}")

# ^ 按位异或：不同为 1，相同为 0
# 1010 ^ 1100 = 0110（十进制 6）
print(f"{a} ^ {b} = {a ^ b}")

# ~ 按位取反
print(f"~{a} = {~a}")  # -11

# << 左移（相当于乘以 2）
print(f"{a} << 1 = {a << 1}")  # 20

# >> 右移（相当于除以 2）
print(f"{a} >> 1 = {a >> 1}")  # 5

'''


n = 7
if (n & 1) == 1: #按位与运算符 & 的规则是：只有对应的两个二进制位都为 1 时，结果才为 1，否则为 0
    print(f"{n} 是奇数")
else:
    print(f"{n} 是偶数")
