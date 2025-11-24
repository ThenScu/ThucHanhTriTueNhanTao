import copy
import math
import random
import numpy

# Các biến toàn cục để định nghĩa quân cờ
X = "X"
O = "O"
EMPTY = None
user = None
ai = None

def initial_state():
    # Hàm này trả về trạng thái bắt đầu của bàn cờ (một ma trận 3x3 toàn ô trống)
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    # Hàm xác định xem lượt tiếp theo là của ai (Người chơi hay AI)
    count = 0
    # Duyệt qua bàn cờ để đếm số lượng quân đã đánh
    for i in board:
        for j in i:
            if j:
                count += 1
    # Nếu số lượng quân là lẻ -> lượt AI, chẵn -> lượt người chơi (giả định người đi trước)
    if count % 2 != 0:
        return ai
    return user

def actions(board):
    # Trả về tập hợp tất cả các hành động (nước đi) có thể thực hiện (các ô còn trống)
    res = set()
    board_len = len(board)
    for i in range(board_len):
        for j in range(board_len):
            # Nếu ô tại vị trí i, j là rỗng thì thêm vào danh sách nước đi hợp lệ
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    # Trả về trạng thái bàn cờ MỚI sau khi thực hiện nước đi (i, j)
    curr_player = player(board) # Xác định người đi nước này
    result_board = copy.deepcopy(board) # Tạo bản sao bàn cờ (để không làm hỏng bàn cờ chính)
    (i, j) = action
    result_board[i][j] = curr_player # Đánh dấu nước đi vào bản sao
    return result_board

def get_horizontal_winner(board):
    # Kiểm tra chiến thắng theo hàng ngang
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        winner_val = board[i][0] # Lấy ô đầu hàng làm mốc
        for j in range(board_len):
            if board[i][j] != winner_val: # Nếu có ô khác mốc -> hàng này không thắng
                winner_val = None
        if winner_val: # Nếu duyệt hết hàng mà vẫn khớp -> trả về người thắng
            return winner_val
    return winner_val

def get_vertical_winner(board):
    # Kiểm tra chiến thắng theo hàng dọc
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        winner_val = board[0][i] # Lấy ô đầu cột làm mốc
        for j in range(board_len):
            if board[j][i] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_diagonal_winner(board):
    # Kiểm tra chiến thắng theo đường chéo
    winner_val = None
    board_len = len(board)
    
    # Kiểm tra chéo chính (từ trên trái xuống dưới phải)
    winner_val = board[0][0]
    for i in range(board_len):
        if board[i][i] != winner_val:
            winner_val = None
    if winner_val:
        return winner_val
        
    # Kiểm tra chéo phụ (từ trên phải xuống dưới trái)
    winner_val = board[0][board_len - 1]
    for i in range(board_len):
        j = board_len - 1 - i
        if board[i][j] != winner_val:
            winner_val = None
    return winner_val

def winner(board):
    # Trả về người thắng cuộc của trò chơi nếu có (kết hợp kiểm tra ngang, dọc, chéo)
    # Nếu không ai thắng thì trả về None
    winner_val = get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board) or None
    return winner_val

def terminal(board):
    # Kiểm tra xem trò chơi đã kết thúc chưa
    # Kết thúc khi có người thắng
    if winner(board) != None:
        return True
    # Hoặc khi bàn cờ đã đầy (không còn ô EMPTY)
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True

def utility(board):
    # Hàm tiện ích: Trả về điểm số của trạng thái kết thúc
    # 1 nếu X thắng, -1 nếu O thắng, 0 nếu hòa
    winner_val = winner(board)
    if winner_val == X:
        return 1
    elif winner_val == O:
        return -1
    return 0

def maxValue(state):
    # Hàm tìm giá trị lớn nhất (Dùng cho lượt của X - người muốn Max điểm)
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        # Chọn giá trị lớn nhất trong các giá trị nhỏ nhất mà đối thủ sẽ chọn
        v = max(v, minValue(result(state, action)))
    return v

def minValue(state):
    # Hàm tìm giá trị nhỏ nhất (Dùng cho lượt của O - người muốn Min điểm)
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        # Chọn giá trị nhỏ nhất trong các giá trị lớn nhất mà đối thủ sẽ chọn
        v = min(v, maxValue(result(state, action)))
    return v

def minimax(board):
    # Hàm Minimax chính: Trả về hành động (nước đi) tối ưu cho người chơi hiện tại
    current_player = player(board)
    if current_player == X:
        # Nếu là X, tìm nước đi để đạt Max điểm
        min_val = -math.inf
        for action in actions(board):
            check = minValue(result(board, action))
            if check > min_val:
                min_val = check
                move = action
    else:
        # Nếu là O, tìm nước đi để đạt Min điểm (vì O muốn điểm là -1)
        max_val = math.inf
        for action in actions(board):
            check = maxValue(result(board, action))
            if check < max_val:
                max_val = check
                move = action
    return move

if __name__ == "__main__":
    # Khởi tạo bàn cờ
    board = initial_state()
    ai_turn = False
    print("Choose a player")
    user = input() # Người dùng chọn X hoặc O
    
    # Gán phe cho AI dựa trên lựa chọn của người dùng
    if user == "X":
        ai = "O"
    else:
        ai = "X"
        
    # Vòng lặp game chính
    while True:
        game_over = terminal(board)
        playr = player(board)
        
        # Nếu game kết thúc
        if game_over:
            winner_res = winner(board)
            if winner_res is None:
                print("Game Over: Tie.") # Hòa
            else:
                print(f"Game Over: {winner_res} wins.") # Có người thắng
            break;
        else:
            # Nếu lượt hiện tại không phải của người dùng (tức là lượt AI) và game chưa xong
            if user != playr and not game_over:
                if ai_turn:
                    # AI tính toán nước đi bằng Minimax
                    move = minimax(board)
                    board = result(board, move)
                    ai_turn = False
                    print(numpy.array(board)) # In bàn cờ ra
            # Nếu lượt hiện tại là của người dùng
            elif user == playr and not game_over:
                ai_turn = True
                print("Enter the position to move (row,col)")
                i = int(input("Row: "))
                j = int(input("Col: "))
                # Kiểm tra ô đó có trống không
                if board[i][j] == EMPTY:
                    board = result(board, (i, j))
                    print(numpy.array(board))