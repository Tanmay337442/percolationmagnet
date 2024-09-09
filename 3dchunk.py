import random
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import time

# TODO
# count N as number of points in cluster
# fix generate_array
# set constants, directions
# pass temp as arg
# remove value argument
# replace chunk with cluster

# useful directions in 3D space
directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
diagonal_directions = [(1, 1, 0),
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
            (-1, 0, -1)]

# size = 4 # lattice size
# p = 0.05
max_temp = 15
min_temp = 1 # min temp - 0.1
temp = max_temp # starting point for temp - 20.0
step = 0.1 # size of steps for temp loop - 0.2
mcs = 100000 # number of Monte Carlo steps
transient = 10000 # number of transient steps
norm = 1/mcs # normalization for averaging

# array of largest chunks
largestchunks = []

# generate 3D array representation of cube with side length and probability of square being removed
def generatearray(size, p):
    array = [[[1] * size for _ in range(size)] for _ in range(size)] # 3D array of 1's
    # set spins
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if (x+y+z) % 2 != 0:
                    array[x][y][z] *= random.choice([-1, 1]) # multiplying with 0 does nothing
                elif random.random() < p: # randomly remove square with probability
                    array[x][y][z] = 0
                    # check adjacent circles with wrapping
                    for dx, dy, dz in directions:
                        nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
                        array[nx][ny][nz] = 0
                else:
                    array[x][y][z] = 0
    return array

# choose random point within the given chunk
def get_random_point(chunk):
    return random.choice(chunk)

# get energy of point in chunk
def get_energy(point, array):
    x, y, z = point # get coordinates of point
    neighbours = 0 # total spin value of neighbouring points
    for dx, dy, dz in diagonal_directions:
        nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
        neighbours += array[nx][ny][nz]
    energy = -array[x][y][z] * neighbours # calculate energy
    return energy

# flip spin at a point if valid
def flip(point, array):
    x, y, z = point # get coordinates of point
    # calculate change in energy for spin - in get_energy -1 multiplied by spin is done, therefore
    # when flipped, must multiply by -1 and multiply by 2 since it is the difference from the other value
    de = -2 * get_energy(point, array)
    if de < 0 or random.random() < (math.e ** (-de/temp)): # flip due to lower energy or heat bath
        array[x][y][z] *= -1
        return de, True
    return de, False # do not flip

# ignore transient results
def transient_results(array, chunk, n):
    for _ in range(n * transient):
        flip(get_random_point(chunk), array)

# calculate total magnetization of chunk
def total_magnetization(array, chunk):
    magnetization = 0
    for point in chunk:
        x, y, z = point
        magnetization += array[x][y][z] # sum all spin values
    return magnetization

# calculate total energy of chunk
def total_energy(array, chunk):
    energy = 0.0
    for point in chunk:
        energy += get_energy(point, array) # sum energy of each point in chunk
    return energy/2 # bonds double counted

def bfs(array, start, visited, size):
    path = [] # list of coordinates that makes up a chunk
    queue = deque([start]) # queue of remaining points in chunk
    # while points in the chunk remain
    while queue:
        x, y, z = queue.popleft() # get coordinates of point
        path.append((x, y, z)) # add point to path
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
        for dx, dy, dz in diagonal_directions: # check diagonally adjacent points with wrapping
            nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
            # check if point matches value being searched for (circle/square) and is not yet visited
            if abs(array[nx][ny][nz]) == 1 and not visited[nx][ny][nz]:
                visited[nx][ny][nz] = True # set point to visited
                queue.append((nx, ny, nz)) # add point to queue
    return path

# find largest chunk in array
def find_largest_chunk(array, size):
    visited = [[[False] * size for _ in range(size)] for _ in range(size)] # array of visited points
    max_path = [] # coordinates of all points in largest chunk
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # if point unvisited and matches value being searched for (circle/square)
                if not visited[x][y][z] and abs(array[x][y][z]) == 1:
                    visited[x][y][z] = True # set to visited
                    path = bfs(array, (x, y, z), visited, size) # get all points in chunk
                    # set chunk to new max if chunk is larger than the current max
                    if len(path) > len(max_path):
                        max_path = path
    print(f"Largest chunk size: {len(max_path)}")
    return max_path

