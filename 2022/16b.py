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
    tree = valve_tree(tunnels, rates)
    orders = all_orders_dfs(tree, rates)
    keys = keys_from_tree(tree)
    print(len(orders))
    pairs = []
    for order1, p1 in orders.items():
        for order2, p2 in orders.items():
            if not share_steps(order1, order2):
                pairs.append((order1, order2, p1 + p2))
    print(len(pairs))
    if pairs:
        pairs.sort(key=lambda p: p[2], reverse=True)
        largest_pair = pairs[0]
        print(nodes(largest_pair[0], keys), nodes(largest_pair[1], keys))
        print(largest_pair)


def share_steps(order1, order2):
    """Determine if the paths order1 and order2 share steps beside "AA" (1)."""
    return (order1 ^ 1) & (order2 ^ 1)


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


def bitset(path, keys):
    """Return the bitset representation of a path in tree."""
    bits = 0
    for step in path:
        bits |= keys[step]
    return bits


def nodes(bitset, keys):
    """Return the set of nodes represented by a bitset."""
    nodes = set()
    for k, mask in keys.items():
        if bitset & mask:
            nodes.add(k)
    return nodes


def keys_from_tree(tree):
    """Return a dict assigning a bit position to each node."""
    keys = {}
    bit = 1
    for k in sorted(tree.keys()):
        keys[k] = bit
        bit <<= 1
    return keys


def all_orders_dfs(tree, rates):
    """Traverse the tree using depth-first search to find all orders of actions.
    Returns a dict of all combinations of visited valves as the key (a bitset) with the maximum
    pressure for that combination as the value."""
    keys = keys_from_tree(tree)
    orders = {}
    to_open = sum(1 for _, rate in rates.items() if rate > 0) + 1
    stack = deque()
    stack.appendleft(("AA", {}, 26))
    while stack:
        current, visited, ttl = stack.pop()
        p = pressure(visited, rates)
        bits = bitset(visited, keys)
        if orders.get(bits, 0) < p:
            orders[bits] = p
        if ttl <= 0 or len(visited) == to_open:
            continue
        if current not in visited:
            visited[current] = ttl
            for neighbor, distance in tree[current].items():
                stack.appendleft((neighbor, visited.copy(), ttl - distance - 1))
    return orders


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
