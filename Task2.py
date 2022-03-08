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

from queue import PriorityQueue

def get_cost(path):
    ucs_total_cost = 0
    for i in range(len(path) -1):
        ucs_total_cost += cost[f"{path[i]},{path[i+1]}"]
    return ucs_total_cost

def ucs(start_node, end_node):
    # create a priority queue of paths
    queue = PriorityQueue()
    queue.put((0, [start_node]))
    visited = set()
    path = []
    # iterate over the items in the queue
    while not queue.empty():
        # get the highest priority item
        dist, path = queue.get()
        node = path[len(path)-1]
        # if it's the goal, return
        if node not in visited:
            visited.add(node)
            if node == end_node:
                return path, dist

            for n in combine_graph[node]:
                if get_cost(path) + n[2] > 287932:
                    continue
                if n[0] not in visited:
                    t_dist = dist + n[1]
                    temp = path[:]
                    temp.append(n[0])

                    queue.put((t_dist, temp))
    return [], -1
ucs_path, ucs_distance = ucs('1', '50')
ucs_total_cost = 0
for i in range(len(ucs_path) -1):
    ucs_total_cost += cost[f"{ucs_path[i]},{ucs_path[i+1]}"]
print("Shortest path: ", end="")
for i, p in enumerate(ucs_path):
    if i == len(ucs_path) - 1:
        print(p, end='')
    else:
        print(p, end='->')
print()
print(f"Shortest distance: {ucs_distance}")
print(f"Total energy cost: {ucs_total_cost}")