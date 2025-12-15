import numpy as np  
import matplotlib.pyplot as plt 
from scipy.spatial.distance import cdist  
import cv2  
import sys  

# ==========================================
# PHẦN 1: HÀM HỖ TRỢ XỬ LÝ ẢNH (KỸ THUẬT)
# ==========================================
def fig_to_cv2_image(fig):
    """
    Hàm này biến đổi biểu đồ Matplotlib (vector) thành ảnh bitmap (pixel)
    để OpenCV có thể hiển thị được.
    """
    # 1. Vẽ biểu đồ lên bộ nhớ đệm (RAM)
    fig.canvas.draw()
    
    # 2. Lấy kích thước ảnh (rộng, cao)
    w, h = fig.canvas.get_width_height()
    
    # 3. Lấy dữ liệu pixel từ buffer (dạng RGBA - Red Green Blue Alpha)
    buffer = fig.canvas.buffer_rgba()
    
    # 4. Chuyển buffer thành mảng số học (numpy array)
    data = np.frombuffer(buffer, dtype=np.uint8)
    data = data.reshape((int(h), int(w), 4)) # Định hình lại thành ma trận ảnh
    
    # 5. Chuyển hệ màu từ RGB (của Matplotlib) sang BGR (của OpenCV)
    # Nếu không có dòng này, màu đỏ sẽ biến thành màu xanh dương
    img_bgr = cv2.cvtColor(data, cv2.COLOR_RGBA2BGR)
    
    return img_bgr

# ==========================================
# PHẦN 2: CÁC HÀM TÍNH TOÁN K-MEANS (TOÁN HỌC)
# ==========================================
def kmeans_init_centers(X, n_cluster):
    """
    Bước khởi tạo: Chọn ngẫu nhiên n_cluster điểm từ dữ liệu X làm tâm ban đầu.
    replace=False: Đảm bảo không chọn trùng.
    """
    return X[np.random.choice(X.shape[0], n_cluster, replace=False)]

def kmeans_predict_labels(X, centers):
    """
    Bước E-Step (Expectation): Gán nhãn cho điểm dữ liệu.
    Mỗi điểm sẽ được gán vào tâm cụm nào gần nó nhất.
    """
    # Tính khoảng cách từ mọi điểm đến mọi tâm
    D = cdist(X, centers) 
    # Trả về chỉ số (index) của tâm có khoảng cách nhỏ nhất
    return np.argmin(D, axis=1)

def kmeans_update_centers(X, labels, n_cluster):
    """
    Bước M-Step (Maximization): Cập nhật vị trí tâm.
    Tâm mới = Trung bình cộng toạ độ của tất cả các điểm thuộc cụm đó.
    """
    centers = np.zeros((n_cluster, X.shape[1]))
    for k in range(n_cluster):
        # Lấy tất cả các điểm thuộc cụm k
        Xk = X[labels == k, :]
        
        # Nếu cụm không rỗng thì tính trung bình
        if len(Xk) > 0:
            centers[k,:] = np.mean(Xk, axis=0)
    return centers

def kmeans_has_converged(centers, new_centers):
    """
    Kiểm tra hội tụ: So sánh tập hợp tâm cũ và tâm mới.
    Nếu giống hệt nhau -> Thuật toán dừng.
    """
    return (set([tuple(a) for a in centers]) == set([tuple(a) for a in new_centers]))

# ==========================================
# PHẦN 3: CÁC HÀM HIỂN THỊ (VISUALIZATION)
# ==========================================

# Hàm 1: Vẽ các bước trung gian (1 biểu đồ)
def kmeans_visualize_step(X, centers, labels, n_cluster, title):
    fig = plt.figure(figsize=(10, 8))
    plt.xlabel('x'); plt.ylabel('y')
    plt.title(title)
    
    base_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
    
    for i in range(n_cluster):
        color = base_colors[i % len(base_colors)]
        data = X[labels == i]
        # Vẽ điểm dữ liệu (tam giác)
        plt.plot(data[:, 0], data[:, 1], color=color, marker='^', linestyle='', markersize=4, alpha=0.4)
        # Vẽ tâm cụm (hình tròn to)
        if centers is not None:
            plt.plot(centers[i][0], centers[i][1], color=color, marker='o', markersize=15, markeredgecolor='black', markeredgewidth=2)
    
    # Chuyển sang ảnh OpenCV và hiển thị
    img_cv2 = fig_to_cv2_image(fig)
    plt.close(fig) # Giải phóng RAM
    
    cv2.imshow('Mo phong K-Means', img_cv2)
    print(f">> Bước hiện tại: {title}")
    
    # Đợi bấm phím
    key = cv2.waitKey(0)
    if key == ord('q'): sys.exit()

