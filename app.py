# File: app.py (Phiên bản nhập tọa độ Data Editor + Công cụ lấy tọa độ + Slider Zoom)

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import io

# --- QUAN TRỌNG: ĐẢM BẢO FILE visualize.py ĐÃ ĐƯỢC CẬP NHẬT ---
from visualize import draw_graph_map, create_mock_tcv_graph_image 

# =================================================================
# I. CÁC HÀM XỬ LÝ ĐỒ THỊ VÀ TỌA ĐỘ
# (Giữ nguyên)
# =================================================================

# --- HÀM TẠO CẤU TRÚC ĐỒ THỊ CƠ SỞ (100 Nodes - ĐÃ ĐẢO NGƯỢC TỌA ĐỘ Y) ---
@st.cache_data(show_spinner=False)
def create_tcv_full_graph_base():
    G = nx.Graph()
    
    # 1. Tọa độ chuẩn hóa (x, y) - Đã áp dụng Y_mới = 1.0 - Y_cũ cho tất cả nodes
    positions = {
        # Nodes cũ (0-48)
        0: (0.0001, 0.1499), 1: (0.1500, 0.3000), 2: (0.2000, 0.2200), 
        3: (0.1000, 0.3300), 4: (0.2800, 0.2800), 5: (0.2000, 0.4000), 
        6: (0.3500, 0.3500), 7: (0.4000, 0.2500), 8: (0.4500, 0.1500), 
        9: (0.5000, 0.2500), 10: (0.6000, 0.2500), 11: (0.5000, 0.3500), 
        12: (0.5500, 0.4000), 13: (0.5500, 0.4500), 14: (0.6000, 0.4000), 
        15: (0.6000, 0.1200), 16: (0.7500, 0.2500), 17: (0.7000, 0.2000), 
        18: (0.6500, 0.3000), 19: (0.7000, 0.3500), 20: (0.8000, 0.4000), 
        21: (0.2000, 0.4500), 22: (0.2500, 0.5500), 23: (0.3000, 0.5000), 
        24: (0.3500, 0.5000), 25: (0.6000, 0.5500), 26: (0.4500, 0.6000), 
        27: (0.4000, 0.6500), 28: (0.3000, 0.6500), 29: (0.3000, 0.7500), 
        30: (0.3500, 0.7500), 31: (0.2500, 0.7500), 32: (0.1000, 0.8500), 
        33: (0.4000, 0.9999), 34: (0.5000, 0.7500), 35: (0.5500, 0.8500), 
        36: (0.4500, 0.8500), 37: (0.6500, 0.9000), 38: (0.5500, 0.9500), 
        39: (0.6500, 0.8000), 40: (0.7000, 0.7000), 41: (0.7500, 0.6000), 
        42: (0.7000, 0.7500), 43: (1.0000, 0.7000), 44: (0.8500, 0.8000), 
        45: (0.8000, 0.9000), 46: (0.8000, 0.9500), 47: (0.8500, 0.9500), 
        48: (0.7000, 0.9500), 

        # Nodes mới (49-99) - Y đã được đảo ngược
        49: (0.0750, 0.2400), 50: (0.1700, 0.2600), 51: (0.2200, 0.3200), 
        52: (0.3200, 0.3000), 53: (0.4200, 0.2000), 54: (0.5500, 0.1900), 
        55: (0.6700, 0.2300), 56: (0.7200, 0.3000), 57: (0.8500, 0.3000), 
        58: (0.8500, 0.5000), 59: (0.2000, 0.5000), 60: (0.2700, 0.5300), 
        61: (0.4500, 0.4500), 62: (0.6000, 0.4800), 63: (0.5000, 0.5500), 
        64: (0.4000, 0.6000), 65: (0.3500, 0.7000), 66: (0.2000, 0.7000), 
        67: (0.1500, 0.8000), 68: (0.3500, 0.9000), 69: (0.4500, 0.8000), 
        70: (0.6000, 0.7500), 71: (0.7000, 0.8500), 72: (0.8000, 0.6500), 
        73: (0.7700, 0.8000), 74: (0.9000, 0.7500), 75: (0.7500, 0.8500), 
        76: (0.6500, 0.9300), 77: (0.5000, 0.9500), 78: (0.8200, 0.9300), 
        79: (0.1200, 0.4000), 80: (0.2800, 0.4500), 81: (0.4000, 0.4000), 
        82: (0.5000, 0.0000), 83: (0.9000, 0.1000), 84: (0.9500, 0.6000), 
        85: (0.0500, 0.9500), 86: (0.7500, 0.5000), 87: (0.6500, 0.5000), 
        88: (0.4500, 0.5000), 89: (0.3500, 0.6000), 90: (0.4000, 0.9000), 
        91: (0.5000, 0.9000), 92: (0.6000, 0.9300), 93: (0.8500, 0.8500), 
        94: (0.1000, 0.1200), 95: (0.7500, 0.1500), 96: (0.5000, 0.6500), 
        97: (0.2500, 0.3500), 98: (0.7500, 0.6500), 99: (0.1500, 0.6500)
    }

    # 2. Định nghĩa các cạnh và trọng số (100 Edges)
    edges = [
        (0, 49, 0.5), (49, 1, 0.5), (49, 2, 0.8), (1, 5, 2), (2, 50, 1), 
        (50, 3, 1), (50, 4, 1), (4, 52, 1), (52, 6, 1), (6, 7, 3), 
        (7, 53, 1), (53, 9, 0.5), (53, 8, 0.5), (9, 10, 1), (9, 11, 2), 
        (15, 8, 2), (17, 55, 0.5), (55, 10, 0.5), (17, 16, 1), (5, 21, 1), 
        (21, 59, 1), (59, 22, 1), (22, 60, 0.5), (60, 23, 0.5), (23, 24, 2), 
        (23, 25, 4), (11, 12, 1), (13, 12, 1), (12, 14, 1), (12, 9, 2), 
        (24, 88, 1.5), (88, 26, 0.5), (26, 64, 0.5), (64, 27, 0.5), 
        (27, 65, 1), (65, 30, 0.5), (65, 29, 0.5), (28, 66, 0.5), 
        (66, 31, 0.5), (31, 67, 1), (67, 32, 1), (32, 85, 1), (85, 33, 2), 
        (34, 69, 1), (69, 36, 0.5), (69, 35, 0.5), (35, 91, 0.5), 
        (91, 38, 0.5), (37, 76, 0.5), (76, 48, 0.5), (37, 71, 1), 
        (71, 39, 1), (39, 40, 1), (40, 98, 0.5), (98, 41, 0.5), 
        (40, 72, 1), (72, 20, 2), (41, 73, 0.5), (73, 44, 0.5), 
        (44, 93, 1), (93, 46, 1), (46, 78, 0.5), (78, 47, 0.5), 
        (45, 93, 1), (45, 78, 0.5), (43, 74, 0.5), (74, 44, 1.5), 
        (42, 25, 1), (25, 87, 1), (87, 19, 1), (19, 56, 0.5), 
        (56, 18, 0.5), (19, 17, 1), (47, 48, 1), (38, 77, 0.5), 
        (77, 33, 0.5), (48, 76, 0.5), (76, 37, 0.5), (37, 92, 0.5), 
        (92, 38, 0.5), 
        (1, 97, 1), (97, 5, 1), (97, 52, 1), (88, 61, 1), (61, 11, 1), 
        (88, 63, 0.5), (63, 14, 1), (63, 25, 1), (63, 26, 1), 
        (69, 70, 1), (70, 39, 1), (70, 34, 1), (71, 75, 1), (75, 42, 1),
        (86, 20, 1), (86, 14, 1), (86, 40, 1), (54, 15, 1), (54, 95, 1), 
        (95, 16, 1), (94, 0, 0.5), (94, 3, 1), (80, 21, 1), (80, 24, 1), 
        (80, 88, 1), (90, 33, 0.5), (90, 68, 0.5), (90, 38, 0.5),
        (37, 90, 1), (35, 90, 0.5), (64, 89, 0.5), (89, 27, 0.5), 
        (89, 34, 1), (66, 99, 0.5), (99, 28, 0.5), (99, 31, 0.5),
        (82, 15, 0.5), (82, 8, 0.5), (83, 16, 0.5), (83, 20, 0.5),
        (84, 43, 0.5), (84, 20, 0.5)
    ]

    for node in positions: G.add_node(node)
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    
    return G, positions

