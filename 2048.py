import random
import curses

def init_game():
    return [[0] * 4 for _ in range(4)]

def add_new_number(board):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2 if random.random() < 0.9 else 4

def compress(board):
    new_board = [[0] * 4 for _ in range(4)]
    for r in range(4):
        pos = 0
        for c in range(4):
            if board[r][c] != 0:
                new_board[r][pos] = board[r][c]
                pos += 1
    return new_board

def merge(board):
    for r in range(4):
        for c in range(3):
            if board[r][c] == board[r][c + 1] and board[r][c] != 0:
                board[r][c] *= 2
                board[r][c + 1] = 0
    return board

def reverse(board):
    return [row[::-1] for row in board]

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_left(board):
    board = compress(board)
    board = merge(board)
    board = compress(board)
    return board

def move_right(board):
    board = reverse(board)
    board = move_left(board)
    board = reverse(board)
    return board

def move_up(board):
    board = transpose(board)
    board = move_left(board)
    board = transpose(board)
    return board

def move_down(board):
    board = transpose(board)
    board = move_right(board)
    board = transpose(board)
    return board

def is_game_over(board):
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return False
            if c < 3 and board[r][c] == board[r][c + 1]:
                return False
            if r < 3 and board[r][c] == board[r + 1][c]:
                return False
    return True

def draw_board(stdscr, board):
    stdscr.clear()
    for r in range(4):
        for c in range(4):
            stdscr.addstr(r * 2, c * 5, str(board[r][c]) if board[r][c] != 0 else '.')
    stdscr.refresh()

def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    board = init_game()
    add_new_number(board)
    add_new_number(board)
    while True:
        draw_board(stdscr, board)
        key = stdscr.getch()
        if key == ord('q'):
            break
        new_board = None
        if key == curses.KEY_LEFT:
            new_board = move_left(board)
        elif key == curses.KEY_RIGHT:
            new_board = move_right(board)
        elif key == curses.KEY_UP:
            new_board = move_up(board)
        elif key == curses.KEY_DOWN:
            new_board = move_down(board)
        if new_board and new_board != board:
            board = new_board
            add_new_number(board)
        if is_game_over(board):
            stdscr.addstr(9, 0, "Game Over! Press 'q' to exit.")
            stdscr.refresh()
            while stdscr.getch() != ord('q'):
                pass
            break

def main():
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()
