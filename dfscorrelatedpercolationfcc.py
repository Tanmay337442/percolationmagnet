import random
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file = open('fccmetropolis.txt', 'a')
directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

x_diagonal_directions = [(1, 1, 0),
            (1, -1, 0),
            (1, 0, 1),
            (1, 0, -1),
            (0, 1, 1),
            (0, -1, 1),
            (0, 1, -1),
            (0, -1, -1),
            (-1, 1, 0),
            (-1, -1, 0),
            (-1, 0, 1),
            (-1, 0, -1)
            ]

y_diagonal_directions = [(1, 1, 0),
            (-1, 1, 0),
            (0, 1, 1),
            (0, 1, -1),
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, 1),
            (-1, 0, -1),
            (1, -1, 0),
            (-1, -1, 0),
            (0, -1, 1),
            (0, -1, -1)
            ]
z_diagonal_directions = [(0, 1, 1),
            (1, 0, 1),
            (-1, 0, 1),
            (0, -1, 1),
            (1, 1, 0),
            (-1, 1, 0),
            (1, -1, 0),
            (-1, -1, 0),
            (0, 1, -1),
            (0, -1, -1),
            (1, 0, -1),
            (-1, 0, -1)
            ]

arrays = []
percolated = []
largestchunks = []
chunksizes = {}