# --- ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA) ---
def shortest_path(G, start, end):
    weight_key = 'weight' if nx.get_edge_attributes(G, 'weight') else None
    try:
        path = nx.dijkstra_path(G, start, end, weight=weight_key)
        length = nx.dijkstra_path_length(G, start, end, weight=weight_key)
        return path, length
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, None

# =================================================================
# II. STREAMLIT APP LOGIC 
# =================================================================

st.set_page_config(layout="wide", page_title="Bản đồ TCV - Chỉnh sửa Tọa độ")
st.title("🗺️ Bản đồ Thảo Cầm Viên - Công cụ Chỉnh sửa Tọa độ Node (0-99)")

# Tải đồ thị cơ sở 
G_TCV_base, pos_TCV_base = create_tcv_full_graph_base() 
nodes_TCV = sorted(list(G_TCV_base.nodes)) 
display_nodes = [f"Node {num}" for num in nodes_TCV]
image_path = "thao_cam_vien.jpg"
full_image_path = os.path.join("assets", image_path)


# --- 1. HIỆU CHỈNH TỌA ĐỘ TRONG SIDEBAR (Dùng Data Editor) ---

if 'edited_positions_df' not in st.session_state:
    df_init = pd.DataFrame.from_dict(
        pos_TCV_base, 
        orient='index', 
        columns=['x', 'y']
    )
    df_init.index.name = 'Node'
    df_init = df_init.reset_index()
    
    st.session_state.edited_positions_df = df_init
    st.session_state.edited_positions_df['x'] = st.session_state.edited_positions_df['x'].round(4)
    st.session_state.edited_positions_df['y'] = st.session_state.edited_positions_df['y'].round(4)


