# File: visualize.py (Phiên bản Đầy đủ, đã bao gồm create_mock_tcv_graph_image)

import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import os
import io

# --- ĐỊNH NGHĨA KÍCH THƯỚC VẼ NODE ---
NODE_SIZE_MAP = 100 # Kích thước node trên bản đồ (đã giảm)
NODE_SIZE_MOCK = 500 # Kích thước node khi vẽ đồ thị mô phỏng

def draw_graph_map(G, pos, image_path, edges_to_highlight=None, title="Đường đi Ngắn nhất trên Bản đồ", x_lim=(0, 1), y_lim=(0, 1)):
    """
    Vẽ đồ thị NetworkX lên một ảnh nền bản đồ (map image) với tùy chỉnh giới hạn trục (zoom).
    """
    
    # 1. Khởi tạo Figure và Axes
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(title, fontsize=16)

    try:
        # 2. Tải và hiển thị ảnh nền
        img = Image.open(os.path.join("assets", image_path))
        ax.imshow(img, extent=[0, 1, 0, 1]) # Đặt ảnh nền trong phạm vi 0-1
        
        # Ẩn trục tọa độ
        ax.axis('off')

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh nền '{image_path}'. Vui lòng kiểm tra thư mục 'assets'.")
        # Thiết lập nền trắng nếu không tìm thấy ảnh
        ax.set_facecolor('white')


    # 3. Chuẩn bị các thành phần đồ thị
    all_edges = list(G.edges())
    
    if edges_to_highlight:
        normal_edges = [edge for edge in all_edges if tuple(sorted(edge)) not in [tuple(sorted(e)) for e in edges_to_highlight]]
    else:
        normal_edges = all_edges
    
    edge_weights = nx.get_edge_attributes(G, 'weight')


    # 4. Vẽ đồ thị
    
    # A. Vẽ các nodes (điểm)
    nx.draw_networkx_nodes(G, pos, 
                           node_size=NODE_SIZE_MAP, 
                           node_color='red', 
                           alpha=0.8, 
                           ax=ax)

    # B. Vẽ các cạnh thường
    nx.draw_networkx_edges(G, pos, 
                           edgelist=normal_edges, 
                           edge_color='gray', 
                           style='--', 
                           alpha=0.5, 
                           width=1, 
                           ax=ax)
    
    # C. Highlight đường đi ngắn nhất
    if edges_to_highlight:
        nx.draw_networkx_edges(G, pos, 
                               edgelist=edges_to_highlight, 
                               edge_color='blue', 
                               style='solid', 
                               width=2.5, 
                               ax=ax)

        # D. Lấy các trọng số của cạnh được highlight để hiển thị
        highlight_weights = {
            (u, v): edge_weights[(u, v)] 
            for u, v in edges_to_highlight if (u, v) in edge_weights
        }
        
        # E. Vẽ labels (trọng số) lên đường đi ngắn nhất
        nx.draw_networkx_edge_labels(G, pos, 
                                     edge_labels=highlight_weights, 
                                     font_color='black', 
                                     font_size=10,
                                     bbox={"boxstyle": "round", "fc": "yellow", "alpha": 0.5},
                                     ax=ax)

    # F. Vẽ labels cho nodes (chỉ hiển thị số thứ tự)
    node_labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, 
                            labels=node_labels, 
                            font_size=10, 
                            font_color='black', 
                            ax=ax)

    # 5. Áp dụng giới hạn trục để tạo hiệu ứng Zoom/Pan
    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylim(y_lim[0], y_lim[1])
    
    return fig


def create_mock_tcv_graph_image(G, pos, temp_path="assets/temp_mock_path.png"):
    """
    Tạo một biểu đồ NetworkX mô phỏng nếu không có ảnh nền.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("Đồ thị MÔ PHỎNG (Thiếu ảnh nền)")
    
    # Vẽ nodes và edges
    nx.draw(G, pos, 
            with_labels=True, 
            node_size=NODE_SIZE_MOCK, # Kích thước node lớn hơn cho mô phỏng
            node_color='lightblue', 
            font_size=12, 
            edge_color='gray', 
            width=1.5, 
            ax=ax)
            
    # Lưu hình ảnh vào bộ đệm và trả về đường dẫn tạm thời
    try:
        if not os.path.exists(os.path.dirname(temp_path)):
            os.makedirs(os.path.dirname(temp_path))
        fig.savefig(temp_path, format="png")
        plt.close(fig)
        return temp_path
    except Exception as e:
        print(f"Lỗi khi lưu ảnh mô phỏng: {e}")
        return None