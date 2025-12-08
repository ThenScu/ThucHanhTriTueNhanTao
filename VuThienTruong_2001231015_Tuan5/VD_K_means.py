# Bước 1: Import các thư viện cần thiết
import numpy as np # thư viện tính toán toán học
import matplotlib.pyplot as plt # visualize data sử dụng đồ thị
from scipy.spatial.distance import cdist # Hỗ trợ tính khoảng cách

# Bước 2: Khởi tạo 500 điểm dữ liệu xung quanh 3 tâm cụm
means = [[2, 2], [9, 2], [4, 9]]
cov = [[2, 0], [0, 2]]
n_samples = 500
n_cluster = 3

X0 = np.random.multivariate_normal(means[0], cov, n_samples)
X1 = np.random.multivariate_normal(means[1], cov, n_samples)
X2 = np.random.multivariate_normal(means[2], cov, n_samples)
X = np.concatenate((X0, X1, X2), axis = 0)

# Bước 3: Xem phân bố của dữ liệu vừa tạo
plt.figure(figsize=(8, 6))
plt.xlabel('x')
plt.ylabel('y')
plt.plot(X[:, 0], X[:, 1], 'bo', markersize=5, alpha=0.5)
plt.title('Dữ liệu ban đầu')
plt.show()

# --- CÁC HÀM HỖ TRỢ K-MEANS ---

# Bước 4: Hàm khởi tạo tâm cụm ban đầu
def kmeans_init_centers(X, n_cluster):
    # random k index between 0 and shape(X) without duplicate index.
    # Then return X[index] as cluster
    return X[np.random.choice(X.shape[0], n_cluster, replace=False)]

# Bước 5: Hàm xác định nhãn (label) cho từng điểm dữ liệu dựa trên tâm cụm
def kmeans_predict_labels(X, centers):
    D = cdist(X, centers)
    # return index of the closest center
    return np.argmin(D, axis = 1)

# Bước 6: Hàm cập nhật lại vị trí các tâm cụm
def kmeans_update_centers(X, labels, n_cluster):
    centers = np.zeros((n_cluster, X.shape[1]))
    for k in range(n_cluster):
        # collect all points assigned to the k-th cluster
        Xk = X[labels == k, :]
        # take average
        centers[k,:] = np.mean(Xk, axis = 0)
    return centers

# Bước 7: Hàm kiểm tra tính hội tụ
def kmeans_has_converged(centers, new_centers):
    # return True if two sets of centers are the same
    return (set([tuple(a) for a in centers]) == set([tuple(a) for a in new_centers]))

# Bước 8: Hàm vẽ đồ thị để quan sát quá trình
def kmeans_visualize(X, centers, labels, n_cluster, title):
    plt.figure(figsize=(8, 6))
    plt.xlabel('x') 
    plt.ylabel('y') 
    plt.title(title) 
    
    # Danh sách màu hỗ trợ
    plt_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'] 
    
    for i in range(n_cluster):
        data = X[labels == i] # lấy dữ liệu của cụm i
        # Vẽ các điểm thuộc cụm i
        plt.plot(data[:, 0], data[:, 1], plt_colors[i] + '^', markersize=4, label='cluster_' + str(i), alpha=0.5) 
        # Vẽ tâm cụm i (dùng màu khác để nổi bật, offset index màu đi 4 đơn vị)
        plt.plot(centers[i][0], centers[i][1], plt_colors[i + 4] + 'o', markersize=10, label='center_' + str(i)) 
    
    plt.legend() 
    plt.show()

# Bước 9: Toàn bộ thuật toán K-means
def kmeans(init_centers, init_labels, X, n_cluster):
    centers = init_centers
    labels = init_labels
    times = 0
    
    while True:
        # Bước tìm nhãn mới
        labels = kmeans_predict_labels(X, centers)
        
        # Vẽ đồ thị sau khi gán nhãn
        kmeans_visualize(X, centers, labels, n_cluster, 'Assigned label for data at time = ' + str(times + 1))
        
        # Bước cập nhật tâm cụm
        new_centers = kmeans_update_centers(X, labels, n_cluster)
        
        # Kiểm tra hội tụ
        if kmeans_has_converged(centers, new_centers):
            break
        
        centers = new_centers
        
        # Vẽ đồ thị sau khi cập nhật tâm
        kmeans_visualize(X, centers, labels, n_cluster, 'Update center position at time = ' + str(times + 1))
        times += 1
        
    return (centers, labels, times)

# Bước 10: Gọi hàm để thực thi
print("Bắt đầu thuật toán K-Means...")

# Khởi tạo
init_centers = kmeans_init_centers(X, n_cluster)
print("Tâm khởi tạo ban đầu:\n", init_centers) 

init_labels = np.zeros(X.shape[0])

# Vẽ trạng thái khởi tạo
kmeans_visualize(X, init_centers, init_labels, n_cluster, 'Init centers in the first run. Assigned all data as cluster 0')

# Chạy vòng lặp K-means
centers, labels, times = kmeans(init_centers, init_labels, X, n_cluster)

print('Done! Kmeans has converged after', times, 'times')
print('Final centers:\n', centers)