import json

with open("G.json", "r") as f:
    G = json.loads(f.read())

with open("Cost.json", "r") as f:
    cost = json.loads(f.read())

with open("Dist.json", "r") as f:
    dist = json.loads(f.read())

with open("Coord.json", "r") as f:
    coord = json.loads(f.read())


combine_graph = {}
for k, adj in G.items():
    # coord_value = coord[k]
    res_list = []
    for node in adj:
        tmp_dist = dist[f"{k},{node}"]
        tmp_cost = cost[f"{k},{node}"]
        tmp_list = [node, tmp_dist, tmp_cost]
        res_list.append(tmp_list)
    combine_graph[k] = res_list


import heapq
import sys
from collections import deque

def get_cost(path):
    ucs_total_cost = 0
    for i in range(len(path) -1):
        ucs_total_cost += cost[f"{path[i]},{path[i+1]}"]
    return ucs_total_cost

def dijkstras(start_node, end_node):
    unvisited_nodes = list(combine_graph.keys())
    distance_from_start = {
            node: (0 if node == start_node else float("inf")) for node in combine_graph.keys()

        }
    previous_node = {node: None for node in combine_graph.keys()}
    while unvisited_nodes:
        current_node = min(
            unvisited_nodes, key=lambda node: distance_from_start[node]
        )
        unvisited_nodes.remove(current_node)

        if distance_from_start[current_node] == float("inf"):
            break

        for neighbor in combine_graph[current_node]:
            new_path = distance_from_start[current_node] + neighbor[1]
            if new_path < distance_from_start[neighbor[0]]:
                distance_from_start[neighbor[0]] = new_path
                previous_node[neighbor[0]] = current_node

        if current_node == end_node:
            break
    path = deque()
    current_node = end_node
    while previous_node[current_node] is not None:
        path.appendleft(current_node)
        current_node = previous_node[current_node]
    path.appendleft(start_node)

    return path, distance_from_start[end_node]
dijkstras_path, dijkstras_shortest_dist = dijkstras('1', '50')

print("Shortest path: ", end="")
for i, p in enumerate(dijkstras_path):
    if i == len(dijkstras_path) - 1:
        print(p, end='')
    else:
        print(p, end='->')
print()
print(f"Shortest distance: {dijkstras_shortest_dist}")
print(f"Total energy cost: {get_cost(dijkstras_path)}")