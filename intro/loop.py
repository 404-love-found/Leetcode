'''
# range(n) 生成 0 到 n-1 的整数序列
# 输出：0 1 2 3 4

input_str = input("请输入一个整数：")
n = int(input_str)
for i in range(n):
    print(i, end=' ')

'''


# range(start, end) 生成 start 到 end-1
# 输出：2 3 4 5 6
for i in range(2, 7):
    print(i, end=" ")
print()

# range(start, end, step) 带步长
# 输出：0 2 4 6 8
for i in range(0, 10, 2):
    print(i, end=" ")
print()

# 倒序遍历
# 输出：5 4 3 2 1
for i in range(5, 0, -1):
    print(i, end=" ")
print()