# File: app.py (Phiên bản Đã loại bỏ Node 0)

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
# =================================================================

# --- HÀM TẠO CẤU TRÚC ĐỒ THỊ CƠ SỞ (CHỈ CÓ NODES TỪ 1 ĐẾN 71) ---
@st.cache_data(show_spinner=False)
def create_tcv_full_graph_base():
    G = nx.Graph()
    
    # 1. Tọa độ chuẩn hóa (x, y) - CHỈ CÓ NODES TỪ 1 ĐẾN 71
    positions = {
        1: (0.6071, 0.5700), 2: (0.4543, 0.6900),
        3: (0.5014, 0.5515), 4: (0.4157, 0.6400), 5: (0.3614, 0.6313),
        6: (0.3929, 0.4506), 7: (0.3843, 0.3000), 8: (0.4571, 0.2950),
        9: (0.4200, 0.1810), 10: (0.5457, 0.2540), 11: (0.6129, 0.4520),
        12: (0.6629, 0.4320), 13: (0.6943, 0.4900), 14: (0.6457, 0.5270),
        15: (0.7329, 0.5700), 16: (0.7443, 0.4300), 17: (0.8229, 0.4500),
        18: (0.7900, 0.5000), 19: (0.6243, 0.5100), 20: (0.6643, 0.3500),
        21: (0.7743, 0.1800), 22: (0.7014, 0.3000), 23: (0.7557, 0.2900),
        24: (0.8600, 0.1900), 25: (0.7240, 0.6500), 26: (0.8886, 0.2400),
        27: (0.8886, 0.2500), 28: (0.8714, 0.3100), 29: (0.8257, 0.3500),
        30: (0.6643, 0.5400), 31: (0.8800, 0.3500), 32: (0.9586, 0.3400),
        33: (0.9414, 0.2600), 34: (0.8986, 0.4900), 35: (0.8900, 0.5300),
        36: (0.5300, 0.4000), 37: (0.4557, 0.4800), 38: (0.3243, 0.4500),
        39: (0.3329, 0.6300), 40: (0.5500, 0.4700), 41: (0.5743, 0.2900),
        42: (0.8014, 0.1800), 43: (0.4386, 0.5500), 44: (0.3929, 0.5700),
        45: (0.3929, 0.6600), 46: (0.3871, 0.6800), 47: (0.9057, 0.2700),
        48: (0.7229, 0.5100), 49: (0.7700, 0.4500), 50: (0.9671, 0.3000),
        51: (0.2929, 0.2500), 52: (0.5186, 0.3500), 53: (0.5257, 0.1800),
        54: (0.6014, 0.3500), 55: (0.6100, 0.2000), 56: (0.7600, 0.4100),
        57: (0.8300, 0.3800), 58: (0.8943, 0.3900), 59: (0.8671, 0.4700),
        60: (0.8257, 0.6000), 61: (0.7900, 0.3900), 62: (0.7500, 0.6000),
        63: (0.5000, 0.5500), 64: (0.6557, 0.5800), 65: (0.5443, 0.5800),
        66: (0.3486, 0.5800), 67: (0.5143, 0.4900), 68: (0.5171, 0.4000),
        69: (0.7943, 0.3500), 70: (0.7500, 0.2500), 71: (0.6929, 0.1900)
    }

    # 2. Định nghĩa các cạnh và trọng số (ĐÃ XÓA CẠNH LIÊN QUAN ĐẾN NODE 0)
    edges = [
        # Khu vực phía Tây/Tây Bắc (1-9, 38, 39, 44, 45, 46, 51)
        (9, 53, 1), (53, 10, 1), (53, 8, 1), (8, 7, 1),
        (7, 51, 1), (51, 38, 1), (38, 6, 1), (6, 37, 1), (37, 43, 1),
        (43, 44, 1), (44, 66, 1), (66, 39, 1), (39, 5, 1), (5, 4, 1),
        (4, 2, 1), (2, 46, 1), (46, 45, 1), (45, 39, 1),

        # Khu vực Trung tâm/Hồ (1, 3, 14, 19, 30, 40, 63, 65, 67, 68)
        (43, 63, 1), (63, 3, 1), (3, 65, 1), (65, 1, 1), (1, 64, 1),
        (64, 14, 1), (14, 30, 1), (30, 19, 1), (19, 48, 1), (48, 15, 1),
        (40, 67, 1), (67, 43, 1), (67, 68, 1), (68, 36, 1), (36, 52, 1),
        (52, 40, 1), (40, 37, 1), (40, 11, 1), (11, 12, 1), (12, 13, 1),
        (13, 48, 1), (14, 19, 1), (19, 64, 1), (64, 1, 1), (3, 67, 1),

        # Khu vực Đông/Đông Nam (15, 16, 17, 18, 20, 49, 56, 57, 59, 60, 62)
        (15, 62, 1), (62, 25, 1), (25, 60, 1), (60, 17, 1), (17, 59, 1),
        (59, 34, 1), (34, 35, 1), (35, 58, 1), (58, 31, 1), (31, 29, 1),
        (29, 57, 1), (57, 61, 1), (61, 69, 1), (69, 56, 1), (56, 49, 1),
        (49, 15, 1), (49, 16, 1), (16, 20, 1), (20, 54, 1), (54, 41, 1),
        (41, 22, 1), (22, 70, 1), (70, 23, 1), (23, 69, 1), (69, 57, 1),
        (57, 17, 1), (17, 18, 1), (18, 48, 1), (56, 18, 1), (18, 59, 1),

        # Khu vực Đông Bắc/Lối ra (21, 24, 26, 27, 28, 32, 33, 42, 47, 50, 71)
        (21, 42, 1), (42, 24, 1), (24, 26, 1), (26, 27, 1), (27, 47, 1),
        (47, 33, 1), (33, 32, 1), (32, 50, 1), (50, 31, 1), (31, 28, 1),
        (28, 29, 1), (29, 69, 1), (69, 20, 1), (20, 71, 1), (71, 55, 1),
        (55, 21, 1), (21, 70, 1), (24, 28, 1), (24, 42, 1), (26, 47, 1),
        (33, 50, 1), (47, 58, 1),
        
        # Liên kết chéo quan trọng
        (5, 44, 1.5), (38, 7, 1.5), (63, 67, 0.5), (11, 40, 0.5), 
        (13, 16, 2), (25, 48, 1), (60, 62, 0.5), (34, 59, 0.5),
        (58, 34, 1.5), (32, 33, 0.5), (10, 52, 0.5), (36, 68, 0.5),
        (12, 14, 0.5), (17, 60, 0.5), (25, 62, 0.5), (30, 64, 0.5)
    ]

    # Chỉ thêm các Nodes có trong danh sách tọa độ (1-71)
    for node in positions: 
        G.add_node(node)

    for u, v, w in edges: 
        # Chỉ thêm cạnh nếu cả hai node đều tồn tại trong G (1-71)
        if u in G.nodes and v in G.nodes:
            G.add_edge(u, v, weight=w) 
    
    # Lọc lại positions chỉ giữ các nodes đã được thêm vào G
    valid_positions = {k: v for k, v in positions.items() if k in G.nodes}
    
    return G, valid_positions

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
st.title("🗺️ Bản đồ TCV - Công cụ Chỉnh sửa Tọa độ Node (1-71)")

