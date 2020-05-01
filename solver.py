import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import pathlib
import random
from datetime import datetime
import pickle
import heapq

random.seed(datetime.now())

# Function to sort the list by second item of tuple
def Sort_Tuple(tup, pos):
    return (sorted(tup, key=lambda x: x[pos]))

def AverageEdgeCost(G, u):
    average = 0
    neighbors = list(nx.neighbors(G, u))
    for neighbor in neighbors:
        average += G.get_edge_data(u, neighbor)['weight']
    return average / len(neighbors)

def findSpanningTreeDFS(G):
    T = nx.Graph()
    n = len(list(G.nodes()))
    visited = [False] * n
    start = random.randrange(n)
    fringe = [(-1, start)]
    while len(fringe) > 0:
        edge = fringe.pop()
        if not visited[edge[1]]:
            visited[edge[1]] = True
            T.add_node(edge[1])
            if edge[0] > -1:
                weight = G.get_edge_data(edge[0], edge[1])['weight']
                T.add_edge(edge[0], edge[1], weight=weight)
            neighbors = list(nx.neighbors(G, edge[1]))
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if not visited[neighbor]:
                    fringe.append((edge[1], neighbor))
    return T


def findSpanningTreeDFS(G):
    T = nx.Graph()
    n = len(list(G.nodes()))
    visited = [False] * n
    start = random.randrange(n)
    fringe = [(-1, start)]
    while len(fringe) > 0:
        edge = fringe.pop()
        if not visited[edge[1]]:
            visited[edge[1]] = True
            T.add_node(edge[1])
            if edge[0] > -1:
                weight = G.get_edge_data(edge[0], edge[1])['weight']
                T.add_edge(edge[0], edge[1], weight=weight)
            neighbors = list(nx.neighbors(G, edge[1]))
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if not visited[neighbor]:
                    fringe.append((edge[1], neighbor))
    return T


def findSpanningTreeBFS(G):
    T = nx.Graph()
    n = len(list(G.nodes()))
    visited = [False] * n
    start = random.randrange(n)

    # node_degree = Sort_Tuple(G.degree(list(G.nodes())), 1)
    # max_degree_nodes = []
    # max_deg = 0
    # for node in node_degree:
    #     max_deg = max(max_deg, node[1])
    # for node in node_degree:
    #     if node[1] == max_deg:
    #         max_degree_nodes.append(node)
    # max_deg_avg = []
    # if len(max_degree_nodes) > 1:
    #     for node in max_degree_nodes:
    #         max_deg_avg.append((node[0], AverageEdgeCost(G, node[0])))
    #     max_deg_avg = Sort_Tuple(max_deg_avg, 1)
    #     start = max_deg_avg.pop(0)[0]
    # else:
    #     start = max_degree_nodes.pop()[0]

    fringe = [(-1, start)]

    while len(fringe) > 0:
        edge = fringe.pop(0)

        if not visited[edge[1]]:
            visited[edge[1]] = True
            T.add_node(edge[1])
            if edge[0] > -1:
                weight = G.get_edge_data(edge[0], edge[1])['weight']
                T.add_edge(edge[0], edge[1], weight=weight)

            neighbors = list(nx.neighbors(G, edge[1]))
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if not visited[neighbor]:
                    fringe.append((edge[1], neighbor))
    return T

def findSpanningTreeHeuristicDFS(G):
    T = nx.Graph()
    n = len(list(G.nodes()))
    visited = [False] * n
    start = random.randrange(n)
    fringe = []

    fringe.append((-1, start))
    while len(fringe) > 0:
        # edge = fringe.pop(0)
        edge = heapq.heappop(fringe)
        if not visited[edge[1]]:
            visited[edge[1]] = True
            T.add_node(edge[1])
            if edge[0] > -1:
                weight = G.get_edge_data(edge[0], edge[1])['weight']
                T.add_edge(edge[0], edge[1], weight=weight)

            neighbors = list(nx.neighbors(G, edge[1]))

            # neighbors_inv_weights = []
            # total = 0
            # for neighbor in neighbors:
            #     inv_weight = 1/G.get_edge_data(edge[1], edge[neighbor])['weight']
            #     neighbors_inv_weights.append((neighbor, inv_weight))
            #     total += inv_weight
            # normalized_neighbor_inv_weights = []
            # for neighbor in neighbors_inv_weights:
            #     normalized_neighbor_inv_weights.append((neighbor[0], neighbor[1]/total))
            # normalized_neighbor_inv_weights = sorted(normalized_neighbor_inv_weights, key=lambda x: x[1])

            random.shuffle(neighbors)
            for neighbor in neighbors:
                if not visited[neighbor]:
                    fringe.append((edge[1], neighbor))
    return T

