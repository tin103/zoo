# File: graph_algo.py
import networkx as nx
from collections import deque
import itertools

# --- DUYỆT ĐỒ THỊ ---

def bfs_traversal(graph, start):
    """Duyệt đồ thị theo chiều rộng (BFS)"""
    visited = set()
    queue = deque([start])
    traversal_order = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            traversal_order.append(node)
            neighbors = sorted(list(graph.neighbors(node)))
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
    return traversal_order


def dfs_traversal(graph, start):
    """Duyệt đồ thị theo chiều sâu (DFS)"""
    visited = set()
    stack = [start]
    traversal_order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            traversal_order.append(node)
            neighbors = sorted(list(graph.neighbors(node)), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
    return traversal_order

# --- ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA) ---

def shortest_path(G, start, end):
    """Tìm đường đi ngắn nhất giữa start và end sử dụng Dijkstra"""
    weight_key = 'weight' if nx.get_edge_attributes(G, 'weight') else None
    try:
        path = nx.dijkstra_path(G, start, end, weight=weight_key)
        length = nx.dijkstra_path_length(G, start, end, weight=weight_key)
        return path, length
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, None

# --- CÂY KHUNG NHỎ NHẤT (MST) ---

def prim_mst_visualize(G):
    """Tìm Cây khung nhỏ nhất bằng Prim."""
    # NetworkX yêu cầu 'weight' cho MST, nếu không có sẽ dùng trọng số 1
    return nx.minimum_spanning_tree(G, algorithm="prim", weight="weight")

def kruskal_mst_visualize(G):
    """Tìm Cây khung nhỏ nhất bằng Kruskal."""
    return nx.minimum_spanning_tree(G, algorithm="kruskal", weight="weight")

# --- LUỒNG CỰC ĐẠI (MAX FLOW) ---

def ford_fulkerson_max_flow(G, source, sink):
    """Áp dụng thuật toán Ford-Fulkerson (hoặc Edmonds-Karp)"""
    if not G.is_directed():
        return "Lỗi: Thuật toán Max Flow chỉ áp dụng cho Đồ thị CÓ HƯỚNG.", 0, None

    # Kiểm tra thuộc tính 'capacity' (cần thiết cho Max Flow)
    if not nx.get_edge_attributes(G, 'capacity'):
         return "Lỗi: Các cạnh đồ thị cần thuộc tính 'capacity' để tính Max Flow.", 0, None
         
    try:
        # Sử dụng thuật toán Max Flow của NetworkX (thường là Edmonds-Karp)
        flow_value, flow_dict = nx.maximum_flow(G, source, sink, capacity='capacity')
        return "Thành công", flow_value, flow_dict
    except nx.NetworkXNoPath:
        return "Không có đường đi từ nguồn đến đích.", 0, None
    except nx.NetworkXError as e:
        return f"Lỗi: {e}", 0, None


# --- CHU TRÌNH/ĐƯỜNG ĐI EULER ---

def fleury_algorithm(G):
    """Thuật toán Fleury (Tìm chu trình Euler)"""
    if not nx.is_eulerian(G):
        return "Đồ thị không phải là đồ thị Euler (không có chu trình Euler)."
    
    # Sử dụng hàm có sẵn của NetworkX để tìm chu trình/đường đi
    circuit = list(nx.eulerian_circuit(G))
    
    # Định dạng chu trình để dễ đọc
    if circuit:
        path_str = ' -> '.join(f'{u}' for u, v in circuit)
        return f"Chu trình Euler tìm thấy: {path_str} -> {circuit[0][0]}"
    else:
        return "Lỗi: Không tìm thấy chu trình Euler dù đồ thị là Euler."


def hierholzer_algorithm(G):
    """Thuật toán Hierholzer (Tìm chu trình Euler)"""
    # Trong NetworkX, hàm eulerian_circuit