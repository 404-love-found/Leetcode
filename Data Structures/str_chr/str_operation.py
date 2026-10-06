'''
Python 的字符串也是不可变的——你不能修改字符串中的某个字符，想修改就只能创建新字符串。
'''

s = "Hello, Python!"

# 想修改？转成列表再转回来
chars = list(s)
chars[0] = 'h'
s_new = "".join(chars)# join：把列表用分隔符连接成字符串
print(s_new)

print(s.strip())  #strip：去除两端空白字符  

print(s.split(',')) #split：按逗号分割成列表

print(s.split()) #split：按空白字符分割成列表

print(s.find('Python')) #find：查找子串，返回索引，找不到返回 -1
print(s.find('Java')) #找不到返回 -1

print(s.replace('Python', 'Java')) #replace：替换子串，返回新字符串

'''
刷题时最常用的字符串方法：
split 用于解析输入
join 用于拼接输出
find 用于查找子串
strip 用于去除多余空白
'''


