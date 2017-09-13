from random import randint

def ConstructGraph(path):
    file = open(path, "r")
    n, m = file.readline().split()
    vertices = [Vertex(i) for i in range(int(n))]

    for line in file:
        edge = list(map(int, line.split()))     #[v, v_o, w]
        vertices[edge[0]-1].add_edge(vertices[edge[1]-1], edge[2])
        vertices[edge[1]-1].add_edge(vertices[edge[0]-1], edge[2])

    return vertices

class Vertex():
    def __init__(self, i):
        self.i = i
        self.edges = []

    def add_edge(self, other, weight):
        self.edges.append((other, weight))

    def __repr__(self):
        return "{}:\n{}".format(self.i, self.edges)

def R(n):
    return [randint(0,1) == 1 for i in range(n)]

def S(vertices, in_A=None):
    if in_A is None:
        in_A = [False for i in range(len(vertices))]
    assert len(vertices) == len(in_A)

    changed = True
    while changed:
        changed = False
        for v in vertices:
            W = sum((e[1] for e in v.edges if in_A[v.i] != in_A[e[0].i]))
            W_flipped = sum((e[1] for e in v.edges if in_A[v.i] == in_A[e[0].i]))
            if W_flipped > W:
                in_A[v.i] = not in_A[v.i]
                changed = True

    return in_A

def RS(vertices):
    permutation = R(len(vertices))
    return S(vertices, permutation)

def cut_size(vertices, in_A):
    C = 0
    for v in vertices:
        C += sum((e[1] for e in v.edges if in_A[v.i] != in_A[e[0].i]))
    return C/2

import matplotlib.pyplot as plt
import numpy as np

reps = 100
vertices = ConstructGraph("assign2_ex_100.txt")
r_100 = [cut_size(vertices, R(len(vertices))) for i in range(reps)]
s_100 = [cut_size(vertices, S(vertices)) for i in range(reps)]
rs_100 = [cut_size(vertices, RS(vertices)) for i in range(reps)]

print("R_100:  avg={}, max={}".format(np.average(r_100), np.max(r_100)))
print("S_100:  avg={}, max={}".format(np.average(s_100), np.max(s_100)))
print("RS_100: avg={}, max={}".format(np.average(rs_100), np.max(rs_100)))

vertices = ConstructGraph("assign2_ex_1000.txt")
r_1000 = [cut_size(vertices, R(len(vertices))) for i in range(reps)]
s_1000 = [cut_size(vertices, S(vertices)) for i in range(reps)]
rs_1000 = [cut_size(vertices, RS(vertices)) for i in range(reps)]
print("R_1000:  avg={}, max={}".format(np.average(r_1000), np.max(r_1000)))
print("S_1000:  avg={}, max={}".format(np.average(s_1000), np.max(s_1000)))
print("RS_1000: avg={}, max={}".format(np.average(rs_1000), np.max(rs_1000)))

plt.hist(r_100, alpha = 0.5)
plt.hist(s_100, bins=2, alpha=0.5)
plt.hist(rs_100, alpha=0.5)
plt.axis([10000, 13658, 0, 30])
plt.show()

# 3 =>  O(N)
# 4 =>  32*n random bits
#       C~12354, 90%
# 7 =>  ????? 0?
#       Pr(X_uv = 1) = 0.5
#       ?? E[C] = 0.5 * W
#       ????? E[C] >= 0*OPT
#       the probabilities are independent, and the algorithm may
#           place all edges in the same Set, giving a cut of 0.