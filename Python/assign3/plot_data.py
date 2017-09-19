import matplotlib.pyplot as plt
from math import log

n_R0 = 5
n_R1 = n_R0 + 4
n_R2 = n_R1 + 2
path = "output.txt"

f = open(path, "r")
header = f.readline()
lines = f.readlines()

def get_data(start_line, n):
    R = [line.split() for line in lines[start_line:start_line+n]]
    files = [int(line[0]) for line in R]
    set_size = [int(line[1]) for line in R]
    iterations = [log(int(line[2])) for line in R]
    return files, set_size, iterations


R0_files, R0_is, R0_iter = get_data(0, n_R0)
R1_files, R1_is, R1_iter = get_data(n_R0, n_R1)
R2_files, R2_is, R2_iter = get_data(n_R0 + n_R1, n_R2)

line_r1, = plt.plot(R0_files, R0_iter, alpha=0.5, linewidth=2)
line_r2, = plt.plot(R1_files, R1_iter, alpha=0.5, linewidth=2)
line_r3, = plt.plot(R2_files, R2_iter, alpha=0.5, linewidth=2)
plt.axis([0, 130, 0, 20])
plt.xlabel("|V|")
plt.ylabel("iterations, log")
plt.legend([line_r1, line_r2, line_r3], ["R0", "R1", "R2"], loc=2)
plt.show()