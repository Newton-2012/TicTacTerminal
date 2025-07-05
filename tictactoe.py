import time

# ANSI Color Codes
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

def line_break(n):
    print("-" * n)

def fake_loading(text="Loading", dots=9, delay=0.3, done_text="Done!"):
    print(text, end="", flush=True)
    for _ in range(dots):
        print(".", end="", flush=True)
        time.sleep(delay)
    print(done_text)

def print_board(board):
    line_break(45)
    for i, row in enumerate(board):
        print(" | ".join(f"{YELLOW if cell=='X' else RED if cell=='O' else RESET}{cell or ' '}{RESET}" for cell in row))
        if i < 2:
            print("---+---+---")
    line_break(45)

def check_winner(board, player):
    win = [player] * 3
    # Rows
    for row in board:
        if row == win:
            return True
    # Columns
    for col in range(3):
        if [board[row][col] for row in range(3)] == win:
            return True
    # Diagonals
    if [board[i][i] for i in range(3)] == win:
        return True
    if [board[i][2 - i] for i in range(3)] == win:
        return True
    return False

def is_full(board):
    return all(cell is not None for row in board for cell in row)

def get_human_move(board):
    while True:
        try:
            move = input(f"{GREEN}Your move (row and col 0-2): {RESET}")
            row, col = map(int, move.split())
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print(RED + "Integers between 0 and 2 only." + RESET)
                continue
            if board[row][col] is not None:
                print(RED + "Spot taken, try again." + RESET)
                continue
            return row, col
        except Exception:
            print(RED + "Enter two numbers separated by space." + RESET)

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[r][c] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[r][c] = None
                    best_score = min(score, best_score)
        return best_score

def get_ai_move(board):
    best_score = -float('inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                board[r][c] = 'O'
                score = minimax(board, 0, False)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def replay():
    replay = input("Do you want to play again? (Y/N): ").strip().lower()
    if replay != 'y':
        fake_loading("Closing Application", dots=12, delay=0.05, done_text="")


def commands():
    board = [[None]*3 for _ in range(3)]
    current_player = 'X'  # Human always starts

    while True:
        print_board(board)
        if current_player == 'X':
            row, col = get_human_move(board)
        else:
            fake_loading("AI is thinking", dots=6, delay=0.2, done_text=" Done!")
            row, col = get_ai_move(board)

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            if current_player == 'X':
                print(GREEN + "You win!" + RESET)
            else:
                print(RED + "AI wins!" + RESET)
            break

        if is_full(board):
            print_board(board)
            print(YELLOW + "Tie game. At least you didn't lose..." + RESET)
            break

        current_player = 'O' if current_player == 'X' else 'X'

def main():
    line_break(45)
    print("Copyright (c) 2025 Newton2012 - MIT License")
    fake_loading("Starting Program")
    line_break(45)
    print(BLUE + "Tic Tac Terminal - Version 1.0.0" + RESET)
    line_break(45)

    while True:
        commands()
        replay_choice = input("Do you want to play again? (Y/N): ").strip().lower()
        if replay_choice != 'y':
            fake_loading("Closing Application", dots=12, delay=0.05, done_text="")
            break
if __name__ == "__main__":
    main()
