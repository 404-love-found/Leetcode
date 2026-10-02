cols ,rows = 2,3
grid = [[0] * cols for _ in range(rows)]
print(grid)  # 输出：[[0, 0], [0, 0], [0, 0]]

grid.append([1, 2])
grid.append([3, 4])
print(grid)