def generatearray(size, p):
    array = [[[0] * size for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if (x+y+z) % 2 == 0:
                    array[x][y][z] = 1
                    if random.random() < p:
                        array[x][y][z] = 2
                        for dx, dy, dz in directions:
                            nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
                            array[nx][ny][nz] = -1
    return array

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

# def xdfs(array, size, current, visited, value):
#     x, y, z = current
#     visited[x][y][z] = True
#     if x == size - 1:
#         return [current]
#     for dx, dy, dz in x_diagonal_directions:
#             nx, ny, nz = x + dx, (y + dy) % size, (z + dz) % size

#             if nx > 0 and array[nx][ny][nz] == value and not visited[nx][ny][nz]:
#                 prev = xdfs(array, size, (nx, ny, nz), visited, value)
#                 if prev:
#                     return [current] + prev

# def ydfs(array, size, current, visited, value):
#     x, y, z = current
#     visited[x][y][z] = True
#     if y == size - 1:
#         return [current]
#     for dx, dy, dz in y_diagonal_directions:
#             nx, ny, nz = (x + dx) % size, y + dy, (z + dz) % size

#             if ny > 0 and array[nx][ny][nz] == value and not visited[nx][ny][nz]:
#                 prev = ydfs(array, size, (nx, ny, nz), visited, value)
#                 if prev:
#                     return [current] + prev

# def zdfs(array, size, current, visited, value):
#     x, y, z = current
#     visited[x][y][z] = True
#     if z == size - 1:
#         return [current]
#     for dx, dy, dz in z_diagonal_directions:
#             nx, ny, nz = (x + dx) % size, (y + dy) % size, z + dz

#             if nz > 0 and array[nx][ny][nz] == value and not visited[nx][ny][nz]:
#                 prev = zdfs(array, size, (nx, ny, nz), visited, value)
#                 if prev:
#                     return [current] + prev

def percolates(array, size, value):
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    for y in range(size):
        for z in range(size):
            if array[0][y][z] == value and not visited[0][y][z]:
                path = xdfs(array, size, (0, y, z), visited, value)
                if path:
                    return path
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for z in range(size):
            if array[x][0][z] == value and not visited[x][0][z]:
                path = ydfs(array, size, (x, 0, z), visited, value)
                if path:
                    return path
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            if array[x][y][0] == value and not visited[x][y][0]:
                path = zdfs(array, size, (x, y, 0), visited, value)
                if path:
                    return path
    return False

def bfs(array, start, visited, size, value):
    path = []
    queue = deque([start])
    while queue:
        x, y, z = queue.popleft()
        path.append((x, y, z))
        diagonal_directions = [(1, 1, 0),
                (-1, 1, 0),
                (1, -1, 0),
                (-1, -1, 0),
                (1, 0, 1),
                (-1, 0, 1),
                (1, 0, -1),
                (-1, 0, -1),
                (0, 1, 1),
                (0, -1, 1),
                (0, 1, -1),
                (0, -1, -1)]
        for dx, dy, dz in diagonal_directions:
            nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size

            if array[nx][ny][nz] == value and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                queue.append((nx, ny, nz))
    try:
        chunksizes[len(path)] += 1
    except KeyError:
        chunksizes[len(path)] = 1
    return path

def path_percolates(path, size):
    if any(coord[0] == 0 for coord in path) and any(coord[0] == (size-1) for coord in path):
        return True
    if any(coord[1] == 0 for coord in path) and any(coord[1] == (size-1) for coord in path):
        return True
    if any(coord[2] == 0 for coord in path) and any(coord[2] == (size-1) for coord in path):
        return True
    return False

def find_largest_chunk(array, size, value):
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    max_path = []

    for x in range(size):
        for y in range(size):
            for z in range(size):
                if not visited[x][y][z] and array[x][y][z] == value:
                    visited[x][y][z] = True
                    path = bfs(array, (x, y, z), visited, size, value)
                    if len(path) > len(max_path):
                        max_path = path
    
    return max_path

def find_largest_percolated_chunk(array, size, value):
    visited = [[[False] * size for _ in range(size)] for _ in range(size)]
    max_path = []

    for x in range(size):
        for y in range(size):
            for z in range(size):
                if not visited[x][y][z] and array[x][y][z] == value:
                    visited[x][y][z] = True
                    path = bfs(array, (x, y, z), visited, size, value)
                    if path_percolates(path, size) and len(path) > len(max_path):
                        max_path = path
    
    return max_path

def xdfs(array, size, current, visited, value):
    stack = [(current,[])]
    x, y, z = current
    visited[x][y][z] = True
    while stack:
        (x, y, z), path = stack.pop()
        if x == size - 1:
            return [(x,y,z)] + path

        for dx, dy, dz in x_diagonal_directions:
            nx, ny, nz = x + dx, (y + dy) % size, (z + dz) % size

            if nx > 0 and array[nx][ny][nz] == value and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                stack.append(((nx, ny, nz), [(x, y, z)] + path))

def ydfs(array, size, current, visited, value):
    stack = [(current,[])]
    x, y, z = current
    visited[x][y][z] = True
    while stack:
        (x, y, z), path = stack.pop()
        if y == size - 1:
            return [(x,y,z)] + path

        for dx, dy, dz in y_diagonal_directions:
            nx, ny, nz = (x + dx) % size, y + dy, (z + dz) % size

            if ny > 0 and array[nx][ny][nz] == value and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                stack.append(((nx, ny, nz), [(x, y, z)] + path))

def zdfs(array, size, current, visited, value):
    stack = [(current,[])]
    x, y, z = current
    visited[x][y][z] = True
    while stack:
        (x, y, z), path = stack.pop()
        if z == size - 1:
            return [(x,y,z)] + path

        for dx, dy, dz in z_diagonal_directions:
            nx, ny, nz = (x + dx) % size, (y + dy) % size, z + dz

            if nz > 0 and array[nx][ny][nz] == value and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True
                stack.append(((nx, ny, nz), [(x, y, z)] + path))

def calculate(size, p, trials, value):
    numpercolated = 0
    for _ in range(trials):
        array = generatearray(size, p)
        arrays.append(array)
        path = percolates(array, size, value)
        if path:
            percolated.append(True)
            numpercolated += 1
        else:
            percolated.append(False)
        largestchunk = find_largest_chunk(array, size, value)
        largestchunks.append(len(largestchunk))
    avglargestchunk = sum(largestchunks)/len(largestchunks)
    # sorted_chunksizes = dict(sorted(chunksizes.items()))
    print(f"{size}, {p}, {numpercolated/trials}, {avglargestchunk/((size ** 3)/2)}\n")
    file.write(f"{size}, {p}, {numpercolated/trials}, {avglargestchunk/((size ** 3)/2)}\n")

    # plt.hist(largestchunks)
    # plt.xlabel('Chunk Size')
    # plt.ylabel('Number of Occurrences')
    # plt.title(f'Number of Occurrences of Chunk Sizes for p={p} and trials={trials}')
    # plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for x in range(size):
        for y in range(size):
            for z in range(size):
                if array[x][y][z] == 0:
                    ax.scatter(x, y, z, c='b', marker='o')
                elif array[x][y][z] == 1:
                    ax.scatter(x, y, z, c='g', marker=',')
    
    if path:
        # print(path)
        for point in path:
            ax.scatter(point[0], point[1], point[2], c='r', s=100, marker='o')

    # print(largestchunk)
    # for point in largestchunk:
    #     ax.scatter(point[0], point[1], point[2], c='y', s=100, alpha=0.3, marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.axes.set_xlim3d(left=0, right=size-1) 
    ax.axes.set_ylim3d(bottom=0, top=size-1) 
    ax.axes.set_zlim3d(bottom=0, top=size-1) 
    ax.set_title('3D Grid Visualization')
    plt.savefig("fccvisualization.png")
    plt.show()

    return [p, numpercolated, avglargestchunk]

data = []

# for i in range(12, 22, 2):
#     for j in range(260, 285, 5):
#         calculate(i, j*0.001, 20000, 0)
#         arrays = []
#         percolated = []
#         largestchunks = []
#         chunksizes = {}

calculate(6, 0.25, 1, 0)

# calculate(8, 0.3, 1, 0)

# 6,8,10,12