import os
import math

# Tham khảo: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/

def GetWinner(board):
    """
    Hàm kiểm tra người thắng cuộc trên bàn cờ hiện tại.
    Trả về 'X' hoặc 'O' nếu thắng, trả về None nếu chưa ai thắng.
    """
    # Các trường hợp thắng theo hàng ngang (Indices: 0-1-2, 3-4-5, 6-7-8)
    if board[0] == board[1] and board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] and board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] and board[7] == board[8]:
        return board[6]
    
    # Các trường hợp thắng theo hàng dọc (Indices: 0-3-6, 1-4-7, 2-5-8)
    elif board[0] == board[3] and board[3] == board[6]:
        return board[0]
    elif board[1] == board[4] and board[4] == board[7]:
        return board[1]
    elif board[2] == board[5] and board[5] == board[8]:
        return board[2]
    
    # Các trường hợp thắng theo đường chéo (Indices: 0-4-8, 2-4-6)
    elif board[0] == board[4] and board[4] == board[8]:
        return board[0]
    elif board[2] == board[4] and board[4] == board[6]:
        return board[2]
        
    return None

def PrintBoard(board):
    """
    Xóa màn hình console và in bàn cờ hiện tại.
    """
    # Lệnh xóa màn hình: 'cls' cho Windows, 'clear' cho Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''
    {board[0]} | {board[1]} | {board[2]}
    --+---+--
    {board[3]} | {board[4]} | {board[5]}
    --+---+--
    {board[6]} | {board[7]} | {board[8]}
    ''')

def GetAvailableCells(board):
    """
    Trả về danh sách các chỉ số (số thứ tự ô) còn trống.
    Ví dụ: Nếu ô 1 và 5 đã đánh, trả về [2, 3, 4, 6, 7, 8, 9]
    """
    available = list()
    for cell in board:
        # Nếu ô không phải là 'X' hay 'O' (tức là vẫn còn là số) thì là ô trống
        if cell != "X" and cell != "O":
            available.append(cell)
    return available

def minimax(position, depth, alpha, beta, isMaximizing):
    """
    Thuật toán cốt lõi: Minimax với Cắt tỉa Alpha-Beta.
    Mục tiêu: Tính điểm số tốt nhất cho nước đi hiện tại.
    
    Tham số:
    - position: Trạng thái bàn cờ.
    - depth: Độ sâu của cây tìm kiếm (càng sâu tức là càng tốn nhiều nước đi).
    - alpha: Giá trị tốt nhất mà máy (Maximizer) đã tìm thấy.
    - beta: Giá trị tốt nhất mà đối thủ (Minimizer) đã tìm thấy.
    - isMaximizing: True nếu đến lượt máy (muốn điểm cao), False nếu đến lượt người (muốn điểm thấp).
    """
    
    # 1. Kiểm tra trạng thái kết thúc (Base case)
    winner = GetWinner(position)
    if winner != None:
        # Nếu X thắng: Trả về 10 trừ đi độ sâu (thắng càng nhanh càng tốt -> điểm càng cao)
        # Nếu O thắng: Trả về -10 cộng độ sâu (thua càng chậm càng tốt -> điểm càng đỡ thấp)
        return 10 - depth if winner == "X" else -10 + depth
    
    # Nếu hòa (không còn ô trống và không ai thắng)
    if len(GetAvailableCells(position)) == 0:
        return 0

    # 2. Thuật toán đệ quy
    if isMaximizing: # Lượt của người muốn Max (thường là X)
        maxEval = -math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = "X" # Thử đi nước X
            
            # Gọi đệ quy cho lượt tiếp theo (là lượt Min)
            Eval = minimax(position, depth + 1, alpha, beta, False)
            
            # Backtrack: Hoàn tác nước đi để thử ô khác
            position[cell - 1] = cell 
            
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            
            # Cắt tỉa Alpha-Beta: Nếu nhánh này tệ hơn nhánh đã tìm thấy trước đó, dừng lại
            if beta <= alpha:
                break 
        return maxEval

    else: # Lượt của người muốn Min (thường là O)
        minEval = +math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = "O" # Thử đi nước O
            
            # Gọi đệ quy cho lượt tiếp theo (là lượt Max)
            Eval = minimax(position, depth + 1, alpha, beta, True)
            
            # Backtrack
            position[cell - 1] = cell
            
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            
            # Cắt tỉa Alpha-Beta
            if beta <= alpha:
                break
        return minEval
    

def FindBestMove(currentPosition, AI):
    """
    Hàm tìm nước đi tối ưu nhất cho AI.
    Nó duyệt qua tất cả các ô trống, gọi hàm minimax để tính điểm, 
    và chọn ô có điểm tốt nhất.
    """
    # Nếu AI là X thì cần tìm Max, nếu AI là O thì cần tìm Min
    bestVal = -math.inf if AI == "X" else +math.inf
    bestMove = -1
    
    for cell in GetAvailableCells(currentPosition):
        currentPosition[cell - 1] = AI # AI thử đi vào ô này
        
        # Gọi minimax để tính xem tương lai của nước đi này thế nào
        # Nếu AI vừa đi (AI="X"), lượt tiếp theo là False (Minimizing) và ngược lại
        moveVal = minimax(currentPosition, 0, -math.inf, +math.inf, False if AI == "X" else True)
        
        currentPosition[cell - 1] = cell # Hoàn tác (Backtrack)
        
        # Cập nhật nước đi tốt nhất
        if (AI == "X" and moveVal > bestVal): # X muốn điểm cao nhất
            bestMove = cell
            bestVal = moveVal
        elif (AI == "O" and moveVal < bestVal): # O muốn điểm thấp nhất
            bestMove = cell
            bestVal = moveVal
            
    return bestMove

def main():
    # Chọn phe
    player = input("Bạn muốn chơi X hay O? ").strip().upper()
    AI = "O" if player == "X" else "X"
    
    # Khởi tạo bàn cờ với các số từ 1 đến 9
    currentGame = [*range(1, 10)]
    
    # Mặc định X luôn đi trước
    currentTurn = "X"
    counter = 0 # Đếm số lượt đi để kiểm tra hòa nhanh (tùy chọn)

    while True:
        # --- LƯỢT CỦA AI ---
        if currentTurn == AI:
            print(f"AI ({AI}) đang suy nghĩ...")
            # Mẹo tối ưu: Nếu AI đi trước (bàn cờ trống), luôn đánh ô 5 (giữa) hoặc 1 (góc) để thắng nhanh/không thua
            # Code dưới đây để AI tự tính toán hết bằng Minimax
            cell = FindBestMove(currentGame, AI)
            currentGame[cell - 1] = AI
            currentTurn = player # Đổi lượt sang người chơi

        # --- LƯỢT CỦA NGƯỜI CHƠI ---
        elif currentTurn == player:
            PrintBoard(currentGame)
            while True:
                try:
                    humanInput = int(input(f"Lượt bạn ({player}). Nhập số ô (1-9): ").strip())
                    # Kiểm tra xem ô đó có nằm trong danh sách ô còn trống không
                    if humanInput in currentGame:
                        currentGame[humanInput - 1] = player
                        currentTurn = AI # Đổi lượt sang AI
                        break
                    else:
                        print("Ô này đã bị đánh hoặc không hợp lệ. Chọn ô khác!")
                except ValueError:
                    print("Vui lòng nhập một con số!")
        
        # --- KIỂM TRA KẾT THÚC GAME ---
        winner_res = GetWinner(currentGame)
        if winner_res != None:
            PrintBoard(currentGame)
            print(f"KẾT QUẢ: {winner_res} ĐÃ THẮNG!!!")
            break
        
        counter += 1
        # Kiểm tra hòa (nếu không còn ai thắng và bàn cờ đầy hoặc hết lượt)
        if GetWinner(currentGame) == None and len(GetAvailableCells(currentGame)) == 0:
            PrintBoard(currentGame)
            print("KẾT QUẢ: HÒA (Tie).")
            break

if __name__ == "__main__":
    main()