'''
字典是 Python 中的哈希表实现，存储键值对，增删查改都很快（平均 O(1)）
'''

# 创建字典
d = {"apple": 3, "banana": 5, "cherry": 2}

print(d["apple"])#取值

print("旧字典：", d)
# 赋值（key 存在就修改，不存在就新增）
d["apple"] = 10
d["grape"] = 7
print("新字典：", d)

# in 判断 key 是否存在
print("banana" in d)  # True
print("orange" in d)  # False


#del 删除键值对
del d["cherry"]
print("删除 cherry 后的字典：", d)

# 遍历 key-value 对（最常用）
for key, val in d.items():
    print(f"{key}: {val}", end="  ")
print()

# 只遍历 values
print("只遍历 values：", list(d.values()))
print("只遍历 values：", sum(d.values()))