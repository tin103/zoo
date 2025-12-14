# File: graph_core.py
import networkx as nx
import streamlit as st
import pandas as pd

# --- HÀM TẠO ĐỒ THỊ CHUNG ---

@st.cache_data(show_spinner=False)
def create_graph_from_input(data_string, is_directed=False, weighted=True):
    """Tạo đồ thị NetworkX từ chuỗi dữ liệu (u, v, weight)."""
    G = nx.DiGraph() if is_directed else nx.Graph()
    lines = data_string.strip().split('\n')
    
    for line in lines:
        parts = line.replace(',', ' ').split()
        if len(parts) < 2: continue

        u, v = parts[0], parts[1]
        weight = 1 
        
        if weighted and len(parts) >= 3:
            try:
                weight = float(parts[2])
            except ValueError:
                st.warning(f"Bỏ qua cạnh: Trọng số '{parts[2]}' không hợp lệ.")
                continue

        if weighted:
            G.add_edge(u, v, weight=weight)
        else:
            G.add_edge(u, v)

    return G

# --- HÀM TẠO ĐỒ THỊ THẢO CẦM VIÊN (Tọa độ Tinh chỉnh TRÊN ĐƯỜNG ĐI) ---
@st.cache_data(show_spinner=False)
def create_tcv_full_graph():
    G = nx.Graph()
    
    # 1. Tọa độ chuẩn hóa (x, y) - ĐÃ ĐIỀU CHỈNH TRÊN ĐƯỜNG MÀU TRẮNG
    positions = {
        # Khu vực Cổng chính/Phía Bắc
        "Cổng chính (N.T.M.K)": (0.05, 0.85),
        "Ngã 4 NMTK/Sân khấu": (0.15, 0.70),  # Nút giao mới, trên đường
        "Ngã 3 Hươu (1,8)": (0.20, 0.78),
        "Khu Hươu cao cổ (1)": (0.10, 0.67),
        "Khu thú móng guốc (3)": (0.28, 0.72),
        "Sân khấu (4)": (0.20, 0.60),
        "Khu ăn thịt nhỏ (5)": (0.35, 0.65),
        "Khu Hổ/Đười ươi (34)": (0.40, 0.75), 
        "Động vật châu Phi (7)": (0.45, 0.85),
        "Ngã 4 ĐV Châu Phi": (0.50, 0.75),    # Nút giao mới, trên đường
        "Khu Voi (2)": (0.60, 0.75),
        "Nhà ăn (31)": (0.60, 0.88),
        "Quầy bán hoa (40)": (0.75, 0.75),
        "Khu vui chơi T.Nhi (15,39)": (0.70, 0.80),
        
        # Khu vực Trung tâm/Phía Tây
        "Bảo tàng (10)": (0.20, 0.55),
        "Đền Hùng (11)": (0.25, 0.45),
        "Ngã 3 Đền Hùng": (0.30, 0.50),       # Nút giao mới, trên đường
        "Khu Khỉ/Vượn (12,20,23)": (0.35, 0.50), 
        "Khu Hà mã (16)": (0.50, 0.65),
        "Ngã 4 TCV/Hồ Trắng": (0.55, 0.60),   # Nút giao mới, trên đường
        "Khu Sư tử/Cáo (18)": (0.55, 0.55),
        "Hồ trắng (19)": (0.60, 0.60),
        
        # Khu vực Phía Nam/Hồ Lớn
        "Khu Chim Nước/Rái Cá (17,43)": (0.40, 0.35), 
        "Ngã 4 Chim Nước": (0.45, 0.40),      # Nút giao mới, trên đường
        "Chuồng Sếu (41)": (0.30, 0.35),
        "Ngã 3 Hồng Hạc": (0.30, 0.25),       # Nút giao mới, trên đường
        "Vườn Hồng hạc (37)": (0.35, 0.25),
        "Heo rừng (25)": (0.25, 0.25),
        "Di tích Q.N.Hương (49)": (0.10, 0.15),
        "Cổng Nguyễn Bỉnh Khiêm": (0.40, 0.05),
        "Hồ lớn/Đảo Sen (24)": (0.50, 0.25), 
        "Ngã 4 Quán giải khát": (0.55, 0.15), # Nút giao mới, trên đường
        "Quán giải khát (29)": (0.45, 0.15),
        "Hội trường (21)": (0.65, 0.10),
        "Khu Chim/Vườn Bướm (48)": (0.65, 0.20), 
        
        # Khu vực Phía Đông/Bò Sát
        "Ngã 4 Voi/Xe điện": (0.65, 0.70),    # Nút giao mới, trên đường
        "Trạm xe điện (9)": (0.70, 0.65),
        "Hồ Đông Dương (32)": (0.80, 0.60),
        "Ngã 3 Bò Sát/Hồ": (0.70, 0.30),      # Nút giao mới, trên đường
        "Nhà Bò Sát (6)": (0.75, 0.40),
        "Báo hoa mai (45)": (0.70, 0.25),
        "Khu Chim trĩ (22)": (0.60, 0.45),
        "Cổng N.H.Cảnh (52)": (0.90, 0.30),
        "Rắn hổ chúa (46)": (0.85, 0.20),
        "Vườn cá sấu (35)": (0.80, 0.10),
        "Ngã 3 Vườn N.N": (0.80, 0.05),       # Nút giao mới, trên đường
        "Vườn nông nghiệp (50)": (0.85, 0.05),
        "Linh cẩu/Cáo tuyết (27)": (0.70, 0.05),
        "Nhà vệ sinh (36)": (0.55, 0.05),
    }

    # 2. Định nghĩa các cạnh và trọng số (Giữ nguyên logic cạnh đã chia nhỏ)
    edges = [
        # Tuyến Cổng chính/Phía Bắc
        ("Cổng chính (N.T.M.K)", "Ngã 4 NMTK/Sân khấu", 1),
        ("Ngã 4 NMTK/Sân khấu", "Ngã 3 Hươu (1,8)", 1),
        ("Ngã 4 NMTK/Sân khấu", "Sân khấu (4)", 2),
        ("Ngã 3 Hươu (1,8)", "Khu Hươu cao cổ (1)", 2),
        ("Ngã 3 Hươu (1,8)", "Khu thú móng guốc (3)", 2),
        ("Khu thú móng guốc (3)", "Khu ăn thịt nhỏ (5)", 2),
        ("Khu ăn thịt nhỏ (5)", "Khu Hổ/Đười ươi (34)", 3),
        ("Khu Hổ/Đười ươi (34)", "Ngã 4 ĐV Châu Phi", 1), 
        ("Ngã 4 ĐV Châu Phi", "Động vật châu Phi (7)", 1),
        ("Ngã 4 ĐV Châu Phi", "Khu Voi (2)", 1),
        ("Ngã 4 ĐV Châu Phi", "Khu Hà mã (16)", 2),
        ("Nhà ăn (31)", "Động vật châu Phi (7)", 2), 
        ("Khu vui chơi T.Nhi (15,39)", "Nhà ăn (31)", 1),
        ("Quầy bán hoa (40)", "Khu vui chơi T.Nhi (15,39)", 1),

        # Tuyến Trung tâm/Phía Tây
        ("Sân khấu (4)", "Bảo tàng (10)", 1),
        ("Bảo tàng (10)", "Đền Hùng (11)", 2),
        ("Đền Hùng (11)", "Ngã 3 Đền Hùng", 1),
        ("Ngã 3 Đền Hùng", "Khu Khỉ/Vượn (12,20,23)", 2),
        ("Ngã 3 Đền Hùng", "Khu Chim trĩ (22)", 4),
        
        ("Khu Hà mã (16)", "Ngã 4 TCV/Hồ Trắng", 1),
        ("Khu Sư tử/Cáo (18)", "Ngã 4 TCV/Hồ Trắng", 1),
        ("Ngã 4 TCV/Hồ Trắng", "Hồ trắng (19)", 1),
        ("Ngã 4 TCV/Hồ Trắng", "Ngã 4 ĐV Châu Phi", 2),
        
        # Tuyến Phía Nam/Hồ Lớn
        ("Khu Khỉ/Vượn (12,20,23)", "Ngã 4 Chim Nước", 2),
        ("Ngã 4 Chim Nước", "Khu Chim Nước/Rái Cá (17,43)", 1),
        ("Ngã 4 Chim Nước", "Chuồng Sếu (41)", 2),
        ("Khu Chim Nước/Rái Cá (17,43)", "Hồ lớn/Đảo Sen (24)", 2),
        ("Chuồng Sếu (41)", "Ngã 3 Hồng Hạc", 1),
        ("Ngã 3 Hồng Hạc", "Vườn Hồng hạc (37)", 1),
        ("Ngã 3 Hồng Hạc", "Heo rừng (25)", 1),
        ("Heo rừng (25)", "Di tích Q.N.Hương (49)", 2),
        ("Di tích Q.N.Hương (49)", "Cổng Nguyễn Bỉnh Khiêm", 3),

        ("Hồ lớn/Đảo Sen (24)", "Ngã 4 Quán giải khát", 1),
        ("Ngã 4 Quán giải khát", "Quán giải khát (29)", 1),
        ("Ngã 4 Quán giải khát", "Hội trường (21)", 2),
        ("Ngã 4 Quán giải khát", "Nhà vệ sinh (36)", 1),
        ("Hội trường (21)", "Khu Chim/Vườn Bướm (48)", 1),
        
        # Tuyến Phía Đông
        ("Khu Chim/Vườn Bướm (48)", "Ngã 3 Bò Sát/Hồ", 1),
        ("Ngã 3 Bò Sát/Hồ", "Nhà Bò Sát (6)", 1),
        ("Ngã 3 Bò Sát/Hồ", "Báo hoa mai (45)", 1),
        ("Ngã 3 Bò Sát/Hồ", "Hồ Đông Dương (32)", 3),

        ("Nhà Bò Sát (6)", "Rắn hổ chúa (46)", 1),
        ("Rắn hổ chúa (46)", "Ngã 3 Vườn N.N", 2),
        ("Ngã 3 Vườn N.N", "Vườn cá sấu (35)", 1),
        ("Ngã 3 Vườn N.N", "Vườn nông nghiệp (50)", 1),
        ("Vườn cá sấu (35)", "Cổng N.H.Cảnh (52)", 2),
        
        ("Báo hoa mai (45)", "Khu Chim trĩ (22)", 1),
        ("Khu Chim trĩ (22)", "Trạm xe điện (9)", 2),
        ("Trạm xe điện (9)", "Ngã 4 Voi/Xe điện", 1),
        ("Trạm xe điện (9)", "Khu vui chơi T.Nhi (15,39)", 1),
        
        ("Vườn nông nghiệp (50)", "Linh cẩu/Cáo tuyết (27)", 1),
        ("Linh cẩu/Cáo tuyết (27)", "Hội trường (21)", 1),
        ("Nhà vệ sinh (36)", "Cổng Nguyễn Bỉnh Khiêm", 1),
    ]

    for node in positions: G.add_node(node)
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    
    return G, positions

# --- HÀM KIỂM TRA ĐỒ THỊ ---

def is_bipartite_graph(G):
    """Kiểm tra đồ thị hai phía."""
    try:
        is_bip = nx.is_bipartite(G)
        sets = nx.bipartite.sets(G) if is_bip else None
        return is_bip, sets
    except nx.NetworkXError:
        return False, None # Đồ thị có hướng không thể là Bipartite

# --- HÀM CHUYỂN ĐỔI BIỂU DIỄN ---

def to_adjacency_matrix(G):
    """Chuyển sang Ma trận kề."""
    return nx.adjacency_matrix(G).todense().tolist()

def to_adjacency_list(G):
    """Chuyển sang Danh sách kề."""
    return nx.to_dict_of_lists(G)

def to_edge_list(G):
    """Chuyển sang Danh sách cạnh."""
    # Thêm cột 'type' cho đồ thị có hướng để phân biệt (DiGraph vs Graph)
    data = list(G.edges(data=True))
    if not data: return []
    
    if 'weight' in data[0][2]:
        return [(u, v, d['weight']) for u, v, d in data]
    else:
        return [(u, v, 1) for u, v, d in data]