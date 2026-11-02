#元组和列表长得很像，但有一个关键区别：元组创建后不能修改
# 创建元组，用小括号
t = (1, 2, 3)
print(t[0]) 

# 元组拆包：把元组的值分别赋给多个变量
a,b, c = (4,5,6)
print(a,b,c)

'''
既然元组不能修改，那为什么还要用它呢？
元组在刷题中主要有三个用途：
1.多返回值：函数返回多个值时，实际上返回的是元组，用拆包接收
2.字典的键：列表不能当字典的键（因为可变），但元组可以
3.排序的 key：用元组做排序的 key 可以实现多级排序，比如 key=lambda x: (x[1], x[0])
'''


#用途一：多返回值
def min_max(nums):
    return min(nums),max(nums)

low,high = min_max([1,2,3,4,5]) #返回一个元组
print(low,high) #拆包接收元组的值

# 用途二：元组可以当字典的键
# 比如用 (行, 列) 坐标作为 key
visited = {}
visited[(0, 0)] = True
visited[(1, 2)] = True
print((0, 0) in visited)

# 用途三：多级排序
# 先按成绩降序，成绩相同按姓名升序
students = [("Alice", 88), ("Bob", 95), ("Charlie", 88), ("Diana", 95)]
students.sort(key=lambda x: (-x[1], x[0]))
print(students)
#多级排序这个技巧非常实用：元组在比较时会先比第一个元素，相等再比第二个，以此类推。想要降序就取负号。
