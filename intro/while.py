# 计算 1 + 2 + ... + 100
x = 1
y = 0
while x <= 100:
    y += x # y += x（状态累积）等价展开：y = y + x
    x += 1
print(y)


total = sum(range(1, 101))# 高级内置写法（一行搞定，运行速度更快，且杜绝越界与死循环风险）
print(total)

