import networkx as nx  
import matplotlib.pyplot as plt  #
import sys  
import random  

# ==========================================
# 1. HÀM VẼ ĐỒ THỊ (Dùng chung cho cả lúc chưa tô và đã tô)
# ==========================================
def ve_do_thi(G_matrix, node_labels, colors_mapping=None, title=""):
    """
    Hàm này chịu trách nhiệm hiển thị đồ thị lên màn hình.
    - G_matrix: Ma trận chứa thông tin các kết nối.
    - colors_mapping: Kết quả màu đã tô (nếu None thì vẽ màu xám).
    """
    # Khởi tạo một đối tượng đồ thị rỗng
    G_viz = nx.Graph()
    n = len(node_labels)
    
    # Thêm danh sách các đỉnh vào đồ thị
    G_viz.add_nodes_from(node_labels)
    
    # Duyệt ma trận kề để thêm các cạnh nối (Edges)
    for i in range(n):
        for j in range(i + 1, n): # Chỉ duyệt nửa trên ma trận để tránh trùng lặp
            if G_matrix[i][j] == 1:
                G_viz.add_edge(node_labels[i], node_labels[j])

    # Thiết lập kích thước khung hình vẽ (Dài x Rộng)
    plt.figure(figsize=(10, 7))
    
    # seed=42 giúp thuật toán sắp xếp vị trí các đỉnh luôn giống nhau ở mọi lần vẽ.
    # Điều này giúp hình "Trước" và "Sau" khi tô màu không bị nhảy vị trí lung tung.
    pos = nx.spring_layout(G_viz, seed=42) 

    # Xác định màu sắc cho từng đỉnh
    if colors_mapping is None:
        # Nếu chưa có bảng màu (Lúc mới nhập xong) -> Tô tất cả màu xám nhạt
        node_colors = ['lightgray'] * n
    else:
        # Nếu đã có kết quả -> Lấy màu tương ứng cho từng đỉnh
        node_colors = [colors_mapping[node] for node in G_viz.nodes()]

    # Vẽ đồ thị thực sự
    nx.draw(G_viz, pos, 
            with_labels=True,  # Hiển thị tên đỉnh (A, B, C...)
            node_color=node_colors, # Gán màu
            node_size=800,  # Kích thước chấm tròn
            edge_color='gray', # Màu dây nối
            font_weight='bold', # Chữ in đậm
            font_color='black')
    
    plt.title(title) # Đặt tiêu đề cho cửa sổ
    print(f">> Đang hiển thị cửa sổ: {title}")
    print("   (LƯU Ý: Vui lòng ĐÓNG cửa sổ hình ảnh để chương trình chạy tiếp...)")
    plt.show() # Lệnh này sẽ tạm dừng chương trình cho đến khi tắt ảnh

# ==========================================
# 2. LOGIC TÔ MÀU (Thuật toán tham lam / Welsh-Powell)
# ==========================================
def thuat_toan_to_mau(G, node_names):
    """
    Đây là bộ não của chương trình.
    Sử dụng giải thuật tham lam: Ưu tiên tô màu đỉnh có bậc cao nhất trước.
    """
    # B1: Tính bậc (Degree) cho từng đỉnh (Số lượng kết nối)
    degree = [sum(row) for row in G]
    
    # Kho màu dự trữ (đủ dùng cho hầu hết đồ thị cơ bản)
    available_colors_pool = ["red", "green", "blue", "yellow", "cyan", "magenta", "orange", "purple", "pink", "brown"]
    
    # Tạo danh sách màu khả dụng riêng cho từng đỉnh ban đầu (đỉnh nào cũng có thể chọn full màu)
    color_dict = {node: available_colors_pool.copy() for node in node_names}
    
    # B2: Sắp xếp các đỉnh theo thứ tự Bậc Giảm Dần
    # (Đỉnh nào nhiều kết nối nhất thì xử lý trước -> Đây là mấu chốt để tối ưu)
    sorted_indices = sorted(range(len(degree)), key=lambda k: degree[k], reverse=True)
    sorted_nodes = [node_names[i] for i in sorted_indices]
    
    result = {} # Biến lưu kết quả cuối cùng
    
    # Tạo từ điển ánh xạ tên đỉnh sang vị trí index (Ví dụ: 'A' -> 0) để dễ truy xuất ma trận
    t_ = {node_names[i]: i for i in range(len(G))}
    
    # B3: Duyệt qua từng đỉnh đã sắp xếp và chọn màu
    for n in sorted_nodes:
        # Nếu đỉnh này không còn màu nào để chọn (hiếm gặp)
        if not color_dict[n]:
            result[n] = 'white' 
            continue
            
        # Chọn màu đầu tiên trong danh sách khả dụng của nó
        chosen_color = color_dict[n][0]
        result[n] = chosen_color # Gán màu
        
        # --- QUAN TRỌNG: CẬP NHẬT HÀNG XÓM ---
        # Sau khi đỉnh n chọn màu X, phải đi báo cho tất cả hàng xóm biết:
        # "Đỉnh n chọn màu X rồi, tụi bây bỏ X ra khỏi danh sách nhé!"
        idx = t_[n] # Lấy index của đỉnh n
        for neighbor_idx, linked in enumerate(G[idx]):
            if linked == 1: # Nếu có nối cạnh
                neighbor_name = node_names[neighbor_idx]
                # Nếu màu vừa chọn nằm trong danh sách của hàng xóm -> Xóa nó đi
                if chosen_color in color_dict[neighbor_name]:
                    color_dict[neighbor_name].remove(chosen_color)
                    
    return result

