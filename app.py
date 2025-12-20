# =========================
# app.py
# =========================

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
import math
from PIL import Image

from visualize import draw_graph_map

# ======================================================
# I. HÀM TỰ ĐỘNG NỐI NODE BỊ RỜI RẠC
# ======================================================

def connect_disconnected_nodes(G, pos, k=2):
    """
    Nối các node chưa có cạnh với k node gần nhất
    """
    nodes = list(G.nodes)

    for u in nodes:
        if G.degree(u) == 0:
            x1, y1 = pos[u]
            distances = []

            for v in nodes:
                if u == v:
                    continue
                x2, y2 = pos[v]
                dist = math.dist((x1, y1), (x2, y2))
                distances.append((dist, v))

            distances.sort()
            for i in range(k):
                v = distances[i][1]
                G.add_edge(u, v, weight=round(distances[i][0] * 100, 2))

# ======================================================
# II. TẠO ĐỒ THỊ
# ======================================================

@st.cache_data(show_spinner=False)
def create_tcv_full_graph_base():
    G = nx.Graph()

    # ----- TỌA ĐỘ NODE -----
    positions = {
        1:(0.7086,0.5900),2:(0.6071,0.5700),3:(0.4543,0.6900),
        4:(0.5014,0.5515),5:(0.4157,0.6400),6:(0.3614,0.6313),
        7:(0.3929,0.4506),8:(0.3843,0.3000),9:(0.4571,0.2950),
        10:(0.4200,0.1810),11:(0.5457,0.2540),12:(0.6129,0.4520),
        13:(0.6629,0.4320),14:(0.6943,0.4900),15:(0.6457,0.5270),
        16:(0.7329,0.5700),17:(0.7443,0.4300),18:(0.8229,0.4500),
        19:(0.7900,0.5000),20:(0.6243,0.5100),21:(0.6643,0.3500),
        22:(0.7743,0.1800),23:(0.7014,0.3000),24:(0.7557,0.2900),
        25:(0.8600,0.1900),26:(0.7240,0.6500),27:(0.8886,0.2400),
        28:(0.8886,0.2500),29:(0.8714,0.3100),30:(0.8257,0.3500),
        31:(0.6643,0.5400),32:(0.8800,0.3500),33:(0.9586,0.3400),
        34:(0.9414,0.2600),35:(0.8986,0.4900),36:(0.8900,0.5300),
        37:(0.5300,0.4000),38:(0.4557,0.4800),39:(0.3243,0.4500),
        40:(0.3329,0.6300),41:(0.5500,0.4700),42:(0.5743,0.2900),
        43:(0.8014,0.1800),44:(0.4386,0.5500),45:(0.3929,0.5700),
        46:(0.3929,0.6600),47:(0.3871,0.6800),48:(0.9057,0.2700),
        49:(0.7229,0.5100),50:(0.7700,0.4500),51:(0.9671,0.3000),
        52:(0.2929,0.2500),53:(0.5186,0.3500),54:(0.5257,0.1800),
        55:(0.6014,0.3500),56:(0.6100,0.2000),57:(0.7600,0.4100),
        58:(0.8300,0.3800),59:(0.8943,0.3900),60:(0.8671,0.4700),
        61:(0.8257,0.6000),62:(0.7900,0.3900),63:(0.7500,0.6000),
        64:(0.5000,0.5500),65:(0.6557,0.5800),66:(0.5443,0.5800),
        67:(0.3486,0.5800),68:(0.5143,0.4900),69:(0.5171,0.4000),
        70:(0.7943,0.3500),71:(0.7500,0.2500),72:(0.6929,0.1900)
    }

    # ----- ADD NODE -----
    for n in positions:
        G.add_node(n)

    # ----- CẠNH CƠ BẢN (GIỮ ÍT, PHẦN CÒN LẠI TỰ NỐI) -----
    base_edges = [
        (1,2),(2,4),(4,5),(5,6),(6,7),(7,8),(8,9),
        (14,19),(19,30),(30,31),(31,49),(49,15),
        (17,18),(18,50),(50,31)
    ]

    for u,v in base_edges:
        d = math.dist(positions[u], positions[v])
        G.add_edge(u, v, weight=round(d*100,2))

    # ----- TỰ ĐỘNG NỐI NODE BỊ RỜI RẠC -----
    connect_disconnected_nodes(G, positions, k=2)

    return G, positions

# ======================================================
# III. DIJKSTRA
# ======================================================

def shortest_path(G, start, end):
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        length = nx.dijkstra_path_length(G, start, end, weight="weight")
        return path, length
    except:
        return None, None

# ======================================================
# IV. STREAMLIT UI
# ======================================================

st.set_page_config(layout="wide", page_title="TCV Shortest Path")
st.title("🗺️ Tìm đường đi ngắn nhất – Thảo Cầm Viên")

G, pos = create_tcv_full_graph_base()
nodes = sorted(G.nodes)
labels = [f"Node {n}" for n in nodes]

col1, col2 = st.columns(2)
with col1:
    start = int(st.selectbox("Điểm bắt đầu", labels).split()[1])
with col2:
    end = int(st.selectbox("Điểm kết thúc", labels, index=1).split()[1])

edges_highlight = None

if start != end:
    path, length = shortest_path(G, start, end)
    if path:
        st.success(f"Đường đi: {' → '.join(map(str,path))} | Tổng: {length:.1f}")
        edges_highlight = [(path[i], path[i+1]) for i in range(len(path)-1)]
    else:
        st.warning("Không tìm thấy đường đi")

fig = draw_graph_map(
    G,
    pos,
    "thao_cam_vien.jpg",
    edges_highlight,
    title="Shortest Path – TCV"
)

st.pyplot(fig, use_container_width=True)

st.write("🔗 Đồ thị liên thông:", nx.is_connected(G))
