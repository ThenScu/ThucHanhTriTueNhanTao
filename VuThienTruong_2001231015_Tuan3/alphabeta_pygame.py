import sys
import pygame

# -- helpers (self-contained, don't import alphabeta.py because it runs main on import) --

def create_board(n):
    return [i for i in range(1, n * n + 1)]


def check_winner_n(board, n, win_len):
    def at(r, c):
        return board[r * n + c]

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(n):
        for c in range(n):
            player = at(r, c)
            if player != 'X' and player != 'O':
                continue
            for dr, dc in directions:
                cnt = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < n and 0 <= cc < n and at(rr, cc) == player:
                    cnt += 1
                    if cnt >= win_len:
                        return player
                    rr += dr
                    cc += dc
    return None


def GetWinner(board):
    """Compatibility function named like original file.
    If board length is 9, use classic 3x3 checks; otherwise infer n and use check_winner_n with win_len=n.
    Returns 'X' or 'O' or None.
    """
    ln = len(board)
    if ln == 9:
        # classic 3x3 direct checks (indices 0..8)
        if board[0] == board[1] == board[2]:
            return board[0]
        if board[3] == board[4] == board[5]:
            return board[3]
        if board[6] == board[7] == board[8]:
            return board[6]
        if board[0] == board[3] == board[6]:
            return board[0]
        if board[1] == board[4] == board[7]:
            return board[1]
        if board[2] == board[5] == board[8]:
            return board[2]
        if board[0] == board[4] == board[8]:
            return board[0]
        if board[2] == board[4] == board[6]:
            return board[2]
        return None
    # otherwise try generalized checker
    import math
    s = int(math.isqrt(ln))
    if s * s == ln:
        return check_winner_n(board, s, s)
    return None


def PrintBoard(board):
    """Console print for compatibility (3x3 or n x n if square)."""
    import math
    ln = len(board)
    s = int(math.isqrt(ln))
    if s * s != ln:
        print(board)
        return
    cell_width = len(str(ln))
    sep = ' | '
    for r in range(s):
        row = [str(board[r*s + c]).rjust(cell_width) for c in range(s)]
        print(sep.join(row))
        if r != s-1:
            print('-' * (s * cell_width + (len(sep) * (s - 1))))


def GetAvailableCells(board):
    """Return list of available cell numbers (like original file)."""
    available = []
    for cell in board:
        if cell != 'X' and cell != 'O':
            available.append(cell)
    return available


def minimax(position, depth, alpha, beta, isMaximizing):
    """Minimax adapted from original file for 3x3 compatibility.
    For larger boards this will be very slow and isn't used by the simple AI.
    """
    import math
    winner = GetWinner(position)
    if winner is not None:
        return 10 - depth if winner == 'X' else -10 + depth
    if len(GetAvailableCells(position)) == 0:
        return 0

    if isMaximizing:
        maxEval = -math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = 'X'
            Eval = minimax(position, depth + 1, alpha, beta, False)
            position[cell - 1] = cell
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = 'O'
            Eval = minimax(position, depth + 1, alpha, beta, True)
            position[cell - 1] = cell
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            if beta <= alpha:
                break
        return minEval


def FindBestMove(currentPosition, AI):
    """Find best move using minimax (copied structure from original file)."""
    import math
    bestVal = -math.inf if AI == 'X' else math.inf
    bestMove = -1
    for cell in GetAvailableCells(currentPosition):
        currentPosition[cell - 1] = AI
        moveVal = minimax(currentPosition, 0, -math.inf, math.inf, False if AI == 'X' else True)
        currentPosition[cell - 1] = cell
        if AI == 'X' and moveVal > bestVal:
            bestMove = cell
            bestVal = moveVal
        elif AI == 'O' and moveVal < bestVal:
            bestMove = cell
            bestVal = moveVal
    return bestMove


# -- pygame UI --

def draw_grid(surface, n, cell_size, line_color=(0,0,0)):
    w, h = surface.get_size()
    for i in range(1, n):
        # vertical
        pygame.draw.line(surface, line_color, (i*cell_size, 0), (i*cell_size, h), 2)
        # horizontal
        pygame.draw.line(surface, line_color, (0, i*cell_size), (w, i*cell_size), 2)


