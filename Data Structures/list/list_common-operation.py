cols ,rows = 3,4
grid = [[0] * cols for _ in range(rows)]

print("Initial grid:",grid)

grid.append([1, 2])
grid.append([3, 4])

print("After appending new rows:",grid)

print(rows)
print(cols)
