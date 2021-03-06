from numpy import maximum

def remove_node(graph, i):
    gen = (k for k in graph[i] if k != i)
    for k in gen:
        graph[k].pop(i)
    node = graph.pop(i)
    return node

def add_node(graph, node, i):
    for k in node:
        graph[k][i] = 1
    graph[i] = node

def remove_neighbourhood(graph, I):
    neighbour = [(i, graph.pop(i)) for i in graph[I]]
    if I in graph:
        neighbour.append((I, graph.pop(I)))
    for t in neighbour:
        for i in t[1]:
            if i in graph:
                graph[i].pop(t[0])
    return neighbour

def add_neighbourhood(graph, neighbourhood):
    for t in neighbourhood:
        graph[t[0]] = t[1]
    for t in neighbourhood:
        for i in t[1]:
            graph[i][t[0]] = 1

def min_max_neighbours_for(graph):
    min_index = 0
    max_index = 0
    min_val = len(graph)
    max_val = 0
    for i, v in graph.items():
        neighbours = sum(v.values()) - v.get(i, 0)
        if neighbours < min_val:
            min_index = i
            min_val = neighbours
        elif neighbours > max_val:
            max_index = i
            max_val = neighbours
    return min_index, min_val, max_index, max_val

def score_not_using_node(graph, i, type):
    node = remove_node(graph, i)
    score = R(graph, type)
    add_node(graph, node, i)
    return score

def score_using_node(graph, i, type):
    neighbourhood = remove_neighbourhood(graph, i)
    score = 1 + R(graph, type)
    add_neighbourhood(graph, neighbourhood)
    return score

def R(graph, type="R2"):
    global iterations
    iterations += 1
    if len(graph) == 0:
        return 0

    min_index, min_val, max_index, max_val = min_max_neighbours_for(graph)

    if min_val == 0:
        val = score_using_node(graph, min_index, type)

    elif min_val == 1 and (type == "R1" or type == "R2"):
        val = score_using_node(graph, min_index, type)

    elif min_val == 2 and type == "R2":
        e = [k for k in graph[min_index]]
        if e[0] in graph[e[1]]:
            val = score_using_node(graph, min_index, type)

        else:
            z = graph[e[0]].copy()
            z.update(graph[e[1]])
            z.pop(min_index)
            z.pop(e[0],-1)
            z.pop(e[1],-1)
            z_index = -iterations
            add_node(graph, z, z_index)
            neighbourhood = remove_neighbourhood(graph, min_index)

            val = 1 + R(graph, type)

            add_neighbourhood(graph, neighbourhood)
            remove_node(graph, z_index)
    else:
        val = maximum(score_not_using_node(graph, max_index, type)
                    , score_using_node(graph, max_index, type))
    return val


def create_graph(path):
    file = open(path, "r")
    n = int(file.readline())
    graph = {}
    for i, line in enumerate(file):
        edges = {j: int(e) for j, e in enumerate(line.split()) if e != "0"}
        graph[i] = edges
    global iterations
    iterations = 0
    return graph


iterations = 0

R0_files = ["g4.in", "g30.in", "g40.in", "g50.in", "g60.in"]
R1_files = R0_files.copy()
R1_files.extend(["g70.in", "g80.in", "g90.in", "g100.in"])
R2_files = R1_files.copy()
R2_files.extend(["g110.in", "g120.in"])

R0 = [(R(create_graph(path), type="R0"), iterations) for path in R0_files]
R1 = [(R(create_graph(path), type="R1"), iterations) for path in R1_files]
R2 = [(R(create_graph(path), type="R2"), iterations) for path in R2_files]

file = open("output.txt", "w")
for p, res in zip(R0_files, R0):
    file.write("{} {} {}\n".format(p, res[0], res[1]))
for p, res in zip(R1_files, R1):
    file.write("{} {} {}\n".format(p, res[0], res[1]))
for p, res in zip(R2_files, R2):
    file.write("{} {} {}\n".format(p, res[0], res[1]))