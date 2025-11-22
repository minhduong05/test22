# graph_loader.py
import networkx as nx
from astar import Graph, Edge

def load_graphml(path):
    nx_graph = nx.read_graphml(path)
    graph = Graph()

    # Load nodes
    for node in nx_graph.nodes:
        lat = float(nx_graph.nodes[node]["lat"])
        lon = float(nx_graph.nodes[node]["lon"])
        graph.nodes[node] = (lat, lon)
        graph.edges[node] = []

    # Load edges
    for u, v, data in nx_graph.edges(data=True):
        edge = Edge(
            to=v,
            distance_km=float(data["distance_km"]),
            base_weight=float(data["base_weight"]),
            traffic_level=float(data["traffic"]),
            allowed_vehicles=data["allowed"].split(","),
            flooded=data["flooded"] == "1"
        )
        graph.edges[u].append(edge)

    return graph
