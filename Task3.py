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
import math

def deg_to_rad(deg):
    return deg*(math.pi / 180)

def get_distance_from_lat_lon(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = deg_to_rad(lat2 - lat1)
    dLon = deg_to_rad(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg_to_rad(lat1)) * math.cos(deg_to_rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R*c*10000)

def get_cost(path):
    total_cost = 0
    for i in range(len(path) -1):
        total_cost += cost[f"{path[i]},{path[i+1]}"]
    return total_cost

def get_distance(path):
    a_star_total_distance = 0
    for i in range(len(path) -1):
        a_star_total_distance += dist[f"{path[i]},{path[i+1]}"]
    return a_star_total_distance

def heuristic(node_one, node_two):
    coord_one = coord[node_one]
    coord_two = coord[node_two]
    lon1 = coord_one[0] / 1000000
    lat1 = coord_one[1] / 1000000
    lon2 = coord_two[0] / 1000000
    lat2 = coord_two[1] / 1000000
    return get_distance_from_lat_lon(lat1, lon1, lat2, lon2)

def a_star_with_constrains(start_node, end_node):
    # create a priority queue of paths
    queue = PriorityQueue()
    queue.put((0, [start_node]))
    path = []
    cost_so_far = {}
    cost_so_far[start_node] = 0
    # iterate over the items in the queue
    while not queue.empty():
        # get the highest priority item
        dist, path = queue.get()
        node = path[len(path)-1]
        # if it's the goal, return
        if node == end_node:
            return path, dist

        for n in combine_graph[node]:
            if get_cost(path) + n[2] > 287932:
                continue
            new_dist = cost_so_far[node] + n[1]
            if n[0] not in cost_so_far or new_dist < cost_so_far[n[0]]:
                cost_so_far[n[0]] = new_dist
                t_dist = new_dist + heuristic(n[0],'50')
                temp = path[:]
                temp.append(n[0])
                queue.put((t_dist, temp))
    return [], -1

a_star_constrains_path, _ = a_star_with_constrains('1', '50')
a_star_constrains_cost = 0
for i in range(len(a_star_constrains_path) -1):
    a_star_constrains_cost += cost[f"{a_star_constrains_path[i]},{a_star_constrains_path[i+1]}"]
print("Shortest path: ", end="")
for i, p in enumerate(a_star_constrains_path):
    if i == len(a_star_constrains_path) - 1:
        print(p, end='')
    else:
        print(p, end='->')
print()
print(f"Shortest distance: {get_distance(a_star_constrains_path)}")
print(f"Total energy cost: {a_star_constrains_cost}")