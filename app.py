# File: app.py (Phiên bản Đã loại bỏ Node 0)

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

from visualize import draw_graph_map, create_mock_tcv_graph_image 

# =================================================================
# I. TẠO ĐỒ THỊ & TỌA ĐỘ
# =================================================================

@st.cache_data(show_spinner=False)
def create_tcv_full_graph_base():
    G = nx.Graph()

    positions = {
        1: (0.7086, 0.5900), 2: (0.6071, 0.5700), 3: (0.4543, 0.6900),
        4: (0.5014, 0.5515), 5: (0.4157, 0.6400), 6: (0.3614, 0.6313),
        7: (0.3929, 0.4506), 8: (0.3843, 0.3000), 9: (0.4571, 0.2950),
        10: (0.4200, 0.1810), 11: (0.5457, 0.2540), 12: (0.6129, 0.4520),
        13: (0.6629, 0.4320), 14: (0.6943, 0.4900), 15: (0.6457, 0.5270),
        16: (0.7329, 0.5700), 17: (0.7443, 0.4300), 18: (0.8229, 0.4500),
        19: (0.7900, 0.5000), 20: (0.6243, 0.5100), 21: (0.6643, 0.3500),
        22: (0.7743, 0.1800), 23: (0.7014, 0.3000), 24: (0.7557, 0.2900),
        25: (0.8600, 0.1900), 26: (0.7240, 0.6500), 27: (0.8886, 0.2400),
        28: (0.8886, 0.2500), 29: (0.8714, 0.3100), 30: (0.8257, 0.3500),
        31: (0.6643, 0.5400), 32: (0.8800, 0.3500), 33: (0.9586, 0.3400),
        34: (0.9414, 0.2600), 35: (0.8986, 0.4900), 36: (0.8900, 0.5300),
        37: (0.5300, 0.4000), 38: (0.4557, 0.4800), 39: (0.3243, 0.4500),
        40: (0.3329, 0.6300), 41: (0.5500, 0.4700), 42: (0.5743, 0.2900),
        43: (0.8014, 0.1800), 44: (0.4386, 0.5500), 45: (0.3929, 0.5700),
        46: (0.3929, 0.6600), 47: (0.3871, 0.6800), 48: (0.9057, 0.2700),
        49: (0.7229, 0.5100), 50: (0.7700, 0.4500), 51: (0.9671, 0.3000),
        52: (0.2929, 0.2500), 53: (0.5186, 0.3500), 54: (0.5257, 0.1800),
        55: (0.6014, 0.3500), 56: (0.6100, 0.2000), 57: (0.7600, 0.4100),
        58: (0.8300, 0.3800), 59: (0.8943, 0.3900), 60: (0.8671, 0.4700),
        61: (0.8257, 0.6000), 62: (0.7900, 0.3900), 63: (0.7500, 0.6000),
        64: (0.5000, 0.5500), 65: (0.6557, 0.5800), 66: (0.5443, 0.5800),
        67: (0.3486, 0.5800), 68: (0.5143, 0.4900), 69: (0.5171, 0.4000),
        70: (0.7943, 0.3500), 71: (0.7500, 0.2500), 72: (0.6929, 0.1900)
    }

    edges = [
        (9, 53, 1), (53, 10, 1), (53, 8, 1), (8, 7, 1),
        (7, 51, 1), (51, 38, 1), (38, 6, 1), (6, 37, 1),
        (37, 43, 1), (43, 44, 1), (44, 66, 1),
        (66, 39, 1), (39, 5, 1), (5, 4, 1),
        (4, 2, 1), (2, 46, 1), (46, 45, 1),
        (45, 39, 1)
    ]

    for n in positions:
        G.add_node(n)

    for u, v, w in edges:
        if u in G.nodes and v in G.nodes:
            G.add_edge(u, v, weight=w)

    return G, positions

# =================================================================
# II. DIJKSTRA – ĐƯỜNG ĐI NGẮN NHẤT (ĐÃ SỬA)
# =================================================================

def shortest_path(G, start, end):
    """
    Tìm đường đi ngắn nhất bằng Dijkstra
    """
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        length = nx.dijkstra_path_length(G, start, end, weight="weight")
        return path, length
    except nx.NetworkXNoPath:
        return None, None
    except nx.NodeNotFound:
        return None, None

# =================================================================
# III. STREAMLIT UI
# =================================================================

st.set_page_config(layout="wide", page_title="TCV Shortest Path")
st.title("🗺️ Tìm đường đi ngắn nhất trong Thảo Cầm Viên")

G_TCV_base, pos_TCV_base = create_tcv_full_graph_base()
nodes_TCV = sorted(G_TCV_base.nodes)
display_nodes = [f"Node {n}" for n in nodes_TCV]

st.subheader("🔍 Tìm đường đi ngắn nhất")

col1, col2 = st.columns(2)

with col1:
    start_node = int(st.selectbox("Điểm bắt đầu", display_nodes).split(" ")[1])

with col2:
    end_node = int(st.selectbox("Điểm kết thúc", display_nodes, index=1).split(" ")[1])

edges_to_highlight = None

if start_node != end_node:
    path, length = shortest_path(G_TCV_base, start_node, end_node)

    if path:
        st.success(f"Đường đi: {' → '.join(map(str, path))} | Tổng: {length} phút")
        edges_to_highlight = [(path[i], path[i+1]) for i in range(len(path)-1)]
    else:
        st.warning("Không tìm thấy đường đi.")
else:
    st.info("Vui lòng chọn 2 node khác nhau.")

fig = draw_graph_map(
    G_TCV_base,
    pos_TCV_base,
    "thao_cam_vien.jpg",
    edges_to_highlight,
    title="Đường đi ngắn nhất"
)

st.pyplot(fig, use_container_width=True)

