#列表是 Python 中最基础、最常用的数据结构，你可以把它理解为"可变长度的数组"。
#几乎所有算法题都离不开它
# 方式一：直接用方括号创建
nums = [1, 2, 3, 4, 5]
# 输出：[1, 2, 3, 4, 5]
print(nums)

# 方式二：创建空列表
empty = []
# 输出：[]
print(empty)

# 方式三：用 * 快速创建指定长度的列表
# 创建长度为 5 的列表，初始值都是 0
zeros = [0] * 5
# 输出：[0, 0, 0, 0, 0]
print(zeros)

# 方式四：列表推导式创建二维列表（最重要！）
# 创建 3 行 4 列的二维列表，初始值为 0
rows, cols = 3, 4
grid = [[0] * cols for _ in range(rows)]
# 输出：[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
print(grid)

# 修改某个元素验证独立性
grid[1][2] = 99
# 输出：[[0, 0, 0, 0], [0, 0, 99, 0], [0, 0, 0, 0]]
# 只有 grid[1] 变了，其他行不受影响
print(grid)

'''
这里要特别强调一个经典的坑：创建二维列表千万不能用 [[0]*4]*3。
因为 *3 复制的是引用，三行指向的是同一个列表对象，修改一行其他行也会跟着变。
用列表推导式 [[0]*cols for _ in range(rows)] 才是正确做法，每行都是独立的列表对象。
这个坑在刷算法题时非常容易踩，一定要记住。
'''


last = nums.pop(2)#删除并提取索引位置为 2 的元素
print("After popping index 2:", nums) 
print("Popped element:", last)


# insert(i, x)：在索引 i 处插入元素 x
new = nums.insert(2, 99)
print("After inserting 99 at index 2:", nums)

# del：删除指定索引的元素
del nums[1]
print(nums)


'''
append 和 pop 是刷题时用得最多的两个操作，它们操作的都是列表末尾，时间复杂度 O(1)。
而 pop(i)、insert(i, x)、del 操作的是中间位置，需要移动元素，时间复杂度 O(n)
'''

