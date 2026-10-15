#队列是"先进先出"（FIFO）的数据结构，在 BFS（广度优先搜索）中必用。
#Python 用 collections.deque（双端队列）来实现高效的队列操作。
#你可能会想：用列表不行吗？用列表的 pop(0) 也能实现出队，
#但 pop(0) 需要把后面所有元素往前移一位，时间复杂度 O(n)。
#而 deque 的 popleft 是 O(1) 的，效率高得多。


from collections import deque

queue = deque()

queue.append(1)
queue.append(2)
queue.append(3)
print("入队后：", queue)

front = queue.popleft()
print("从左端弹出元素：", front)
print("出队后：", queue)
print("队列长度：", len(queue))
front1 = queue.pop()
print("从右端弹出元素：", front1)
print("出队后：", queue)
print("队列长度：", len(queue))

queue.appendleft(0)
print("从左端入队元素：", queue[0])
print("入队后：", queue)


#BFS 层序遍历
# 用邻接表表示一个图
# 0 -> 1, 2
# 1 -> 3
# 2 -> 3, 4
graph = {
    0: [1, 2],
    1: [3],
    2: [3, 4],
    3: [],
    4: [],
}

deque = deque()
visited = set()
#定义集合和队列

deque.append(0)#从 0 开始
visited.add(0)#从 0 开始访问

stack = []

while deque:
    node = deque.popleft()
    stack.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            deque.append(neighbor)