import random
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
arrays = []
percolated = []
largestchunks = []

def generatearray(x, y, z, p):
    return [[[0 if random.random() > p else 1 for _ in range(z)] for _ in range(y)] for _ in range(x)]

""" def showarray(array):
    for i in array:
        for j in i:
            print(j)
        print() """

""" array = [
    [
        [0, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ],
    [
        [0, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ],
    [
        [1, 1, 1, 0],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ],
    [
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ]
] """
# array = generatearray(size, size, size)
# showarray(array)

def percolates(array, size):
    queue = deque([(0, y, z) for y in range(size) for z in range(size) if not array[0][y][z]])
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]

    while queue:
        x, y, z = queue.popleft()
        visited[x][y][z] = True
        if x == size - 1:
            return True
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            ny = ny % size
            nz = nz % size

            if nx > 0 and not array[nx][ny][nz] and not visited[nx][ny][nz]:
                queue.append((nx, ny, nz))

    queue = deque([(x, 0, z) for x in range(size) for z in range(size) if not array[x][0][z]])
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    
    while queue:
        x, y, z = queue.popleft()
        visited[x][y][z] = True
        if y == size - 1:
            return True
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            nx = nx % size
            nz = nz % size

            if ny > 0 and not array[nx][ny][nz] and not visited[nx][ny][nz]:
                queue.append((nx, ny, nz))

    queue = deque([(x, y, 0) for x in range(size) for y in range(size) if not array[x][y][0]])
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]

    while queue:
        x, y, z = queue.popleft()
        visited[x][y][z] = True
        if z == size - 1:
            return True
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            nx = nx % size
            ny = ny % size

            if nz > 0 and not array[nx][ny][nz] and not visited[nx][ny][nz]:
                queue.append((nx, ny, nz))

    return False

def bfs(array, start, visited, size):
    n = 0
    queue = deque([start])
    while queue:
        x, y, z = queue.popleft()
        n += 1
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

            if nz < 0:
                nz = size - 1
            elif nz >= size:
                nz = 0

            if not visited[nx][ny][nz] and not array[nx][ny][nz]:
                visited[nx][ny][nz] = True
                queue.append((nx, ny, nz))
    
    return n

def largestchunk(array, size):
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    max = 0

    for x in range(size):
        for y in range(size):
            for z in range(size):
                if not visited[x][y][z] and not array[x][y][z]:
                    visited[x][y][z] = True
                    n = bfs(array, (x, y, z), visited, size)
                    if n > max:
                        max = n
    
    return max

def calculate(size, p, trials):
    numpercolated = 0

    for _ in range(trials):
        array = generatearray(size, size, size, p)
        arrays.append(array)
        b = percolates(array, size)
        percolated.append(b)
        if b:
            numpercolated += 1
        largestchunks.append(largestchunk(array, size))

    avglargestchunk = sum(largestchunks)/len(largestchunks)
    print(f"{p}, {numpercolated}, {avglargestchunk}")
    return [numpercolated, avglargestchunk ]

for x in range(11):
    calculate(6, x/10, 10000)
    arrays = []
    percolated = []
    largestchunks = []

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# for x in range(size):
#     for y in range(size):
#         for z in range(size):
#             if array[x][y][z] == 0:
#                 ax.scatter(x, y, z, c='b', marker='o')

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.axes.set_xlim3d(left=0, right=size-1) 
# ax.axes.set_ylim3d(bottom=0, top=size-1) 
# ax.axes.set_zlim3d(bottom=0, top=size-1) 
# ax.set_title('3D Grid Visualization')

# plt.show()