def draw_marks(surface, board, n, cell_size, x_color=(200,30,30), o_color=(30,30,200)):
    font = pygame.font.SysFont(None, max(24, cell_size//2))
    for r in range(n):
        for c in range(n):
            v = board[r*n + c]
            cx = c*cell_size + cell_size//2
            cy = r*cell_size + cell_size//2
            if v == 'X':
                # draw X
                off = cell_size//3
                pygame.draw.line(surface, x_color, (cx-off, cy-off), (cx+off, cy+off), 4)
                pygame.draw.line(surface, x_color, (cx-off, cy+off), (cx+off, cy-off), 4)
            elif v == 'O':
                pygame.draw.circle(surface, o_color, (cx, cy), cell_size//3, 4)
            else:
                # draw cell number faintly
                txt = font.render(str(v), True, (120,120,120))
                tr = txt.get_rect(center=(cx,cy))
                surface.blit(txt, tr)


def pos_to_cell(pos, cell_size, n):
    x, y = pos
    c = x // cell_size
    r = y // cell_size
    if 0 <= r < n and 0 <= c < n:
        return r, c
    return None, None


def find_best_move_simple(board, n, ai_symbol):
    """Simple AI: 1) win if possible, 2) block opponent's win, 3) take center, 4) pick random."""
    import random

    opponent = 'O' if ai_symbol == 'X' else 'X'

    # 1) winning move for AI
    for i in range(n*n):
        if board[i] != 'X' and board[i] != 'O':
            board[i] = ai_symbol
            if check_winner_n(board, n, n) == ai_symbol:
                board[i] = i+1
                return i
            board[i] = i+1

    # 2) block opponent winning move
    for i in range(n*n):
        if board[i] != 'X' and board[i] != 'O':
            board[i] = opponent
            if check_winner_n(board, n, n) == opponent:
                board[i] = i+1
                return i
            board[i] = i+1

    # 3) take center
    center = (n*n)//2
    if board[center] != 'X' and board[center] != 'O':
        return center

    # 4) pick random available
    avail = [i for i in range(n*n) if board[i] != 'X' and board[i] != 'O']
    if not avail:
        return None
    return random.choice(avail)


def run_pygame(n):
    pygame.init()
    # determine cell size and window size (cap maximum size)
    max_window = 700
    cell_size = max(30, min(max_window // n, 100))
    win_size = cell_size * n
    # Trước khi mở cửa sổ, hỏi chế độ chơi để tránh prompt xuất hiện khi cửa sổ đã mở
    try:
        print("Chọn chế độ: 1) Người vs Người  2) Người vs Máy")
        mode = int(input("Chọn (1 hoặc 2): ").strip())
    except Exception:
        mode = 1
    ai_enabled = (mode == 2)
    ai_player = 'O'
    if ai_enabled:
        try:
            s = input("Máy đánh X hay O? (gõ X hoặc O, mặc định O): ").strip().upper()
            if s in ('X', 'O'):
                ai_player = s
        except Exception:
            ai_player = 'O'

    surface = pygame.display.set_mode((win_size, win_size))
    pygame.display.set_caption(f"{n}x{n} Tic-Tac-Toe (win {n})")

    board = create_board(n)
    current = 'X'
    clock = pygame.time.Clock()
    running = True
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner is None:
                r, c = pos_to_cell(event.pos, cell_size, n)
                if r is None:
                    continue
                idx = r*n + c
                if board[idx] == 'X' or board[idx] == 'O':
                    continue
                board[idx] = current
                winner = check_winner_n(board, n, n)
                if winner is None and all((cell=='X' or cell=='O') for cell in board):
                    winner = 'TIE'
                current = 'O' if current == 'X' else 'X'
                # if AI enabled and it's AI's turn, it will play in the next frame
            elif event.type == pygame.KEYDOWN and winner is not None:
                # any key restarts
                if event.key == pygame.K_r:
                    board = create_board(n)
                    current = 'X'
                    winner = None

        # Nếu AI bật và tới lượt AI thì AI chọn nước và đánh
        if ai_enabled and winner is None and current == ai_player:
            ai_idx = find_best_move_simple(board, n, ai_player)
            if ai_idx is not None:
                board[ai_idx] = ai_player
                winner = check_winner_n(board, n, n)
                if winner is None and all((cell=='X' or cell=='O') for cell in board):
                    winner = 'TIE'
                current = 'O' if current == 'X' else 'X'

        surface.fill((240,240,240))
        draw_grid(surface, n, cell_size)
        draw_marks(surface, board, n, cell_size)

        # draw status
        font = pygame.font.SysFont(None, 24)
        if winner is None:
            status = f"Turn: {current}"
        elif winner == 'TIE':
            status = "Result: TIE - press R to restart"
        else:
            status = f"Result: {winner} WINS - press R to restart"
        txt = font.render(status, True, (10,10,10))
        surface.blit(txt, (5, win_size-24))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    try:
        n = int(input('Nhập kích thước bàn n (ví dụ 3 hoặc 5): ').strip())
        if n < 1:
            print('n phải là số nguyên dương. Sử dụng n = 3.')
            n = 3
    except Exception:
        print('Giá trị không hợp lệ. Sử dụng n = 3.')
        n = 3

    run_pygame(n)