# Hàm 2: Vẽ SO SÁNH TRƯỚC - SAU (2 biểu đồ cạnh nhau)
def visualize_comparison(X, final_centers, final_labels, n_cluster, times):
    # Tạo khung chứa 2 biểu đồ (1 hàng, 2 cột)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # --- BIỂU ĐỒ 1: Dữ liệu thô (Bên trái) ---
    ax1.set_title("DỮ LIỆU BAN ĐẦU (Input)")
    ax1.set_xlabel('x'); ax1.set_ylabel('y')
    # Vẽ màu xám (gray) để thể hiện chưa phân cụm
    ax1.plot(X[:, 0], X[:, 1], color='gray', marker='^', linestyle='', markersize=4, alpha=0.5)

    # --- BIỂU ĐỒ 2: Kết quả phân cụm (Bên phải) ---
    ax2.set_title(f"KẾT QUẢ PHÂN CỤM (Hội tụ sau {times} bước)")
    ax2.set_xlabel('x'); ax2.set_ylabel('y')
    
    base_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
    for i in range(n_cluster):
        color = base_colors[i % len(base_colors)]
        data = X[final_labels == i]
        # Vẽ điểm
        ax2.plot(data[:, 0], data[:, 1], color=color, marker='^', linestyle='', markersize=4, alpha=0.4)
        # Vẽ tâm
        ax2.plot(final_centers[i][0], final_centers[i][1], color=color, marker='o', markersize=15, markeredgecolor='black', markeredgewidth=2)

    # Hiển thị
    img_cv2 = fig_to_cv2_image(fig)
    plt.close(fig)
    
    cv2.imshow('Mo phong K-Means', img_cv2)
    print(f"\n>> Đã hiển thị bảng so sánh tổng kết. Bấm phím bất kỳ để kết thúc.")
    cv2.waitKey(0)

# ==========================================
# PHẦN 4: LOGIC ĐIỀU KHIỂN CHÍNH
# ==========================================
def kmeans_run(X, n_cluster):
    print("\n--- BẮT ĐẦU THUẬT TOÁN ---")
    
    # B1: Khởi tạo
    init_centers = kmeans_init_centers(X, n_cluster)
    init_labels = np.zeros(X.shape[0]) 
    
    # Vẽ bước 0
    kmeans_visualize_step(X, init_centers, init_labels, n_cluster, 'Khoi tao: Random vi tri tam')

    centers = init_centers
    labels = init_labels
    times = 0
    
    while True:
        # B2: Tìm nhãn mới (E-step)
        labels = kmeans_predict_labels(X, centers)
        kmeans_visualize_step(X, centers, labels, n_cluster, f'Vong lap {times+1}: Gan nhan (Tim tam gan nhat)')
        
        # B3: Tính tâm mới (M-step)
        new_centers = kmeans_update_centers(X, labels, n_cluster)
        
        # B4: Kiểm tra dừng
        if kmeans_has_converged(centers, new_centers):
            # Nếu đã hội tụ, gọi hàm vẽ SO SÁNH TRƯỚC SAU
            visualize_comparison(X, new_centers, labels, n_cluster, times+1)
            break
        
        centers = new_centers
        kmeans_visualize_step(X, centers, labels, n_cluster, f'Vong lap {times+1}: Cap nhat lai vi tri tam')
        times += 1
    
    return times

# ==========================================
# PHẦN 5: CHƯƠNG TRÌNH CHÍNH (MAIN)
# ==========================================
if __name__ == "__main__":
    print("=== DEMO K-MEANS: SO SÁNH TRƯỚC VÀ SAU ===")
    
    # 1. Nhập liệu từ bàn phím
    try:
        n_cluster_input = int(input("1. Nhập số lượng cụm (k): "))
        n_samples_input = int(input("2. Nhập tổng số điểm dữ liệu (N): "))
    except ValueError:
        print("Lỗi: Nhập sai định dạng số!"); sys.exit()

    # 2. Sinh dữ liệu giả lập (Dummy Data Generation)
    print(f">> Đang sinh dữ liệu ngẫu nhiên...")
    true_centers = np.random.randint(0, 20, (n_cluster_input, 2)) # Tâm giả để sinh dữ liệu
    cov = [[1.5, 0], [0, 1.5]] # Độ phân tán
    
    X_list = []
    samples_per_cluster = n_samples_input // n_cluster_input
    
    # Tạo các đám mây điểm quanh tâm giả
    for i in range(n_cluster_input):
        data = np.random.multivariate_normal(true_centers[i], cov, samples_per_cluster)
        X_list.append(data)
    
    # Xử lý phần dư (nếu chia không hết)
    if n_samples_input % n_cluster_input != 0:
        data = np.random.multivariate_normal(true_centers[-1], cov, n_samples_input % n_cluster_input)
        X_list.append(data)

    X = np.concatenate(X_list, axis=0) # Gộp thành 1 tập dữ liệu lớn

    # 3. Chạy thuật toán
    kmeans_run(X, n_cluster_input)
    
    # 4. Kết thúc
    cv2.destroyAllWindows()
    print("Chương trình kết thúc thành công!")