def findSpanningTreeUCS(G):
    T = nx.Graph()
    n = len(list(G.nodes()))
    visited = [False] * n
    start = random.randrange(n)
    fringe = []

    heapq.heappush(fringe, (-1, (-1, start)))
    while len(fringe) > 0:
        edge = heapq.heappop(fringe)[1]
        if not visited[edge[1]]:
            visited[edge[1]] = True
            T.add_node(edge[1])
            if edge[0] > -1:
                weight = G.get_edge_data(edge[0], edge[1])['weight']
                T.add_edge(edge[0], edge[1], weight=weight)

            neighbors = list(nx.neighbors(G, edge[1]))

            neighbors_weights = []
            for neighbor in neighbors:
                weight = G.get_edge_data(edge[1], neighbor)['weight']
                neighbors_weights.append((neighbor, weight))
            for neighbor in neighbors_weights:
                if not visited[neighbor[0]]:
                    heapq.heappush(fringe, (neighbor[1], (edge[1], neighbor[0])))

    return T

def minDominatingSet(G):
    S = nx.dominating_set(G)
    T = nx.minimum_spanning_tree(G)
    for node in list(T.nodes()):
        if node not in S:
            H = T.copy()
            if nx.is_connected(H.remove_node(node)):
                T.remove_node(node)
    return T

# Returns: T: networkx.Graph
def solve(G):
    T = findSpanningTreeBFS(G)
    node_degree = T.degree(list(T.nodes()))
    leaves = []
    for node in node_degree:
        if node[1] == 1:
            edge = list(G.edges(node[0]))[0]
            leaves.append((node[0], G.get_edge_data(edge[0], edge[1])['weight']))

    leaves = Sort_Tuple(leaves, 1)
    random.shuffle(leaves)
    score = average_pairwise_distance(T)
    while len(leaves) > 0:
        leaf = leaves.pop()[0]
        if T.degree(leaf) == 1:
            newT = T.copy()
            newT.remove_node(leaf)
            newScore = average_pairwise_distance(newT)
            if newScore < score:
                score = newScore
                T = newT
    return T

# Usage: python3 solver.py test.in

def main(filename):
    # print(filename, end=": ")
    input_name = filename[0:-3]
    path = str(pathlib.Path().absolute()) + "/inputs/" +  input_name + '.in'
    G = read_input_file(path)
    found = False
    degrees = G.degree(list(G.nodes()))
    for deg in degrees:
        if deg[1] == len(degrees) - 1:
            edges = list(G.edges(deg[0]))
            if len(edges) != len(degrees) - 1:
                continue
            found = True
            T = nx.Graph()
            T.add_node(deg[0])
            break

    # print("Density: " + str(nx.density(G)))
    if not found:
        T = solve(G)
    # if not is_valid_network(G, T):
    #     print(filename)
    assert is_valid_network(G, T)
    score = average_pairwise_distance(T)

    scores = {}
    try:
        scoresFile = open('scores.obj', 'rb')
    except:
        pickle.dump(scores, open('scores.obj', 'wb'))
    scores = pickle.load(open('scores.obj', 'rb'))

    better = False

    if input_name not in scores or score < scores[input_name]:
        # print("Found better solution!")
        scores[input_name] = score
        better = True
        output_path = str(pathlib.Path().absolute()) + "/outputs/" + input_name + '.out'
        write_output_file(T, output_path)
        pickle.dump(scores, open('scores.obj', 'wb'))
    return (input_name, better, scores[input_name])

if __name__ == '__main__':
    assert len(sys.argv) == 2
    sys.exit(main(sys.argv[1]))