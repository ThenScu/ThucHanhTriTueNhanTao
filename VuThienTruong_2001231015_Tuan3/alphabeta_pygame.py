import sys
import pygame
import math
import random

# =============================================================================
# PHẦN 1: CÁC HÀM XỬ LÝ LOGIC GAME (CORE ALGORITHMS)
# =============================================================================

def create_board(n):
    """
    Tạo bàn cờ kích thước n*n dưới dạng danh sách (mảng 1 chiều).
    Giá trị ban đầu là các số từ 1 đến n*n.
    """
    return [i for i in range(1, n * n + 1)]

def check_winner_n(board, n, win_len):
    """
    [THUẬT TOÁN VÉT CẠN - BRUTE FORCE]
    Kiểm tra xem đã có ai thắng chưa trên bàn cờ kích thước n.
    Độ phức tạp: O(n^2)
    """
    # Hàm con để lấy giá trị tại hàng r, cột c từ mảng 1 chiều
    def at(r, c):
        return board[r * n + c]

    # Định nghĩa 4 hướng kiểm tra: Ngang, Dọc, Chéo chính, Chéo phụ
    # 
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # Duyệt qua từng ô trên bàn cờ
    for r in range(n):
        for c in range(n):
            player = at(r, c)
            # Chỉ kiểm tra nếu ô đó đã được đánh (là X hoặc O)
            if player != 'X' and player != 'O':
                continue

            # Tại mỗi ô, kiểm tra loang ra theo 4 hướng
            for dr, dc in directions:
                cnt = 1 # Đếm số quân liên tiếp (bắt đầu là 1 vì tính cả ô hiện tại)
                rr, cc = r + dr, c + dc
                
                # Vòng lặp kiểm tra các ô kế tiếp theo hướng (dr, dc)
                while 0 <= rr < n and 0 <= cc < n and at(rr, cc) == player:
                    cnt += 1
                    if cnt >= win_len: # Nếu đủ số lượng thắng -> Return ngay
                        return player
                    rr += dr
                    cc += dc
    return None

def get_available_cells(board):
    """Lấy danh sách các chỉ số (index) của các ô còn trống."""
    return [i for i, x in enumerate(board) if x != 'X' and x != 'O']

# =============================================================================
# PHẦN 2: TRÍ TUỆ NHÂN TẠO (AI ALGORITHMS)
# =============================================================================

def find_best_move_simple(board, n, ai_symbol):
    """
    [THUẬT TOÁN THAM LAM - GREEDY / HEURISTIC]
    Dùng cho chế độ chơi thực tế (nhanh, hiệu quả cho bàn cờ lớn).
    Thứ tự ưu tiên:
    1. Thắng ngay lập tức.
    2. Chặn đối thủ thắng.
    3. Chiếm ô trung tâm.
    4. Đánh ngẫu nhiên.
    """
    opponent = 'O' if ai_symbol == 'X' else 'X'
    available_moves = get_available_cells(board)

    # Nếu không còn nước đi
    if not available_moves:
        return None

    # --- Ưu tiên 1: TẤN CÔNG (Tìm nước đi để thắng) ---
    for move in available_moves:
        board[move] = ai_symbol      # Thử đánh
        if check_winner_n(board, n, n) == ai_symbol:
            board[move] = move + 1   # Backtrack (hoàn tác)
            return move              # Chốt đơn
        board[move] = move + 1       # Backtrack

    # --- Ưu tiên 2: PHÒNG THỦ (Chặn đối thủ) ---
    for move in available_moves:
        board[move] = opponent       # Giả vờ mình là đối thủ đánh
        if check_winner_n(board, n, n) == opponent:
            board[move] = move + 1   # Backtrack
            return move              # Chặn ngay
        board[move] = move + 1       # Backtrack

    # --- Ưu tiên 3: CHIẾM TRUNG TÂM ---
    center = (n * n) // 2
    if center in available_moves:
        return center

    # --- Ưu tiên 4: NGẪU NHIÊN ---
    return random.choice(available_moves)

