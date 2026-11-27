"""
LeetCode 1. 两数之和 (Two Sum)

题目：
    给定整数数组 nums 和整数 target，找出和为 target 的两个数，返回它们的下标。
    每个输入只有一个答案；同一个元素不能用两次。

示例：
    nums = [2, 7, 11, 15], target = 9  ->  [0, 1]   (因为 2 + 7 = 9)

任务：
    1. 先写 two_sum_brute（暴力解法），并在下面写出时间/空间复杂度
    2. 再写 two_sum_hash（用 dict），目标是 O(n)
    3. 运行本文件：python lc0001_two_sum.py ，看到 "全部通过" 就成功了

复杂度（自己填）：
    暴力：时间 O(?)  空间 O(?)
    哈希：时间 O(?)  空间 O(?)
"""


def two_sum_brute(nums, target):
    # 提示：两层循环，j 从 i + 1 开始（为什么不是从 0 开始？）
    pass


def two_sum_hash(nums, target):
    # 提示：一边遍历，一边把 "数值 -> 下标" 存进 dict
    #       对当前的数 x，你需要找的另一半是什么？它在不在 dict 里？
    pass


# ---------------- 测试代码，不用改 ----------------
if __name__ == "__main__":
    tests = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([-1, -2, -3, -4, -5], -8, [2, 4]),
    ]
    for func in (two_sum_brute, two_sum_hash):
        for nums, target, expected in tests:
            result = func(nums, target)
            ok = result is not None and sorted(result) == expected
            print(f"{func.__name__:15} nums={nums}, target={target} -> {result}  {'✓' if ok else '✗ 期望 ' + str(expected)}")
            assert ok, "有测试没通过，检查一下上面打 ✗ 的那一行"
    print("全部通过！")