# Tải đồ thị cơ sở 
G_TCV_base, pos_TCV_base = create_tcv_full_graph_base() 
nodes_TCV = sorted(list(G_TCV_base.nodes)) 
# Khi node 0 bị loại bỏ, Node đầu tiên là 1
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


st.sidebar.header("🛠️ Hiệu chỉnh Tọa độ Node (1 đến 71)")
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
# Điều chỉnh index mặc định cho Node 1 và Node 2
start_node_index = 0 
end_node_index = 1 if len(display_nodes) > 1 else 0

with col1: 
    start_node_str = st.selectbox("Điểm Bắt đầu:", display_nodes, key="tcv_start", index=start_node_index)
    start_node = int(start_node_str.split(' ')[1]) 
with col2: 
    end_node_str = st.selectbox("Điểm Kết thúc:", display_nodes, key="tcv_end", index=end_node_index)
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
    image_to_click = Image.open(full_image_path)
    value = streamlit_image_coordinates(image_to_click, key="coord_finder", width=700)
    
    col_x, col_y = st.columns(2)
    
    if value:
        x_click = value['x']
        y_click = value['y']
        w_widget = value['width']
        h_widget = value['height']

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

zoom_level = st.slider(
    'Mức độ Zoom (0.0: Max Zoom Out, 1.0: Max Zoom In)',
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.01,
    format='%.2f'
)

view_range = 1.0 - (zoom_level * 0.9)
center_x, center_y = 0.5, 0.5 

x_min = center_x - (view_range / 2)
x_max = center_x + (view_range / 2)
y_min = center_y - (view_range / 2)
y_max = center_y + (view_range / 2)

x_min = max(0.0, x_min)
x_max = min(1.0, x_max)
y_min = max(0.0, y_min)
y_max = min(1.0, y_max)

fig = draw_graph_map(
    G_TCV_base, 
    current_pos_dict, 
    image_path, 
    edges_to_highlight, 
    title="Đường đi Ngắn nhất trên Bản đồ TCV",
    x_lim=(x_min, x_max),
    y_lim=(y_min, y_max)
) 

st.pyplot(fig, use_container_width=True)
