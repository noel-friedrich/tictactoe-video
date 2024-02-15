from board import TicTacToeBoard, X, O, N, board_win_combinations, get_opponent, board_possible_moves
from PIL import Image, ImageFont, ImageDraw, ImageColor
import random, copy

random.seed(42)

COMPUTER_TOKEN = O
PLAYER_TOKEN = get_opponent(COMPUTER_TOKEN)


# generating all boards

boards_map: dict[int, "ShowBoard"] = {}

class ShowBoard:

    def __init__(self, board: TicTacToeBoard) -> None:
        self.board = board
        self.marked_moves = []
        self.move_children_map: dict[int, ShowBoard] = {}
        self.depth = None
        self.id = board.calc_id()
        self.idx = 0
    
    @classmethod
    def get_board(cls, board: TicTacToeBoard):
        id = board.calc_id()
        if id in boards_map:
            return boards_map[id]
        show_board = cls(board)
        boards_map[id] = show_board
        return show_board

    @property
    def children(self):
        return list(self.move_children_map.values())
    
    def time(self, offset_seconds=0):
        if self.idx == None:
            return "None"
        minutes = (self.idx + offset_seconds) // 60
        seconds = (self.idx + offset_seconds) % 60
        return f"{minutes:0>2}:{seconds:0>2}"

    def fill_children(self, depth=0):
        self.depth = depth
        for i, move in enumerate(board_possible_moves):
            if not self.board.field_is_free(move):
                continue

            new_board = self.board.make_move_board(move, PLAYER_TOKEN)
            marked_moves = []

            if not new_board.is_terminal():
                computer_move = new_board.make_computer_move(COMPUTER_TOKEN)
                marked_moves.append(computer_move)

            if not new_board.is_terminal() and new_board.count_filled_cells() == 8:
                for move in board_possible_moves:
                    if new_board.field_is_free(move):
                        new_board.data[move[1]][move[0]] = X
                        marked_moves.append(move)
                        break
            
            new_show_board = ShowBoard.get_board(new_board)
            new_show_board.depth = depth + 1
            new_show_board.marked_moves = marked_moves
            self.move_children_map[i] = new_show_board

            if not new_board.is_terminal():
                new_show_board.fill_children(depth=depth + 1)
    
    def __repr__(self):
        return f"SB(board={repr(self.board)}, id={self.id}, depth={self.depth})"

starting_board = TicTacToeBoard.from_id(0)
root = ShowBoard.get_board(starting_board)

root.fill_children()

all_boards: list[ShowBoard] = sorted(list(boards_map.values()), key=lambda sb: sb.depth)

for i, board in enumerate(all_boards):
    board.idx = i

if __name__ == "__main__":
    # testing it out
    sb = all_boards[0]
    while not sb.board.is_terminal():
        print(sb.board)
        child_move_map = {i: c.idx for i, c in sb.move_children_map.items()}
        sb = all_boards[child_move_map[int(input("Your Move: ")) - 1]]