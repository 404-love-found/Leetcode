#input().split() 基本用法
'''
n = int(input())
for i in range(n):
    nums = list(map(int, input().split()))
    print(sum(nums))
'''


#sys.stdin 快读（大数据量）
#当输入数据量很大比如几十万行，input() 可能会超时。这时候需要用 sys.stdin 来加速读取。

import sys
input = sys.stdin.readline 
dict = {}

for i in dict:
    print(i, dict[i])







