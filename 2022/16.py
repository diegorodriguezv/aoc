import fileinput
from itertools import permutations
from queue import PriorityQueue
from pprint import pp
from collections import deque


def main():
    rates = {}
    tunnels = {}
    for line in fileinput.input():
        _, _, rest = line.strip().partition("Valve ")
        name, _, rest = rest.partition(" has flow rate=")
        sep = "; tunnel leads to valve "
        rate, found, children = rest.partition(sep)
        if found != sep:
            sep = "; tunnels lead to valves "
            rate, found, children = rest.partition(sep)
        rate = int(rate)
        children = children.split(", ")
        rates[name] = rate
        tunnels[name] = children
    #     pp(tunnels)
    tree = valve_tree(tunnels, rates)
    #     pp(tree)
    #     pp(rates)
    bo = best_order_dfs(tree, rates)
    print(bo)


def valve_tree(tunnels, rates):
    """Create a tree with the distances to valves with positive flows only."""
    tree = distances(
        ["AA"] + [valve for valve, rate in rates.items() if rate > 0], tunnels
    )
    valve_tree = {}
    for start, distances_from_start in tree.items():
        valve_tree[start] = {}
        for end, distance_to_end in distances_from_start.items():
            if rates[end] > 0 and start != end:
                valve_tree[start][end] = distance_to_end
    return valve_tree


def best_order_dfs(tree, rates):
    """Traverse the tree using depth-first search to find the best order of actions and
    return the best one."""
    max_pressure = 0
    best_order = None
    to_open = sum(1 for _, rate in rates.items() if rate > 0) + 1
    stack = deque()
    stack.appendleft(("AA", {}, 30))
    while stack:
        current, visited, ttl = stack.pop()
        if ttl <= 0 or len(visited) == to_open:
            p = pressure(visited, rates)
            #             print(visited, p)
            if p > max_pressure:
                max_pressure = p
                best_order = visited
            continue
        if current not in visited:
            visited[current] = ttl
            for neighbor, distance in tree[current].items():
                stack.appendleft((neighbor, visited.copy(), ttl - distance - 1))
    return best_order, max_pressure


def distance(start, tunnels):
    """Calculate the shortest distance from start to every other node using the Dijkstra's
    algorithm."""
    distance = {start: 0}
    q = PriorityQueue()
    q.put((0, start))
    while not q.empty():
        _, current = q.get()
        for neighbor in tunnels[current]:
            if neighbor not in distance or distance[current] + 1 < distance[neighbor]:
                distance[neighbor] = distance[current] + 1
                q.put((distance[neighbor], neighbor))
    return distance


def distances(nodes, tunnels):
    """Calculate the shortest distances from every starting node in nodes to every other node."""
    distances = {}
    for node in nodes:
        distances[node] = distance(node, tunnels)
    return distances


def pressure(steps, rates):
    return sum(rates[valve] * time for valve, time in steps.items())


if __name__ == "__main__":
    main()
