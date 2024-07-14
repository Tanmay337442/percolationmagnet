import random
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

p = 0.5
size = 4

def generatearray(x, y, z):
    return [[[0 if random.random() < p else 1 for _ in range(x)] for _ in range(y)] for _ in range(z)]

def showarray(array):
    for i in array:
        for j in i:
            print(j)
        print()

array = [
    [
        [0, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ],
    [
        [0, 1, 1, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ],
    [
        [1, 1, 1, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ],
    [
        [1, 1, 1, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]
]
# array = generatearray(size, size, size)
showarray(array)

def percolates(array):
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    queue = deque([(0, y, z) for y in range(size) for z in range(size) if not array[0][y][z]])
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    
    while queue:
        x, y, z = queue.popleft()
        if x == size - 1:
            return True
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            if ny < 0:
                ny = size - 1
            elif ny >= size:
                ny = 0
            
            if nz < 0:
                nz = size - 1
            elif nz >= size:
                nz = 0

            if not array[nx][ny][nz] and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                queue.append((nx, ny, nz))
    
    queue = deque([(x, 0, z) for x in range(size) for z in range(size) if not array[x][0][z]])
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    
    while queue:
        x, y, z = queue.popleft()
        if y == size - 1:
            return True
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            if nx < 0:
                nx = size - 1
            elif nx >= size:
                nx = 0
            
            if nz < 0:
                nz = size - 1
            elif nz >= size:
                nz = 0

            if not array[nx][ny][nz] and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                queue.append((nx, ny, nz))

    queue = deque([(x, y, 0) for x in range(size) for y in range(size) if not array[x][y][0]])
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    
    while queue:
        x, y, z = queue.popleft()
        if z == size - 1:
            return True
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            if nx < 0:
                nx = size - 1
            elif nx >= size:
                nx = 0
            
            if ny < 0:
                ny = size - 1
            elif ny >= size:
                ny = 0

            if not array[nx][ny][nz] and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                queue.append((nx, ny, nz))
    
    return False

print(percolates(array))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for x in range(size):
    for y in range(size):
        for z in range(size):
            if array[x][y][z] == 0:
                ax.scatter(x, y, z, c='b', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.axes.set_xlim3d(left=0, right=size-1) 
ax.axes.set_ylim3d(bottom=0, top=size-1) 
ax.axes.set_zlim3d(bottom=0, top=size-1) 
ax.set_title('3D Grid Visualization')

plt.show()