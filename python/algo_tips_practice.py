"""
配套练习：labuladong「算法题常用技巧」
https://labuladong.online/zh/programming-language/py/algo-tips/

规则：每个函数只用 1~3 行代码写完，把 pass 删掉换成你的代码。
运行：python algo_tips_practice.py   —— 每题会显示 ✓ 或 ✗，可以一题一题地做。
"""
from collections import Counter, defaultdict
from bisect import bisect_left


# 练习 1：多级排序（元组 key）
# records 是 [(名字, 分数), ...]，按 分数从高到低 排；分数相同时按 名字字母顺序 排。
# 返回排好序的新列表（不要改动原列表 → sorted 还是 .sort()？）
def sort_students(records):
    pass


# 练习 2：Counter + min 带 key
# 返回字符串 s 中出现次数最多的字符；如果有并列，返回字母顺序最小的那个。
# 例："bbaac" -> 'a'（a 和 b 都出现 2 次，a 更小）
def most_frequent_char(s):
    pass


# 练习 3：defaultdict(list)
# 把单词按长度分组，返回 dict：{长度: [单词, ...]}，组内保持原来的顺序。
# 例：["hi", "cat", "go", "dog"] -> {2: ["hi", "go"], 3: ["cat", "dog"]}
def group_by_length(words):
    pass


# 练习 4：min 带 key + 元组
# 返回 nums 中最接近 0 的数；如果距离相同（比如 -2 和 2），返回正数。
def closest_to_zero(nums):
    pass


# 练习 5：整除陷阱
# 实现「向零取整」的整数除法：7/2 -> 3，-7/2 -> -3（注意：-7 // 2 等于 -4！）
# 这个陷阱在 LeetCode 150「逆波兰表达式求值」里会遇到。
def div_toward_zero(a, b):
    pass


# 练习 6：bisect
# sorted_nums 是升序列表，返回其中「严格小于 x」的元素个数，要求 O(log n)。
def count_less_than(sorted_nums, x):
    pass


# ---------------- 测试代码，不用改 ----------------
def _check(name, func, cases):
    try:
        for args, expected in cases:
            got = func(*args)
            if got != expected:
                print(f"✗ {name}: 输入 {args} 期望 {expected!r}，你返回了 {got!r}")
                return False
    except Exception as e:
        print(f"✗ {name}: 运行出错 {type(e).__name__}: {e}")
        return False
    print(f"✓ {name}")
    return True


if __name__ == "__main__":
    original = [("bob", 90), ("amy", 95), ("cat", 90)]
    results = [
        _check("练习1 sort_students", sort_students, [
            ((original,), [("amy", 95), ("bob", 90), ("cat", 90)]),
        ]),
        _check("练习2 most_frequent_char", most_frequent_char, [
            (("bbaac",), "a"), (("hello",), "l"), (("z",), "z"),
        ]),
        _check("练习3 group_by_length", lambda w: dict(group_by_length(w) or {}), [
            ((["hi", "cat", "go", "dog"],), {2: ["hi", "go"], 3: ["cat", "dog"]}),
            (([],), {}),
        ]),
        _check("练习4 closest_to_zero", closest_to_zero, [
            (([5, -3, 4],), -3), (([-2, 2, 7],), 2), (([0, 1],), 0),
        ]),
        _check("练习5 div_toward_zero", div_toward_zero, [
            ((7, 2), 3), ((-7, 2), -3), ((7, -2), -3), ((-6, 3), -2),
        ]),
        _check("练习6 count_less_than", count_less_than, [
            (([1, 2, 2, 2, 5], 2), 1), (([1, 3, 5], 6), 3), (([1, 3, 5], 0), 0),
        ]),
    ]
    if original != [("bob", 90), ("amy", 95), ("cat", 90)]:
        print("⚠ 练习1 把原列表改掉了！题目要求返回新列表")
    print(f"\n通过 {sum(results)}/{len(results)}")
