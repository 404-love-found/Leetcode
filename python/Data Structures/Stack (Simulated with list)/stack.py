'''
栈是"后进先出"（LIFO）的数据结构。
Python 没有专门的栈类型，直接用列表就能模拟
'''

from inspect import stack


'''
stack = []

# 入栈
stack.append(1)
stack.append(2)
stack.append(3)
print("入栈后：", stack)

# 查看栈顶元素（不删除）
print("栈顶元素：", stack[-1])

# 出栈(删除并返回栈顶元素)
top = stack.pop()
print("出栈元素：", top)


# 全部出栈
stack.pop()
stack.pop()
print("全部出栈后：", len(stack)==0)
#判空：len(stack) == 0

'''
                #经典例子——括号匹配：
def is_valid(s):
        stack = []
        pairs = {")": "(", "}": "{", "]": "["}
        for ch in s:
                if ch in '({[':
                       stack.append(ch)
                else:
                       if not stack or stack[-1] != pairs[ch]: 
                #stack[-1] 是 Python 列表的负索引语法，-1 表示最后一个元素
                               return False
                       stack.pop()
        return len(stack) == 0

input_str =input("请输入括号字符串：")
print("括号匹配结果：", is_valid(input_str))

          


