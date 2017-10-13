import numpy as np
from itertools import combinations as comb

class Bag:
    def __init__(self, *args):
        self.id = args[0]
        self.vertices = frozenset(args[1:])
        self.edges = []
        self.children = []
        self.w = {}

    def edge_to(self, b):
        self.edges.append(b)

    def make_root(self):
        self.children.extend(self.edges)
        for b in self.children:
            b._set_parent(self)

    def _set_parent(self, b):
        self.parent = b
        self.edges.remove(b)
        self.children.extend(self.edges)
        for c in self.children:
            c._set_parent(self)

    def is_leaf(self):
        return len(self.children) == 0

    def max(self, t, all):
        t &= self.vertices
        m = 0
        for t2 in combinations(self.vertices - all):
            if independentset[t2 | t]:
                m = max(m, self.w[t2 | t] - len(t))
        return m


def TD(filename):
    f = open('data/{}.td'.format(filename), 'r')
    bags = []
    m = w = n = 0
    for line in f:
        if line[0] == 's':
            m, w, n = map(int, line.split()[2:])
        elif line[0] == 'b':
            b = Bag(*map(lambda x: int(x)-1, line.split()[1:]))
            bags.append(b)
        elif line[0] != 'c':
            b1, b2 = map(lambda x: int(x)-1, line.split())
            bags[b1].edge_to(bags[b2])
            bags[b2].edge_to(bags[b1])

    bags[0].make_root()
    bags = [bags[0]]
    for i in range(m):
        if len(bags[i].children) > 0:
            bags.extend(bags[i].children)
    return bags, w, n

def Graph(filename):
    f = open('data/{}.gr'.format(filename), 'r')

    for line in f:
        if line[0] == 'p':
            n, m = map(int, line.split()[2:])
            G = np.zeros([n, n])
        elif line[0] != 'c':
            v1, v2 = map(lambda x: int(x) - 1, line.split())
            G[v1, v2] = 1
    return G


def is_independentset(v, G):
    for vi in v:
        for vj in v:
            if G[vi, vj] > 0:
                return False
    return True

def combinations(set, k=None):
    if k is None:
        k = len(set)
    for i in range(k+1):
        for t in comb(set, i):
            yield frozenset(t)


name = 'WellsGraph'
G = Graph(name)
bags, width, n = TD(name)

print('{}: n={}, w={}'.format(name, n, width))

independentset = {}

def get(independentset, t, G):
    if t not in independentset:
        independentset[t] = is_independentset(t, G)
    return independentset[t]


print('starting...')
for b in reversed(bags):
    if b.is_leaf():
        b.w = {t: len(t) for t in combinations(b.vertices) if get(independentset, t, G)}
        #print('leaf [{:3}]: {}'.format(b.id, b.w))
    else:
        for t in combinations(b.vertices):
            if get(independentset, t, G):
                inner = [c.max(t, b.vertices) for c in b.children]
                b.w[t] = len(t) + sum(inner)
        #print('node [{:3}]: {}'.format(b.id, b.w))

setsize = max(v for k, v in bags[0].w.items())
print('Found maximum size: {}'.format(setsize))

