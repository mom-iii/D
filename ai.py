# オセロのマス目の点数を定義（6x6）
# 高得点エリア (隅や周囲のマス) を優先
SCORES = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, -2, -2, -50, -20],
    [10, -2, 3, 3, -2, 10],
    [10, -2, 3, 3, -2, 10],
    [-20, -50, -2, -2, -50, -20],
    [100, -20, 10, 10, -20, 100],
]

# ボードの初期状態
EMPTY, BLACK, WHITE = 0, 1, 2
BOARD = [[EMPTY] * 6 for _ in range(6)]
BOARD[2][2], BOARD[3][3] = WHITE, WHITE
BOARD[2][3], BOARD[3][2] = BLACK, BLACK

# 方向の定義
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def is_valid_move(board, row, col, color):
    """指定した場所に駒を置けるか確認"""
    if board[row][col] != EMPTY:
        return False
    opponent = BLACK if color == WHITE else WHITE
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        has_opponent = False
        while 0 <= r < 6 and 0 <= c < 6 and board[r][c] == opponent:
            has_opponent = True
            r, c = r + dr, c + dc
        if has_opponent and 0 <= r < 6 and 0 <= c < 6 and board[r][c] == color:
            return True
    return False


def get_valid_moves(board, color):
    """全ての合法手を取得"""
    valid_moves = []
    for row in range(6):
        for col in range(6):
            if is_valid_move(board, row, col, color):
                valid_moves.append((row, col))
    return valid_moves


def apply_move(board, row, col, color):
    """指定した手を盤面に適用"""
    opponent = BLACK if color == WHITE else WHITE
    board[row][col] = color
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        stones_to_flip = []
        while 0 <= r < 6 and 0 <= c < 6 and board[r][c] == opponent:
            stones_to_flip.append((r, c))
            r, c = r + dr, c + dc
        if stones_to_flip and 0 <= r < 6 and 0 <= c < 6 and board[r][c] == color:
            for flip_r, flip_c in stones_to_flip:
                board[flip_r][flip_c] = color


def choose_best_move(board, color):
    """最善手を選ぶ"""
    valid_moves = get_valid_moves(board, color)
    if not valid_moves:
        return None
    best_move = None
    best_score = float('-inf')
    for row, col in valid_moves:
        score = SCORES[row][col]
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move


def print_board(board):
    """盤面を表示"""
    symbols = {EMPTY: ".", BLACK: "B", WHITE: "W"}
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print()


# テストプレイ
current_color = BLACK
print_board(BOARD)
while True:
    move = choose_best_move(BOARD, current_color)
    if move is None:
        print(f"{'BLACK' if current_color == BLACK else 'WHITE'} has no valid moves.")
        current_color = WHITE if current_color == BLACK else BLACK
        if not get_valid_moves(BOARD, current_color):
            print("Game over!")
            break
        continue
    print(f"{'BLACK' if current_color == BLACK else 'WHITE'} plays at {move}")
    apply_move(BOARD, move[0], move[1], current_color)
    print_board(BOARD)
    current_color = WHITE if current_color == BLACK else BLACK
