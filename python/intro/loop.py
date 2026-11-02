# range(n) 生成 0 到 n-1 的整数序列
# 输出：0 1 2 3 4
'''
input_str = input("请输入一个整数：")
n = int(input_str)
for i in range(n):
    print(i, end=' ')

'''


# range(start, end) 生成 start 到 end-1
# 输出：2 3 4 5 6
'''
for i in range(2, 7):
    print(i, end=" ")
print()
'''

# range(start, end, step) 带步长
# 输出：0 2 4 6 8
'''
for i in range(0, 10, 2):
    print(i, end=" ")
print()
'''

# 倒序遍历
# 输出：5 4 3 2 1
'''
for i in range(5, 0, -1):
    print(i, end=" ")
print()
'''

#遍历列表和 enumerate
# 直接遍历列表
fruits = ["苹果", "香蕉", "橘子"]
for x in fruits:
    print(x)

print("---")

# enumerate 同时返回下标和元素
for i, x in enumerate(fruits):
    print(f"第{i}个：{x}")

print("---")

# 遍历字符串（逐个字符）
for ch in "Hello":
    print(ch, end=" ")
print()