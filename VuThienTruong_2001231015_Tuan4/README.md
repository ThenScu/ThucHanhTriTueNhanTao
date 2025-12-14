Giải thuật tô màu đồ thị
1. Dữ liệu đầu vào: Một đồ thị với các đỉnh và bậc tương ứng.
<img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/88396c63-925e-416d-9165-3091072be305" />

   Quy trình thuật toán:
   - Bước 1 (Sắp xếp): Sắp xếp danh sách các đỉnh theo thứ tự bậc từ cao xuống thấp.
   - Bước 2 (Tô màu): Chọn đỉnh có bậc cao nhất chưa được tô (ví dụ: Đỉnh 3). Tô màu cho nó.
   - Bước 3 (Xét láng giềng): Tìm các đỉnh không liền kề với đỉnh vừa tô trong danh sách còn lại (ví dụ: Đỉnh 5) và tô cùng màu đó.
   - Bước 4 (Hạ bậc/Cập nhật): Đánh dấu các đỉnh đã tô màu là "đã xử lý" (hoặc gán bậc bằng 0).
   - Bước 5: Lặp lại quy trình với màu tiếp theo cho các đỉnh còn lại.

   Dữ liệu ví dụ (Trace log):
   - Ban đầu (Sắp xếp giảm dần): 
     + Đỉnh 3: Bậc 4
     + Đỉnh 1: Bậc 3
     + Đỉnh 2: Bậc 3
     + Đỉnh 4: Bậc 3
     + Đỉnh 6: Bậc 2
     + Đỉnh 5: Bậc 1
   - Xử lý Lượt 1 (Màu Đỏ):
     + Chọn Đỉnh 3 (Bậc cao nhất).
     + Xét thấy Đỉnh 5 không kề Đỉnh 3 -> Tô Đỉnh 5 màu Đỏ.
  <img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/6a253228-76ab-4f8c-9b08-6ba9de7559e6" />

     
   - Cập nhật sau Lượt 1:
     + Đỉnh 3 -> Bậc 0 (Đã xong)
     + Đỉnh 5 -> Bậc 0 (Đã xong)
     + Các đỉnh còn lại giữ nguyên hoặc giảm bậc tùy theo liên kết (như bảng dữ liệu mẫu: Đỉnh 1, 2, 4 còn bậc 2; Đỉnh 6 còn bậc 1).
       
2. Dữ liệu đầu vào:
- Bảng cập nhật trạng thái các đỉnh (Sau khi đã xong đỉnh 3 và 5 ở bước 1):
  + Đỉnh 3, 5: Bậc 0 (Đã xong).
  + Đỉnh 1, 2, 4: Bậc 2.
  + Đỉnh 6: Bậc 1.

Hành động trong Bước 2 (Màu Xanh Lá):
1. Chọn đỉnh tiếp theo trong nhóm bậc cao nhất: Chọn Đỉnh 1 -> Tô màu Xanh Lá.
2. Xét các đỉnh còn lại: Thấy Đỉnh 4 không kề với Đỉnh 1.
3. Kết luận: Tô Đỉnh 4 màu Xanh Lá.
<img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/ad673dd0-e359-4a9d-8057-7c881e8ff068" />


3. Dữ liệu đầu vào:
- Bảng cập nhật trạng thái (Sau khi xong đỉnh 1 và 4):
  + Đỉnh 3, 5, 1, 4: Bậc 0 (Đã xong).
  + Đỉnh 2, 6: Bậc 1 (Bậc giảm do các đỉnh kề đã bị loại bỏ).

Hành động trong Bước 3 (Màu Xanh Dương):
1. Chọn đỉnh có bậc cao nhất còn lại: Chọn Đỉnh 2 -> Tô màu Xanh Dương.
2. Xét đỉnh còn lại (Đỉnh 6):
   - Kiểm tra quan hệ: Đỉnh 6 CÓ kề với Đỉnh 2 (dựa trên đồ thị gốc).
   - Kết luận: Không thể tô Đỉnh 6 màu Xanh Dương. Đỉnh 6 sẽ được xử lý ở lượt sau.

<img width="500" height="450" alt="image" src="https://github.com/user-attachments/assets/a3c1f625-d88a-467f-9d52-38b30f0126be"/>


