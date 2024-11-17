import random
import math

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
size = 2 # lattice size
n = size ** 2 # number of spin points
temp = 5.0 # starting point for temp
min_temp = 0.5 # min temp
step = 0.1 # size of steps for temp loop
mcs = 10000 # number of Monte Carlo steps
transient = 1000 # number of transient steps
norm = 1.0/(mcs*n) # normalization for averaging

array = [[0] * size for _ in range(size)]
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def generatearray(size):
    global array
    for x in range(size):
        for y in range(size):
            array[x][y] = random.choice([-1, 1])

def showarray():
    for row in array:
        print(row)

def get_random_point():
    x, y = random.randint(0, size-1), random.randint(0, size-1)
    return (x, y)

def get_energy(point):
    x, y = point
    neighbours = 0
    for dx, dy in directions:
        nx, ny = (x + dx) % size, (y + dy) % size
        neighbours += array[nx][ny]
    energy = -array[x][y] * neighbours
    return energy

def flip(point):
    x, y = point
    de = -2 * get_energy((x, y))
    if de < 0 or random.random() < math.exp(-de/temp):
        array[x][y] *= -1
        return de, True
    return de, False

def transient_results():
    for _ in range(n * transient):
        flip(get_random_point())

def total_magnetization():
    magnetization = 0
    for x in range(size):
        for y in range(size):
            magnetization += array[x][y]
    return magnetization

def total_energy():
    energy = 0
    for x in range(size):
        for y in range(size):
            energy += get_energy((x, y))
    return energy

def main():
    global temp
    generatearray(size)

    while temp >= min_temp:

        transient_results()

        m = total_magnetization()
        mabs = abs(m)
        e = total_energy()

        etot = etotsq = mtot = mtotsq = mabstot = mqtot = 0

        for _ in range(mcs):
            for _ in range(n):
                x, y = get_random_point()
                de, flipped = flip((x, y))
                if flipped:
                    e += 2 * de
                    m += 2 * array[x][y]
                    mabs += abs(array[x][y])

            etot += e / 2.0
            etotsq += (e / 2.0) ** 2
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
        U_L = 1-((mq_avg)/(3 * (msq_avg**2)))

        print(f"Temperature: {temp}")
        print(f"<M>: {m_avg}\n<|M|>: {mabs_avg}\n<M^2>: {msq_avg}")
        print(f"Susceptibility per spin (X): {X}")
        print(f"Susceptibility per spin (X’): {X_prime}")
        print(f"<E>: {e_avg}\n<E^2>: {esq_avg}")
        print(f"Heat capacity per spin (C): {C}")
        print(f"Cumulant (U_L): {U_L}")
        showarray()
        print()
        temp -= step

main()