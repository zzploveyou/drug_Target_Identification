# coding:utf-8
import networkx as nx
import numpy as np
from munkres import Munkres


def cal_A(G):
    """calculate weight matrix A"""
    return nx.adjacency_matrix(G).toarray().T


def test():
    # input
    filename = "./example/edges.txt"
    outfile = "./example/out.txt"
    ccfile = "./data/edges.txt.ControlCentrality"
    epsilon = 0.001

    # read graph and calculate matrix A
    G = nx.digraph.DiGraph()
    for line in open(filename):
        tmp = line.strip().split()
        G.add_edge(tmp[0], tmp[1], weight=1)
    N = len(G.nodes())
    Nodes = G.nodes() + ["u_"+i for i in G.nodes()]
    A = cal_A(G)

    # read C matrix(important nodes)
    V0 = set([i.strip() for i in open(outfile).readlines()])

    # read ControlCentrality data
    rcc = {}
    rank = N
    for line in open(ccfile):
        rcc[line.split()[0]] = rank
        rank -= 1

    # construct the weighted bipartite graph
    R = np.zeros((N, 2*N))
    R[:][:] = -np.Inf
    for (i, j), a in np.ndenumerate(A):
        if G.nodes()[i] in V0:
            if a != 0:
                R[i][j] = 1
        else:
            if a != 0:
                R[i][j] = 0
            else:
                if i == j:
                    R[i][j] = 0
    for i, node in enumerate(G.nodes()):
        if node in V0:
            R[i][i+N] = epsilon*rcc[node]
        else:
            R[i][i+N] = epsilon*rcc[node] - 1

    # KM allocate algorithm
    cost_matrix = -R
    m = Munkres()
    indexes = m.compute(cost_matrix)

    for row, col in indexes:
        print "{}, {}".format(Nodes[row], Nodes[col])


if __name__ == '__main__':
    test()
