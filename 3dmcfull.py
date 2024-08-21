import random
from collections import deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

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
size = 8 # lattice size
n = int(size ** 3 / 2) # number of spin points
temp = 5.0 # starting point for temp - 5.0
min_temp = 0.5 # min temp - 0.5
step = 0.1 # size of steps for temp loop
mcs = 10000 # number of Monte Carlo steps
transient = 1000 # number of transient steps
norm = (1.0/float(mcs*n)) # normalization for averaging

def generatearray(size, p):
    global n
    array = [[[0] * size for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if (x+y+z) % 2 != 0:
                    array[x][y][z] = random.choice([-1, 1])
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if (x+y+z) % 2 == 0:
                    if random.random() < p:
                        for dx, dy, dz in directions:
                            nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
                            if array[nx][ny][nz] != 0:
                                n -= 1
                            array[nx][ny][nz] = 0
                    else:
                        array[x][y][z] = 2
    return array

def get_random_point():
    while True:
        x, y, z = random.randint(0, size-1), random.randint(0, size-1), random.randint(0, size-1)
        if (x+y+z) % 2 != 0:
            break
    return (x, y, z)

def get_energy(point, array):
    x, y, z = point
    neighbours = 0
    for dx, dy, dz in diagonal_directions:
        nx, ny, nz = (x + dx) % size, (y + dy) % size, (z + dz) % size
        neighbours += array[nx][ny][nz]
    energy = -array[x][y][z] * neighbours
    return energy

def flip(point, array):
    x, y, z = point
    de = -2 * get_energy(point, array)
    if de < 0 or random.random() < (math.e ** (-de/temp)):
        array[x][y][z] *= -1
        return de, True
    return de, False

def transient_results(array):
    for _ in range(n * transient):
        flip(get_random_point(), array)

def total_magnetization(array):
    magnetization = 0
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if (x+y+z) % 2 != 0:
                    magnetization += array[x][y][z]
    return magnetization

def total_energy(array):
    energy = 0
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if (x+y+z) % 2 != 0:
                    energy += get_energy((x, y, z), array)
    return energy

def main():
    global temp
    array = generatearray(size, 0)

    while temp >= min_temp:

        transient_results(array)

        m = total_magnetization(array)
        mabs = abs(m)
        e = total_energy(array)

        etot = etotsq = mtot = mtotsq = mabstot = mqtot = 0

        for _ in range(mcs):
            for _ in range(n):
                x, y, z = get_random_point()
                de, flipped = flip((x, y, z), array)
                if flipped:
                    e += 2 * de
                    m += 2 * array[x][y][z]
                    mabs += abs(array[x][y][z])

            etot += e/2.0
            etotsq += (e/2.0) ** 2
            mtot += m
            mtotsq += m ** 2
            mqtot += m ** 4
            mabstot += abs(m)
        
        e_avg = etot * norm
        esq_avg = etotsq * norm
        m_avg = mtot * norm
        msq_avg = mtotsq * norm
        mabs_avg = mabstot * norm
        mq_avg = mqtot * norm

        X = (msq_avg-((m_avg ** 2) * n))/temp
        X_prime = (msq_avg-((mabs_avg ** 2) * n))/temp
        C = (esq_avg - ((e_avg ** 2) * n))/(temp ** 2)
        U_L = 1-((mq_avg)/(3 * (msq_avg ** 2)))

        print(f"Temperature: {temp}")
        print(f"<M>: {m_avg}\n<|M|>: {mabs_avg}\n<M^2>: {msq_avg}")
        print(f"Susceptibility per spin (X): {X}")
        print(f"Susceptibility per spin (X’): {X_prime}")
        print(f"<E>: {e_avg}\n<E^2>: {esq_avg}")
        print(f"Heat capacity per spin (C): {C}")
        print(f"Cumulant (U_L): {U_L}")
        print()
        temp -= step

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for x in range(size):
        for y in range(size):
            for z in range(size):
                if array[x][y][z] == 1:
                    ax.scatter(x, y, z, c='b', marker='^')
                elif array[x][y][z] == -1:
                    ax.scatter(x, y, z, c='b', marker='v')
                elif array[x][y][z] == 2:
                    ax.scatter(x, y, z, c='g', marker=',')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.axes.set_xlim3d(left=0, right=size-1) 
    ax.axes.set_ylim3d(bottom=0, top=size-1) 
    ax.axes.set_zlim3d(bottom=0, top=size-1) 
    ax.set_title('3D Grid Visualization')

    plt.show()

main()