st.sidebar.header("🛠️ Hiệu chỉnh Tọa độ Node (0.0001 đến 1.0000)")
st.sidebar.info("Chỉnh sửa tọa độ X (ngang) và Y (dọc) của từng Node bằng tay.")

edited_df = st.sidebar.data_editor(
    st.session_state.edited_positions_df,
    num_rows="fixed",
    column_order=("Node", "x", "y"),
    column_config={
        "Node": st.column_config.Column("Node", disabled=True, width='small'),
        "x": st.column_config.NumberColumn("Tọa độ X", format="%.4f", min_value=0.0001, max_value=1.0000, width='small'),
        "y": st.column_config.NumberColumn("Tọa độ Y", format="%.4f", min_value=0.0001, max_value=1.0000, width='small'),
    },
    use_container_width=True,
    key='coord_editor_widget'
)

st.session_state.edited_positions_df = edited_df

# Chuyển DataFrame đã chỉnh sửa về Dictionary để vẽ đồ thị
current_pos_dict = {
    row['Node']: (row['x'], row['y'])
    for index, row in edited_df.iterrows()
}

# --- 2. LOGIC TÌM ĐƯỜNG (MAIN CONTENT) ---
st.subheader("1. Tìm Đường đi Ngắn nhất")
col1, col2 = st.columns(2)
with col1: 
    start_node_str = st.selectbox("Điểm Bắt đầu:", display_nodes, key="tcv_start", index=0)
    start_node = int(start_node_str.split(' ')[1]) 
with col2: 
    end_node_str = st.selectbox("Điểm Kết thúc:", display_nodes, key="tcv_end")
    end_node = int(end_node_str.split(' ')[1]) 

path = None
length = None
edges_to_highlight = None

if start_node and end_node and start_node != end_node:
    path, length = shortest_path(G_TCV_base, start_node, end_node)

    if path:
        path_display = [str(node) for node in path]
        st.success(f"Đường đi: {' -> '.join(path_display)} | Tổng thời gian ước tính: **{length} phút**")
        edges_to_highlight = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    else:
        st.warning(f"Không tìm thấy đường đi giữa **{start_node_str}** và **{end_node_str}**.")
elif start_node == end_node and start_node is not None:
    st.info("Vui lòng chọn hai điểm khác nhau để tìm đường đi.")

