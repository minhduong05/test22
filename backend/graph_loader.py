from astar import astar, haversine
import networkx as nx

# ---- 1. Load GraphML ----
graphml_file = r"D:\study\minh\map_data\graph_all.graphml"
G = nx.read_graphml(graphml_file)

# ---- 2. Chuyển kiểu dữ liệu node ----
for n, data in G.nodes(data=True):

    # Tọa độ bắt buộc cần cho A*
    if "x" in data:
        data["x"] = float(data["x"])
    if "y" in data:
        data["y"] = float(data["y"])

    # Xóa các thuộc tính không cần thiết
    keys_to_remove = [k for k in data.keys() if k not in ("x", "y")]
    for k in keys_to_remove:
        del data[k]

# ---- 3. Chuyển kiểu dữ liệu edge ----
for u, v, data in G.edges(data=True):

    # length là duy nhất cần cho A*
    if "length" in data:
        data["length"] = float(data["length"])
    else:
        data["length"] = 0.0   # đề phòng thiếu dữ liệu

    # Xóa thuộc tính không cần thiết
    keys_to_keep = ("length",)
    for k in list(data.keys()):
        if k not in keys_to_keep:
            del data[k]

