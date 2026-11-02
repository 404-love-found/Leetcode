'''
ord(ch) - ord('a')   # 字母 → 0~25
chr(i + ord('a'))    # 0~25 → 字母
ord(ch) - ord('a') 这个技巧把小写字母映射到 0~25
非常适合用数组代替哈希表来统计字母频率。刷题时很常用。
'''

# 经典用法：用数组统计字母频率
text = "helloworld"
freq = [0] * 26
for ch in text:
    freq[ord(ch) - ord('a')] += 1

# 输出每个出现过的字母及其频率
for i in range(26):
    if freq[i] > 0:
        print(f"{chr(i + ord('a'))}: {freq[i]}", end="  ")
print()