# Python 刷题常用技巧（整理自 labuladong「算法题常用技巧」）


## 第 1 课 排序 ⭐⭐⭐

```python
nums = [3, 1, 2]
new = sorted(nums)          # 返回新列表 [1, 2, 3]，nums 不变
nums.sort()                 # 原地排序，返回 None；nums 变成 [1, 2, 3]
nums.sort(reverse=True)     # 降序 [3, 2, 1]

# key：告诉 Python「按什么比较」
words = ["banana", "kiwi", "apple"]
sorted(words, key=len)                  # 按长度：['kiwi', 'apple', 'banana']
sorted(words, key=lambda w: w[-1])      # 按最后一个字母：['banana', 'apple', 'kiwi']

# 多级排序：key 返回元组，先比第 1 个元素，相等再比第 2 个
students = [("bob", 90), ("amy", 95), ("cat", 90)]
sorted(students, key=lambda x: (-x[1], x[0]))
# 分数降序（取负号），分数相同按名字升序 → [('amy', 95), ('bob', 90), ('cat', 90)]

# 区间题常见写法：按起点排序
intervals = [[3, 5], [1, 4], [2, 6]]
intervals.sort(key=lambda x: x[0])      # [[1, 4], [2, 6], [3, 5]]
```

```python
# cmp_to_key：只有「必须两个两个比较才能决定顺序」时才用（例：LeetCode 179 最大数）
from functools import cmp_to_key
def cmp(a, b):              # 返回负数：a 排前面；正数：b 排前面；0：相等
    if a + b > b + a: return -1
    if a + b < b + a: return 1
    return 0
strs = ["3", "30", "34", "5", "9"]
"".join(sorted(strs, key=cmp_to_key(cmp)))   # '9534330'
```

## 第 2 课 常用内置函数 ⭐⭐⭐

```python
nums = [3, -7, 2]
max(nums), min(nums), sum(nums), abs(-5)    # 3 -7 -2 5
max(3, 8)                                   # 也可以直接传多个数：8

# max/min 也能带 key
words = ["kiwi", "banana", "fig"]
max(words, key=len)                         # 'banana'
min(nums, key=abs)                          # 2（绝对值最小）

# 不知道最小值是多少时，用无穷大做初始值
best = float('inf')                         # 求最小值时的初始值
worst = float('-inf')                       # 求最大值时的初始值
for x in nums:
    best = min(best, x)

divmod(17, 5)                               # (3, 2)：商和余数一次算出来
pow(2, 10)                                  # 1024
pow(2, 10, 1000)                            # 24：(2**10) % 1000，内部用快速幂
MOD = 10**9 + 7                             # 「答案对 1e9+7 取模」时的标准写法
```

## 第 3 课 整数特性 ⭐⭐

```python
2 ** 100                    # Python 整数不会溢出，可以任意大

# // 是向下取整（往负无穷方向），不是向零取整！
7 // 2                      # 3
-7 // 2                     # -4  ← 陷阱
int(-7 / 2)                 # -3  ← 需要向零取整时这样写（LeetCode 150）
-7 % 2                      # 1   （Python 的 % 结果总是和除数同号）
```

## 第 4 课 Counter：计数 ⭐⭐⭐

```python
from collections import Counter
cnt = Counter("banana")         # Counter({'a': 3, 'n': 2, 'b': 1})
cnt['a']                        # 3
cnt['z']                        # 0  ← 不存在的键返回 0，不会报错
cnt.most_common(2)              # [('a', 3), ('n', 2)]：出现次数最多的 2 个
Counter("listen") == Counter("silent")   # True → 判断字母异位词只需要一行（LeetCode 242）

cnt['a'] -= 1                   # 可以像字典一样修改
```

## 第 5 课 defaultdict：自带默认值的字典 ⭐⭐⭐

```python
from collections import defaultdict

# 普通 dict：要先判断键在不在
groups = {}
for w in ["eat", "tea", "tan"]:
    key = "".join(sorted(w))
    if key not in groups:
        groups[key] = []
    groups[key].append(w)

# defaultdict(list)：键不存在时自动创建 []，可以直接 append
groups = defaultdict(list)
for w in ["eat", "tea", "tan"]:
    groups["".join(sorted(w))].append(w)
# {'aet': ['eat', 'tea'], 'ant': ['tan']}   ← LeetCode 49 的核心写法

# 图论题建邻接表
graph = defaultdict(list)
for u, v in [(0, 1), (0, 2), (1, 2)]:
    graph[u].append(v)
    graph[v].append(u)

freq = defaultdict(int)         # 默认值 0，用来计数（简单计数直接用 Counter 更方便）
```

## 第 6 课 bisect：二分查找 ⭐⭐

```python
from bisect import bisect_left, bisect_right, insort
a = [1, 2, 2, 2, 5]             # 必须是已经排好序的列表！
bisect_left(a, 2)               # 1：第一个 >= 2 的位置（左边界）
bisect_right(a, 2)              # 4：第一个 > 2 的位置（右边界）
bisect_right(a, 2) - bisect_left(a, 2)   # 3：2 出现了几次
bisect_left(a, 3)               # 4：3 应该插在哪里
insort(a, 3)                    # 插入后仍然有序：[1, 2, 2, 2, 3, 5]
```

## 第 7 课 math 模块与进制转换 ⭐

```python
import math
math.ceil(7 / 2)                # 4：向上取整
math.floor(7 / 2)               # 3
math.sqrt(16)                   # 4.0
math.isqrt(17)                  # 4：整数平方根
math.gcd(12, 18)                # 6：最大公约数
math.inf                        # 和 float('inf') 一样
(7 + 2 - 1) // 2                # 4：整数向上取整的常用技巧，不用 import

bin(10)                         # '0b1010'
bin(10)[2:]                     # '1010'：去掉 '0b' 前缀
int("1010", 2)                  # 10：二进制字符串转成十进制
hex(255), oct(8)                # '0xff' '0o10'
bin(10).count('1')              # 2：二进制里有几个 1
```

## 第 8 课 ACM 模式输入输出（国内笔试用） ⭐⭐

```python
import sys
input = sys.stdin.readline      # 加速读取：数据有几十万行时一定要加

n = int(input())                        # 读一个整数
a, b = map(int, input().split())        # 一行里读两个整数
nums = list(map(int, input().split()))  # 一行里读整个列表
s = input().strip()                     # 读字符串时要 strip() 去掉末尾的 '\n'

# 不知道一共有多少行：读到文件末尾（EOF）为止
for line in sys.stdin:
    a, b = map(int, line.split())
    print(a + b)

# 输出：用空格隔开一个列表
print(*nums)                    # 1 2 3
print(" ".join(map(str, nums))) # 和上面一样
```