st.markdown("---")


# --- 3. CÔNG CỤ XÁC ĐỊNH TỌA ĐỘ TRÊN BẢN ĐỒ ---
st.subheader("2. Công cụ Hỗ trợ Xác định Tọa độ")
st.info("Click vào bất kỳ điểm nào trên bản đồ dưới đây để nhận tọa độ chuẩn hóa (0.0001 - 1.0000). Sau đó, bạn chỉ cần sao chép giá trị này vào cột X hoặc Y trong sidebar.")

if os.path.exists(full_image_path):
    # Dùng ảnh nền bản đồ cho công cụ lấy tọa độ
    image_to_click = Image.open(full_image_path)
    
    # Hiển thị ảnh và bắt sự kiện click
    value = streamlit_image_coordinates(image_to_click, key="coord_finder", width=700)
    
    col_x, col_y = st.columns(2)
    
    if value:
        x_click = value['x']
        y_click = value['y']
        w_widget = value['width']
        h_widget = value['height']

        # Chuẩn hóa tọa độ click về khoảng [0.0001, 1.0000]
        x_normalized = x_click / w_widget
        y_normalized = y_click / h_widget
        
        x_final = max(0.0001, min(1.0000, x_normalized))
        y_final = max(0.0001, min(1.0000, y_normalized))
        
        with col_x:
            st.code(f"Tọa độ X (Ngang): {x_final:.4f}")
        with col_y:
            st.code(f"Tọa độ Y (Dọc): {y_final:.4f}")
            
        st.success("Tọa độ đã sẵn sàng. Sao chép và dán vào bảng Data Editor bên trái.")
        
    else:
        with col_x: st.code("Tọa độ X: 0.0000")
        with col_y: st.code("Tọa độ Y: 0.0000")
        
else:
    st.warning(f"Không tìm thấy file ảnh bản đồ `{image_path}` trong thư mục `assets`. Không thể hiển thị công cụ lấy tọa độ.")


st.markdown("---")

# --- 4. VẼ BẢN ĐỒ VỚI TỌA ĐỘ ĐÃ CHỈNH SỬA VÀ THÊM SLIDER ZOOM ---
st.subheader("3. Bản đồ Đồ thị (Sử dụng thanh trượt Zoom)")

# Thanh trượt điều khiển Zoom
zoom_level = st.slider(
    'Mức độ Zoom (0.0: Max Zoom Out, 1.0: Max Zoom In)',
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.01,
    format='%.2f'
)

# Tính toán giới hạn trục dựa trên mức zoom (Giả định trung tâm là 0.5, 0.5)
# Tỷ lệ: khi zoom_level = 0.0 -> view_range = 1.0 (toàn bộ bản đồ)
# khi zoom_level = 1.0 -> view_range = 0.1 (zoom in 10 lần)
view_range = 1.0 - (zoom_level * 0.9) # Range từ 1.0 đến 0.1 (tức là 10% kích thước)
center_x, center_y = 0.5, 0.5 # Giữ trung tâm bản đồ

# Tính toán giới hạn trục mới
x_min = center_x - (view_range / 2)
x_max = center_x + (view_range / 2)
y_min = center_y - (view_range / 2)
y_max = center_y + (view_range / 2)

# Điều chỉnh lại nếu vượt quá giới hạn 0-1 (chỉ là biện pháp phòng ngừa)
x_min = max(0.0, x_min)
x_max = min(1.0, x_max)
y_min = max(0.0, y_min)
y_max = min(1.0, y_max)

# Tạo Figure Matplotlib và truyền giới hạn trục mới vào
fig = draw_graph_map(
    G_TCV_base, 
    current_pos_dict, 
    image_path, 
    edges_to_highlight, 
    title="Đường đi Ngắn nhất trên Bản đồ TCV",
    x_lim=(x_min, x_max), # <--- THAM SỐ MỚI
    y_lim=(y_min, y_max)  # <--- THAM SỐ MỚI
) 

# Sử dụng st.pyplot() để kích hoạt Matplotlib Toolbar (vẫn dùng được Zoom/Pan của Matplotlib)
st.pyplot(fig, use_container_width=True)