# ==========================================
# 3. CHƯƠNG TRÌNH CHÍNH (MAIN FLOW)
# ==========================================
if __name__ == "__main__":
    print("=== TÔ MÀU ĐỒ THỊ (RANDOM + TRỰC QUAN) ===")
    
    # --- BƯỚC 1: NHẬP SỐ ĐỈNH ---
    try:
        n = int(input("1. Nhập số lượng đỉnh (VD: 8): "))
    except:
        print("Lỗi: Phải nhập số nguyên!"); sys.exit()
        
    # Tạo tên đỉnh tự động: A, B, C... hoặc 0, 1, 2... nếu quá nhiều
    node_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:n]
    if n > 26: node_names = [str(i) for i in range(n)]
    
    # Khởi tạo ma trận kề toàn số 0 (chưa có kết nối nào)
    G = [[0]*n for _ in range(n)]

    # --- BƯỚC 2: LỰA CHỌN CÁCH TẠO CẠNH ---
    print("\nBạn muốn tạo cạnh kết nối kiểu nào?")
    print("   [1] Tự nhập tay (Thủ công - Dùng để test bài nhỏ)")
    print("   [2] Tự sinh ngẫu nhiên (Random - Dùng để test bài lớn)")
    choice = input(">> Lựa chọn của bạn (1 hoặc 2): ")

    if choice == '2':
        # --- CHẾ ĐỘ RANDOM (TỰ ĐỘNG) ---
        ty_le = 0.4 # Xác suất 40%
        print(f"\n[INFO] Đang sinh ngẫu nhiên với tỷ lệ kết nối {ty_le*100}%...")
        
        # Duyệt qua từng cặp đỉnh
        for i in range(n):
            for j in range(i + 1, n):
                # random.random() sinh số thực từ 0.0 đến 1.0
                # Nếu số sinh ra < 0.4 thì ta nối cạnh (Gán = 1)
                if random.random() < ty_le:
                    G[i][j] = G[j][i] = 1 
    else:
        # --- CHẾ ĐỘ NHẬP TAY (THỦ CÔNG) ---
        print("\nNhập các cạnh (VD: 0 1 nghĩa là nối đỉnh 0 với 1).")
        print("Nhập chữ 'q' để hoàn tất.")
        while True:
            s = input("   Nối (u v): ")
            if s == 'q': break
            try:
                # Tách chuỗi nhập vào thành 2 số nguyên
                u, v = map(int, s.split())
                if 0 <= u < n and 0 <= v < n:
                    G[u][v] = G[v][u] = 1 # Nối 2 chiều vì là đồ thị vô hướng
                else:
                    print(f"   Lỗi: Chỉ số phải từ 0 đến {n-1}")
            except: 
                print("   Lỗi định dạng! Hãy nhập: số số (VD: 0 1)")
                continue

    # --- BƯỚC 3: VẼ ĐỒ THỊ BAN ĐẦU (CHƯA TÔ) ---
    print("\n[INFO] Đang vẽ đồ thị thô (Màu xám)...")
    # Gọi hàm vẽ với colors_mapping=None để hiện màu xám
    ve_do_thi(G, node_names, colors_mapping=None, title="Do thi ban dau (Chua to mau)")
    
    # --- BƯỚC 4: CHẠY THUẬT TOÁN TÍNH TOÁN ---
    print("\n[INFO] Đang tính toán tô màu...")
    ket_qua_to_mau = thuat_toan_to_mau(G, node_names)
    
    # In kết quả ra màn hình console
    print("-> Kết quả phân màu chi tiết:")
    for k, v in ket_qua_to_mau.items():
        print(f"  Đỉnh {k}: {v}")
        
    # --- BƯỚC 5: VẼ ĐỒ THỊ KẾT QUẢ (ĐÃ TÔ) ---
    print("\n[INFO] Đang vẽ đồ thị kết quả...")
    # Gọi hàm vẽ lần 2, truyền kết quả màu vào để hiển thị
    ve_do_thi(G, node_names, colors_mapping=ket_qua_to_mau, title="Ket qua sau khi to mau")