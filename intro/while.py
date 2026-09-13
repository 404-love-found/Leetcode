# 计算 1 + 2 + ... + 100
'''
x = 1
y = 0
while x <= 100:
    y += x # y += x（状态累积）等价展开：y = y + x
    x += 1
print(y)
'''

# 高级内置写法（一行搞定，运行速度更快，且杜绝越界与死循环风险）
'''
total = sum(range(1, 101))
print(total)
'''

#注意 Python 没有 do-while 循环，也没有 i++ 的写法，自增只能写 i += 1
# break 和 continue
# break 立刻跳出整个循环，continue 跳过当前这一轮、进入下一轮



# Python 代码出错时会抛出异常，用 try-except 把它接住继续运行，否则程序会直接停下来
# 异常处理四件套演示：try / except / else / finally
#四件套分工清楚：try 放可能出错的代码，except 匹配并处理异常。else 在没出错时才执行，常放只在成功路径上跑的收尾逻辑；finally 无论成功失败都跑，常用来释放资源
'''
def sum_to_n(n):
    # 防御性检查
    if not isinstance(n, int):
        raise TypeError(f"目标值必须是整型，实际传入的是 {type(n).__name__}")
    if n < 1:
        raise ValueError("计算范围必须是大于等于 1 的正整数")
    
    return sum(range(1, n + 1))


target = int(input("请输入一个正整数作为求和的目标值: "))

try:
    # 1. try: 尝试执行计算
    result = sum_to_n(target)
except (TypeError, ValueError) as e:
    # 2. except: 捕获参数类型或数值范围错误
    print(f"输入有误，计算失败: {e}")
else:
    # 3. else: 没有抛出异常时打印计算结果
    print(f"1 加到 {target} 的结果是: {result}")
finally:
    # 4. finally: 无论成功还是失败都会执行
    print("求和任务执行完毕。")
'''