def main(size, p):
    global temp
    temp = max_temp
    # generate 3D array
    array = generatearray(size, p)
    # find largest chunk in array
    print(f"Size: {size}, p: {p}")
    chunk = find_largest_chunk(array, size)
    n = len(chunk)
    if n < 1:
        return
    # temperature loop
    temp_arr = []
    x_arr = []
    c_arr = []
    u_l_arr = []
    while temp >= min_temp:
        # ignore transient results
        transient_results(array, chunk, n)
        # calculate total magnetization of chunk
        m = total_magnetization(array, chunk)
        # calculate total energy of chunk
        e = total_energy(array, chunk)
        # set variables to 0
        etot = etot2 = mtot = mtot2 = mabstot = mtot4 = 0
        # Monte Carlo loop
        for _ in range(mcs):
            # Metropolis loop
            for _ in range(n):
                x, y, z = get_random_point(chunk) # pick random point in chunk
                de, flipped = flip((x, y, z), array) # flip spin if valid
                if flipped: # if spin was flipped
                    e += de
                    m += 2 * array[x][y][z] # add change in magnetization

            etot2 += e ** 2
            mtot2 += m ** 2
            mtot4 += m ** 4
            mabstot += abs(m)
            etot += e
            mtot += m 
        
        e_avg = etot * norm
        e2_avg = etot2 * norm
        m_avg = mtot * norm
        m2_avg = mtot2 * norm
        mabs_avg = mabstot * norm
        m4_avg = mtot4 * norm

        # X = (m2_avg-(m_avg ** 2))/(temp * n)
        X = (m2_avg-(mabs_avg ** 2))/(temp * n)
        C = (e2_avg - (e_avg ** 2))/((temp ** 2) * n)
        try:
            U_L = 1-((m4_avg)/(3 * (m2_avg ** 2)))
        except ZeroDivisionError:
            return
        
        print(f"Temperature: {temp}")
        print(f"<M>: {m_avg}\n<|M|>: {mabs_avg}\n<M^2>: {m2_avg}")
        print(f"Susceptibility per spin (X): {X}")
        # print(f"Susceptibility per spin (X’): {X_PRIME}")
        print(f"<E>: {e_avg}\n<E^2>: {e2_avg}")
        print(f"Heat capacity per spin (C): {C}")
        print(f"Cumulant (U_L): {U_L}")
        print()
        temp_arr.append(temp)
        x_arr.append(X)
        # xprime_arr.append(X_PRIME)
        c_arr.append(C)
        u_l_arr.append(U_L)
        file.write(f"{size}, {len(chunk)}, {p}, {temp}, {X}, {C}, {U_L}\n")

        # with open('data.txt') as data:
        #     data.write(temp)
        #     data.write(X)
        #     data.write(X_PRIME)
        #     data.write(C)
        #     data.write(U_L)
        temp -= step

    # plt.plot(temp_arr, x_arr)
    # plt.show()
    # # plt.plot(temp_arr, xprime_arr)
    # # plt.show()
    # plt.plot(temp_arr, c_arr)
    # plt.show()
    # plt.plot(temp_arr, u_l_arr)
    # plt.show()

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # for x in range(size):
    #     for y in range(size):
    #         for z in range(size):
    #             if array[x][y][z] == 1:
    #                 ax.scatter(x, y, z, c='b', marker='^')
    #             elif array[x][y][z] == -1:
    #                 ax.scatter(x, y, z, c='b', marker='v')
    #             elif array[x][y][z] == 2:
    #                 ax.scatter(x, y, z, c='g', marker=',')

    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # ax.axes.set_xlim3d(left=0, right=size-1) 
    # ax.axes.set_ylim3d(bottom=0, top=size-1) 
    # ax.axes.set_zlim3d(bottom=0, top=size-1) 
    # ax.set_title('3D Grid Visualization')

    # plt.show()

file = open('mcdata.txt', 'a')

size, p = 6, 2

for _ in range(15):
    main(size, p/100)

for p in range(3, 31):
    for _ in range(20):
        main(size, p/100)

for size in [8, 12]:
    for p in range(31):
        for _ in range(20):
            main(size, p)