import random
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import time
import numpy as np
from numba import njit

# TODO
# count N as number of points in cluster
# fix generate_array
# set constants, directions
# pass temp as arg
# remove value argument
# replace chunk with cluster

# useful directions in 3D space
directions = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
diagonal_directions = np.array([(1, 1, 0),
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
            (-1, 0, -1)])

# size = 4 # lattice size
# p = 0.05
max_temp = 15 # max temp
min_temp = 1 # min temp - 0.1
step = 0.1 # size of steps for temp loop - 0.2
mcs = 100000 # number of Monte Carlo steps
transient = 10000 # number of transient steps
norm = 1/mcs # normalization for averaging

# generate 3D array representation of cube with side length and probability of square being removed
def generatearray(size, p):
    array = np.random.choice(np.array([-1, 1]), (size, size, size)) # 3D array of 1's
    x, y, z = np.indices((size, size, size))
    mask = (x + y + z) % 2 == 0
    array[mask] = 0
    removal_mask = (np.random.rand(size, size, size) < p) & mask
    for dx, dy, dz in directions:
        rolled_mask = np.roll(removal_mask, (dx, dy, dz), (0, 1, 2))
        array[rolled_mask] = 0
    return array

# get energy of point in chunk
@njit
def get_energy(point, array):
    x, y, z = point
    neighbours = 0
    for d in diagonal_directions:
        dx, dy, dz = d
        nx = (x + dx) % size
        ny = (y + dy) % size
        nz = (z + dz) % size
        neighbours += array[nx, ny, nz]
    energy = -array[x, y, z] * neighbours
    return energy

# flip spin at a point if valid
@njit
def flip(point, array, temp):
    x, y, z = point # get coordinates of point
    # calculate change in energy for spin - in get_energy -1 multiplied by spin is done, therefore
    # when flipped, must multiply by -1 and multiply by 2 since it is the difference from the other value
    de = -2 * get_energy(point, array)
    if de < 0 or np.random.random() < np.exp(-de/temp): # flip due to lower energy or heat bath
        array[x, y, z] *= -1
        return de, True
    return de, False # do not flip

# ignore transient results
def transient_results(array, chunk, n, temp):
    for _ in range(n * transient):
        flip(random.choice(chunk), array, temp)

# calculate total magnetization of chunk
@njit
def total_magnetization(array, chunk):
    magnetization = 0
    # sum all spin values
    for point in chunk:
        x, y, z = point
        magnetization += array[x, y, z]
    return magnetization 

# calculate total energy of chunk
@njit
def total_energy(array, chunk):
    # sum energy of each point in chunk, bonds double counted
    return np.sum(np.array([get_energy(point, array) for point in chunk]))/2

def bfs(array, start, visited, size):
    path = [] # list of coordinates that makes up a chunk
    queue = deque([start]) # queue of remaining points in chunk
    # while points in the chunk remain
    while queue:
        x, y, z = queue.popleft() # get coordinates of point
        path.append((x, y, z)) # add point to path
        for dx, dy, dz in diagonal_directions: # check diagonally adjacent points with wrapping
            nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
            # check if point matches value being searched for (circle/square) and is not yet visited
            if abs(array[nx, ny, nz]) == 1 and not visited[nx, ny, nz]:
                visited[nx, ny, nz] = True # set point to visited
                queue.append((nx, ny, nz)) # add point to queue
    return path

# find largest chunk in array
def find_largest_chunk(array, size):
    visited = np.zeros((size, size, size), dtype=bool) # array of visited points
    max_path = [] # coordinates of all points in largest chunk
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # if point unvisited and matches value being searched for (circle/square)
                if not visited[x, y, z] and abs(array[x, y, z]) == 1:
                    visited[x, y, z] = True # set to visited
                    path = bfs(array, (x, y, z), visited, size) # get all points in chunk
                    # set chunk to new max if chunk is larger than the current max
                    if len(path) > len(max_path):
                        max_path = path
    return max_path

def main(size, p):
    temp = max_temp
    # generate 3D array
    array = generatearray(size, p)
    # find largest chunk in array
    chunk = find_largest_chunk(array, size)
    n = len(chunk)
    if n < 1:
        return
    while temp >= min_temp:
        # ignore transient results
        transient_results(array, chunk, n, temp)
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
                x, y, z = random.choice(chunk) # pick random point in chunk
                de, flipped = flip((x, y, z), array, temp) # flip spin if valid
                if flipped: # if spin was flipped
                    e += de
                    m += 2 * array[x, y, z] # add change in magnetization

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
        
        file.write(f"{size}, {len(chunk)}, {p}, {temp}, {X}, {C}, {U_L}\n")
        temp -= step

file = open('mcdata3.txt', 'a')

size = 8

######## 11.5hrs
for p in [11, 15, 19, 23, 27]:
    main(size, p/100)