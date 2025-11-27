import heapq
import math

# -------------------------------
# 1. Haversine heuristic
# -------------------------------
def haversine(G, n1, n2):
    lat1, lon1 = G.nodes[n1]["y"], G.nodes[n1]["x"]
    lat2, lon2 = G.nodes[n2]["y"], G.nodes[n2]["x"]

    R = 6371000  # bán kính Trái Đất (m)

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))


# -------------------------------
# 2. A* Algorithm for Road Graph
# -------------------------------
def astar(G, start, goal):

    # Priority queue: (f_score, node)
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}            # parents
    g_cost = {start: 0}       # distance from start
    f_cost = {start: haversine(G, start, goal)}

    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # reconstruct path
            path = [goal]
            while path[-1] in came_from:
                path.append(came_from[path[-1]])
            return list(reversed(path)), g_cost[goal]

        closed.add(current)

        # explore neighbors
        for neighbor in G.neighbors(current):
            if neighbor in closed:
                continue

            edge_length = G[current][neighbor][0]["length"]

            tentative_g = g_cost[current] + edge_length

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + haversine(G, neighbor, goal)

                heapq.heappush(open_set, (f_cost[neighbor], neighbor))

    return None, float("inf")  # không tìm thấy đường