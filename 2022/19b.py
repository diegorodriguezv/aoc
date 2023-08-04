import fileinput

ORE, CLAY, OBS, GEODE = 0, 1, 2, 3


def main():
    blueprints = get_blueprints()
    geodes = 1
    for blueprint in blueprints[:3]:
        geodes *= num_geodes(32, blueprint)
    print(geodes)


def get_blueprints():
    blueprints = []
    for line in fileinput.input():
        parts = line.strip().split(".")
        costs = []
        for part in parts:
            if not part:
                continue
            _, _, part = part.partition("costs ")
            ore, _, rest = part.partition(" ore")
            other = "0"
            if rest:
                _, _, other = rest.partition("and ")
                other = other.split()[0]
            costs.append((int(ore), int(other)))
        c1, c2, c3, c4 = costs
        blueprints.append(
            (
                (c1[0], 0, 0, 0),
                (c2[0], 0, 0, 0),
                (c3[0], c3[1], 0, 0),
                (c4[0], 0, c4[1], 0),
            )
        )
    return blueprints


def num_geodes(time_left, robot_costs):
    max_geodes = 0
    workers = (1, 0, 0, 0)
    resources = (0, 0, 0, 0)
    seen_at = {}
    workers_needed = get_workers_needed(robot_costs)
    stack = [(time_left, workers, resources, [False] * 4)]
    while stack:
        state = stack.pop()
        time_left, workers, resources, prevent_robots = state
        if seen_at.get((workers, resources), -1) >= time_left:
            continue
        seen_at[(workers, resources)] = time_left
        if time_left == 0:
            if resources[GEODE] > max_geodes:
                max_geodes = resources[GEODE]
            continue
        if possible_geodes(time_left, workers, resources) <= max_geodes:
            continue
        new_resources = collect_resources(workers, resources)
        new_prevent_robots = [False] * 4
        for resource in [ORE, CLAY, OBS, GEODE]:
            if has_enough(resources, robot_costs[resource]):
                new_prevent_robots[resource] = False if resource == GEODE else True
                if (
                    not prevent_robots[resource]
                    and workers_needed[resource] > workers[resource]
                ):
                    stack.append(
                        (
                            time_left - 1,
                            add_new_worker(workers, resource),
                            pay_cost(new_resources, robot_costs[resource]),
                            [False] * 4,
                        )
                    )
        stack.append((time_left - 1, workers, new_resources, new_prevent_robots))
    return max_geodes


def get_workers_needed(robot_costs):
    return tuple(map(max, zip(*robot_costs)))[:3] + (float("inf"),)


def possible_geodes(time, workers, resources):
    """Maximum number of geodes from the current state. Assuming that each minute a new
    geode robot is created."""
    current_geodes = resources[GEODE]
    current_robots = workers[GEODE]
    return current_geodes + current_robots * time + (time - 1) * time // 2


def add_new_worker(workers, kind):
    return workers[:kind] + (workers[kind] + 1,) + workers[kind + 1 :]


def pay_cost(resources, cost):
    def subtract_pair(pair):
        a, b = pair
        return a - b

    return tuple(map(subtract_pair, zip(resources, cost)))


def has_enough(resources, cost):
    return all(r >= 0 for r in pay_cost(resources, cost))


def collect_resources(workers, resources):
    return tuple(map(sum, zip(workers, resources)))


if __name__ == "__main__":
    main()
