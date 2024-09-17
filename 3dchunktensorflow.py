import tensorflow as tf
import numpy as np
from collections import deque
import random
import time

# Define parameters
max_temp = 15  # max temperature
min_temp = 1   # min temperature
step = 0.1     # temperature step size
mcs = 100000   # number of Monte Carlo steps
transient = 10000  # number of transient steps
norm = 1 / mcs  # normalization for averaging

# Define directions in 3D space
directions = tf.constant([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], dtype=tf.int32)
diagonal_directions = tf.constant([
    (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
    (-1, 1, 0), (-1, -1, 0), (-1, 0, 1), (-1, 0, -1)
], dtype=tf.int32)

# Generate 3D array representation of cube
def generatearray(size, p):
    array = tf.random.uniform((size, size, size), minval=-1, maxval=2, dtype=tf.int32)
    x, y, z = tf.meshgrid(tf.range(size), tf.range(size), tf.range(size), indexing='ij')
    mask = (x + y + z) % 2 == 0
    array = tf.where(mask, array, 0)
    removal_mask = tf.random.uniform((size, size, size)) < p
    removal_mask = tf.logical_and(removal_mask, mask)
    for dx, dy, dz in directions.numpy():
        rolled_mask = tf.roll(removal_mask, shift=[dx, dy, dz], axis=[0, 1, 2])
        array = tf.where(rolled_mask, 0, array)
    return array

# Get energy tensor
def get_energy_tensor(array, directions, diagonal_directions):
    size = array.shape[0]
    energies = tf.zeros_like(tf.cast(array, tf.float32))
    for d in diagonal_directions.numpy():
        dx, dy, dz = d
        shifted_array = tf.roll(tf.cast(array, tf.float32), shift=[dx, dy, dz], axis=[0, 1, 2])
        energies += shifted_array
    return -tf.cast(array, tf.float32) * energies

# Flip spins
def flip_spins(array, temp, directions, diagonal_directions):
    energies = get_energy_tensor(array, directions, diagonal_directions)
    de = -2 * energies
    flip_mask = tf.logical_or(de < 0, tf.random.uniform(tf.shape(de)) < tf.exp(-de / temp))
    array = tf.where(flip_mask, -array, array)
    return array

# Monte Carlo step
def monte_carlo_step(array, temp, directions, diagonal_directions):
    array = flip_spins(array, temp, directions, diagonal_directions)
    return array

# Transient results
def transient_results(array, temp, directions, diagonal_directions, n, transient_steps):
    for _ in range(n * transient_steps):
        array = monte_carlo_step(array, temp, directions, diagonal_directions)
    return array

# Total magnetization of chunk
def total_magnetization(array, chunk):
    magnetization = tf.reduce_sum(tf.gather_nd(array, chunk))
    return magnetization.numpy()

# Total energy of chunk
def total_energy(array, chunk, directions, diagonal_directions):
    energies = get_energy_tensor(array, directions, diagonal_directions)
    total_energy = tf.reduce_sum(tf.gather_nd(energies, chunk))
    return (total_energy / 2).numpy()  # Bonds are double-counted

# BFS to find the largest chunk
def bfs(array, start, visited, size):
    path = []
    queue = deque([start])
    while queue:
        x, y, z = queue.popleft()
        path.append((x, y, z))
        for d in diagonal_directions.numpy():
            dx, dy, dz = d
            nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
            if abs(array[nx, ny, nz]) == 1 and not visited[nx, ny, nz]:
                visited[nx, ny, nz] = True
                queue.append((nx, ny, nz))
    return path

# Find largest chunk in array
def find_largest_chunk(array, size):
    visited = tf.zeros((size, size, size), dtype=tf.bool)
    max_path = []
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if not visited[x, y, z] and abs(array[x, y, z]) == 1:
                    visited[x, y, z] = True
                    path = bfs(array, (x, y, z), visited, size)
                    if len(path) > len(max_path):
                        max_path = path
    return max_path

# Main function
def main(size, p):
    temp = max_temp
    array = generatearray(size, p)
    directions = directions.numpy()
    diagonal_directions = diagonal_directions.numpy()
    
    chunk = find_largest_chunk(array.numpy(), size)
    n = len(chunk)
    if n < 1:
        return

    while temp >= min_temp:
        array = transient_results(array, temp, directions, diagonal_directions, n, transient)
        
        m = total_magnetization(array, chunk)
        e = total_energy(array, chunk, directions, diagonal_directions)
        
        etot = etot2 = mtot = mtot2 = mabstot = mtot4 = 0
        for _ in range(mcs):
            for _ in range(n):
                array = monte_carlo_step(array, temp, directions, diagonal_directions)
                
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

        X = (m2_avg - (mabs_avg ** 2)) / (temp * n)
        C = (e2_avg - (e_avg ** 2)) / ((temp ** 2) * n)
        try:
            U_L = 1 - ((m4_avg) / (3 * (m2_avg ** 2)))
        except ZeroDivisionError:
            return
        
        with open('mcdata.txt', 'a') as file:
            file.write(f"{size}, {len(chunk)}, {p}, {temp}, {X}, {C}, {U_L}\n")
        
        temp -= step

if __name__ == "__main__":
    size = 8
    p = 3
    for _ in range(4):
        main(size, p / 100)
    for p in range(4, 31):
        for _ in range(5):
            main(size, p / 100)