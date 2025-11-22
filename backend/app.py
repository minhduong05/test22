import os
import sys
from Flask import Flask, render_template, request, jsonify

# Import module của bạn
import graph_loader
from astar import astar  # Import hàm astar

# --- CẤU HÌNH ĐƯỜNG DẪN (Như đã thảo luận) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'Frontend')
STATIC_DIR = os.path.join(ROOT_DIR, 'Frontend') # Nếu để css/js chung với html
MAP_DATA_DIR = os.path.join(ROOT_DIR, 'map_data')

# Khởi tạo Flask
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# --- BIẾN TOÀN CỤC ĐỂ LƯU ĐỒ THỊ ---
global_graph = None

def initialize_graph():
    """Hàm load graph khi khởi động server"""
    global global_graph
    graph_path = os.path.join(MAP_DATA_DIR, 'graph.graphml')
    
    if os.path.exists(graph_path):
        try:
            print(f"⚡ Đang tải bản đồ từ: {graph_path}...")
            # Gọi hàm load_graphml từ file graph_loader.py của bạn
            global_graph = graph_loader.load_graphml(graph_path)
            print(f"✅ Tải thành công! Số node: {len(global_graph.nodes)}")
        except Exception as e:
            print(f"❌ Lỗi khi tải graph: {e}")
    else:
        print(f"❌ Không tìm thấy file graph tại: {graph_path}")

# Gọi hàm load ngay lập tức
initialize_graph()

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/find_path', methods=['POST'])
def find_path_api():
    """API nhận start/end node ID và trả về đường đi"""
    if not global_graph:
        return jsonify({'error': 'Graph chưa được load'}), 500

    data = request.json
    start_node = data.get('start_node') # Node ID (ví dụ: "n0")
    end_node = data.get('end_node')     # Node ID (ví dụ: "n10")
    vehicle_type = data.get('vehicle', 'car') # car, bike, walk...

    if not start_node or not end_node:
        return jsonify({'error': 'Thiếu điểm đi hoặc điểm đến'}), 400
    
    if start_node not in global_graph.nodes or end_node not in global_graph.nodes:
        return jsonify({'error': 'ID điểm không tồn tại trong bản đồ'}), 404

    # --- GỌI THUẬT TOÁN ASTAR CỦA BẠN ---
    path_ids, total_cost = astar(global_graph, start_node, end_node, vehicle_type)

    if path_ids is None:
        return jsonify({'success': False, 'message': 'Không tìm thấy đường đi'}), 200

    # --- QUAN TRỌNG: CHUYỂN ĐỔI NODE ID SANG TỌA ĐỘ (LAT, LON) ---
    # Frontend cần tọa độ để vẽ line, chứ không vẽ được bằng ID
    path_coords = []
    for node_id in path_ids:
        lat, lon = global_graph.nodes[node_id]
        path_coords.append({
            'id': node_id,
            'lat': lat,
            'lon': lon
        })

    return jsonify({
        'success': True,
        'path': path_coords, # List các tọa độ
        'cost': total_cost
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)