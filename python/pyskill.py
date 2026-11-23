'''
#input().split() 基本用法
n = int(input())
for i in range(n):
    nums = list(map(int, input().split()))
    print(sum(nums))
'''


#sys.stdin 快读（大数据量）
import sys
input = sys.stdin.readline