# -----------------------------------------------------------------------------
# [LÝ THUYẾT] THUẬT TOÁN MINIMAX 
# -----------------------------------------------------------------------------
def minimax(position, depth, alpha, beta, isMaximizing, n):
    """
    [THUẬT TOÁN ĐỆ QUY + QUAY LUI + CẮT TỈA ALPHA-BETA]
    Tìm nước đi tối ưu tuyệt đối. 
    Lưu ý: Chỉ dùng tham khảo logic vì chạy rất chậm với n > 3.
    
    """
    winner = check_winner_n(position, n, n)
    # Điều kiện dừng (Base case)
    if winner == 'X': return 10 - depth
    if winner == 'O': return -10 + depth
    avail = get_available_cells(position)
    if not avail: return 0 # Hòa

    if isMaximizing: # Lượt của MAX (thường là X)
        maxEval = -math.inf
        for cell_idx in avail:
            original_val = position[cell_idx]
            position[cell_idx] = 'X' # Đi thử
            
            # Đệ quy
            eval_score = minimax(position, depth + 1, alpha, beta, False, n)
            
            position[cell_idx] = original_val # Quay lui (Backtrack)
            
            maxEval = max(maxEval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha: break # Cắt tỉa Alpha-Beta
        return maxEval
    else: # Lượt của MIN (thường là O)
        minEval = math.inf
        for cell_idx in avail:
            original_val = position[cell_idx]
            position[cell_idx] = 'O' # Đi thử
            
            eval_score = minimax(position, depth + 1, alpha, beta, True, n)
            
            position[cell_idx] = original_val # Quay lui
            
            minEval = min(minEval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha: break # Cắt tỉa Alpha-Beta
        return minEval

# =============================================================================
# PHẦN 3: GIAO DIỆN ĐỒ HỌA (PYGAME UI)
# =============================================================================

def draw_grid(surface, n, cell_size, line_color=(50, 50, 50)):
    """Vẽ lưới bàn cờ."""
    w, h = surface.get_size()
    for i in range(1, n):
        # Vẽ dây dọc
        pygame.draw.line(surface, line_color, (i*cell_size, 0), (i*cell_size, h), 2)
        # Vẽ dây ngang
        pygame.draw.line(surface, line_color, (0, i*cell_size), (w, i*cell_size), 2)

def draw_marks(surface, board, n, cell_size, font):
    """Vẽ quân X và O lên bàn cờ."""
    x_color = (200, 30, 30)  # Màu đỏ
    o_color = (30, 30, 200)  # Màu xanh
    
    for r in range(n):
        for c in range(n):
            v = board[r*n + c]
            cx = c*cell_size + cell_size//2
            cy = r*cell_size + cell_size//2
            
            if v == 'X':
                off = cell_size // 4
                pygame.draw.line(surface, x_color, (cx-off, cy-off), (cx+off, cy+off), 5)
                pygame.draw.line(surface, x_color, (cx-off, cy+off), (cx+off, cy-off), 5)
            elif v == 'O':
                pygame.draw.circle(surface, o_color, (cx, cy), cell_size//3, 4)
            else:
                # Vẽ số mờ nhạt để người chơi dễ nhìn vị trí
                txt = font.render(str(v), True, (200, 200, 200))
                tr = txt.get_rect(center=(cx, cy))
                surface.blit(txt, tr)

def pos_to_cell(pos, cell_size, n):
    """Chuyển đổi tọa độ chuột (pixel) thành tọa độ ô (hàng, cột)."""
    x, y = pos
    c = x // cell_size
    r = y // cell_size
    if 0 <= r < n and 0 <= c < n:
        return r, c
    return None, None

def run_pygame(n):
    pygame.init()
    
    # Cấu hình cửa sổ
    max_window = 700
    cell_size = max(40, min(max_window // n, 120)) # Tự động chỉnh size ô cho đẹp
    win_size = cell_size * n
    
    # --- Menu chọn chế độ (Console) ---
    print("\n" + "="*30)
    print(f" KHỞI TẠO GAME TIC-TAC-TOE {n}x{n}")
    print("="*30)
    try:
        mode = int(input("1. Người đấu Người\n2. Người đấu Máy\nChọn (1/2): ").strip())
    except: mode = 1
    
    ai_enabled = (mode == 2)
    ai_player = 'O' # Mặc định máy là O
    
    if ai_enabled:
        try:
            p_choice = input("Bạn muốn cầm quân nào? (X/O): ").strip().upper()
            ai_player = 'X' if p_choice == 'O' else 'O'
        except: pass
        print(f"--> Bạn cầm quân {('X' if ai_player == 'O' else 'O')}, Máy cầm quân {ai_player}")

    # Khởi tạo Pygame
    surface = pygame.display.set_mode((win_size, win_size))
    pygame.display.set_caption(f"{n}x{n} Tic-Tac-Toe")
    clock = pygame.time.Clock()
    
    # Font chữ (Load 1 lần để tối ưu hiệu năng)
    game_font = pygame.font.SysFont("Arial", max(20, cell_size//3))
    status_font = pygame.font.SysFont("Arial", 24)

    # Biến trạng thái game
    board = create_board(n)
    current = 'X'
    running = True
    winner = None

    # --- VÒNG LẶP CHÍNH (GAME LOOP) ---
    while running:
        # 1. Xử lý sự kiện (Event Handling)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Xử lý click chuột (Chỉ khi chưa có ai thắng)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner is None:
                # Nếu đến lượt máy thì không cho người click
                if ai_enabled and current == ai_player:
                    continue

                r, c = pos_to_cell(event.pos, cell_size, n)
                if r is not None:
                    idx = r*n + c
                    # Nếu ô còn trống
                    if board[idx] != 'X' and board[idx] != 'O':
                        board[idx] = current
                        winner = check_winner_n(board, n, n)
                        
                        # Kiểm tra hòa
                        if winner is None and not get_available_cells(board):
                            winner = 'TIE'
                            
                        # Đổi lượt
                        current = 'O' if current == 'X' else 'X'

            # Phím tắt Reset game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Nhấn R để chơi lại
                    board = create_board(n)
                    current = 'X'
                    winner = None
                    print("--> Đã reset bàn cờ!")

        # 2. Xử lý AI (Nếu đến lượt máy)
        if ai_enabled and winner is None and current == ai_player:
            # pygame.time.wait(300) # Tạo độ trễ nhỏ cho giống người đang nghĩ
            
            ai_idx = find_best_move_simple(board, n, ai_player)
            
            if ai_idx is not None:
                board[ai_idx] = ai_player
                winner = check_winner_n(board, n, n)
                if winner is None and not get_available_cells(board):
                    winner = 'TIE'
                current = 'O' if current == 'X' else 'X'

        # 3. Vẽ đồ họa (Rendering)
        surface.fill((245, 245, 245)) # Màu nền trắng xám
        draw_grid(surface, n, cell_size)
        draw_marks(surface, board, n, cell_size, game_font)

        # Hiển thị thông báo kết quả
        if winner:
            if winner == 'TIE':
                msg = "HOA! Nhan phim R de choi lai"
                color = (100, 100, 100)
            else:
                msg = f"{winner} CHIEN THANG! Nhan R de choi lai"
                color = (0, 150, 0)
            
            # Vẽ background cho chữ dễ đọc
            txt_surf = status_font.render(msg, True, (255, 255, 255))
            txt_bg = pygame.Surface((txt_surf.get_width() + 20, txt_surf.get_height() + 10))
            txt_bg.fill(color)
            
            center_x, center_y = win_size // 2, win_size // 2
            surface.blit(txt_bg, (center_x - txt_bg.get_width()//2, center_y - txt_bg.get_height()//2))
            surface.blit(txt_surf, (center_x - txt_surf.get_width()//2, center_y - txt_surf.get_height()//2))

        pygame.display.flip()
        clock.tick(30) # Giới hạn 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        n_input = int(input('Nhập kích thước bàn cờ n (ví dụ 3, 5, 10): ').strip())
        n = max(3, n_input) # Tối thiểu là 3
    except:
        n = 3
        print("Lỗi nhập liệu, mặc định n=3")
    
    run_pygame(n)