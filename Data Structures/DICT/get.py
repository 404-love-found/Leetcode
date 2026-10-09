d ={"apple":3 , "berry":5}
'''
直接用 d[key] 取值时，如果 key 不存在会报 KeyError。
用 get 方法可以避免这个问题
'''

print(d.get("apple"))  # 输出: 3
print(d.get("orange", 0))  # 输出：0（key 不存在，返回默认值 0）


# 频率统计的经典写法
text = input("请输入一段文本：")
freq = {}
for ch in text:
    freq[ch]= freq.get(ch, 0) + 1
    # 如果 ch 不在字典中，get 返回 0，加 1 后就是 1
print(freq)

print("最大频率的字符及其频率：",max(freq.items(), key=lambda x: x[1]))  # 输出频率最高的字符及其频率