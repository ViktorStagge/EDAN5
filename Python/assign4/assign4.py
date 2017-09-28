import numpy as np
import re
import sys
from numpy.linalg import solve
from numpy.linalg.linalg import LinAlgError
from random import random
from os import listdir




def build_process(path):
    file = open(path, "r")
    N, M, H, F, P = (int(v) for v in file.readline().split())

    A = np.zeros([N, N])
    times = np.zeros([N, N])

    for line in file:
        u, v, t, p_uv, p_vu = (float(v) for v in line.split())
        A[int(u), int(v)] = p_uv
        A[int(v), int(u)] = p_vu
        times[int(u), int(v)] = t
        times[int(v), int(u)] = t

    b = np.array([p @ t for p, t in zip(A, times)])
    return A, b, times, H, F, P

def markov_transient(A, b):
    return solve(A - np.eye(*A.shape), -b)



def montecarlo_time(P, T, start_node, home, iterations=100):
    all_times = []

    for i in range(iterations):
        u = start_node
        time = 0.

        while(u != home):
            v = random()
            index = -1
            while v > 0:
                index += 1
                v -= P[u, index]
            time += T[u, index]
            u = index
        all_times.append(time)
    return np.average(all_times)




def run(dir):
    input_RE = re.compile('.*\.in$')
    for file in listdir(dir):
        if input_RE.match(file):
            print('{}:'.format(file))
            A, b, T, H, FedUPS, PostNHL = build_process(dir + '/' + file)

            try:
                x = markov_transient(A, b)
                print("\tmarkov:\t\t FedUPS: {:8.2f}, PostNHL: {:8.2f}".format(x[FedUPS], x[PostNHL]))
            except LinAlgError:
                print("\tFailed to use Markov-chains.")
            print("\tmontecarlo:\t FedUPS: {:8.2f}, PostNHL: {:8.2f}".format(montecarlo_time(A, T, FedUPS, H)
                                                                             , montecarlo_time(A, T, PostNHL, H)))

if __name__ == '__main__':
    dir = 'data'
    if len(sys.argv) > 1:
        dir = sys.argv[2]
    run(dir)

