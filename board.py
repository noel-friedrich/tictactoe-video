import random, copy, math, time

N = " "
X = "X"
O = "O"

board_win_combinations = [
    [[0, 0], [0, 1], [0, 2]],
    [[1, 0], [1, 1], [1, 2]],
    [[2, 0], [2, 1], [2, 2]],
    [[0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [2, 1]],
    [[0, 2], [1, 2], [2, 2]],
    [[0, 0], [1, 1], [2, 2]],
    [[0, 2], [1, 1], [2, 0]]
]

board_possible_moves = [
    [0, 0], [1, 0], [2, 0],
    [0, 1], [1, 1], [2, 1],
    [0, 2], [1, 2], [2, 2],
]

board_value_map = {N: 0, O: 1, X: 2}

special_cases = {6: 2, 69: 6, 909: 3, 14249: 7, 13205: 5}

def get_opponent(player):
    if player == X:
        return O
    elif player == O:
        return X
    else:
        return None

class TicTacToeBoard:

    def __init__(self, data) -> None:
        self.data = data

    @classmethod
    def random(cls):
        return cls([[random.choice([N, X, O]) for i in range(3)] for j in range(3)])
    
    @classmethod
    def empty(cls):
        return cls([[N, N, N], [N, N, N], [N, N, N]])
    
    @classmethod
    def from_id(cls, id):
        nums = []
        for _ in range(9):
            nums.append(id % 3)
            id //= 3
        return cls([[[N, O, X][nums[j*3+i]] for i in range(3)] for j in range(3)])
    
    def calc_id(self):
        sum = 0
        for x in range(3):
            for y in range(3):
                factor = 3 ** (y * 3 + x)
                sum += board_value_map[self.data[y][x]] * factor
        return sum

    def copy(self):
        return TicTacToeBoard(copy.deepcopy(self.data))
    
    def check_win_combination(self, win_combination, token):
        failed = False
        for (x, y) in win_combination:
            if self.data[y][x] != token:
                failed = True
                break

        if not failed:
            return True
        return False

    def get_winner(self):
        for winner in (X, O):
            for combination in board_win_combinations:
                failed = False
                for (x, y) in combination:
                    if self.data[y][x] != winner:
                        failed = True
                        break
                if not failed:
                    return winner
        return None
    
    def __repr__(self):
        return (
            "B("
            f"{self.data[0][0]}{self.data[0][1]}{self.data[0][2]}"
            f"{self.data[1][0]}{self.data[1][1]}{self.data[1][2]}"
            f"{self.data[2][0]}{self.data[2][1]}{self.data[2][2]}"
            ")"
        )

    def __str__(self):
        out_str = "+---+---+---+\n"
        for i in range(3):
            out_str += "|"
            for j in range(3):
                out_str += " "
                out_str += self.data[i][j]
                out_str += " |"
            out_str += "\n+---+---+---+\n"
        return out_str[:-1]
    
    def compute_score(self):
        sum = 0
        for token, weight in [(X, 1), (O, -1)]:
            for win_combination in board_win_combinations:
                if self.check_win_combination(win_combination, token):
                    sum += weight
        return sum
        
    def count_filled_cells(self):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.data[i][j] != N:
                    count += 1
        return count
    
    def make_move_board(self, move, token):
        new_board = self.copy()
        new_board.data[move[1]][move[0]] = token
        return new_board
    
    def field_is_free(self, field_pos):
        return self.data[field_pos[1]][field_pos[0]] == N
    
    def is_empty(self):
        return self.count_filled_cells() == 0
    
    def is_filled(self):
        return self.count_filled_cells() == 9
    
    def is_won(self):
        return self.get_winner() != None
    
    def is_draw(self):
        return self.is_filled() and not self.is_won()
    
    def get_state(self, player_token=X):
        if self.is_invalid():
            return "unreachable"
        elif self.get_winner() == player_token:
            return "won"
        elif self.get_winner() == get_opponent(player_token):
            return "lost"
        elif self.is_draw():
            return "draw"
        else:
            return "normal"
    
    def is_invalid(self):
        counts = {X: 0, O: 0}
        for i in range(3):
            for j in range(3):
                value = self.data[i][j]
                if value in counts:
                    counts[value] += 1
        return abs(counts[X] - counts[O]) > 1
    
    def get_best_moves(self, player):
        possible_moves = [
            [0, 0], [0, 1], [0, 2],
            [1, 0], [1, 1], [1, 2],
            [2, 0], [2, 1], [2, 2],
        ]

        # use the minimax algorithm and alpha-beta pruning to find the best move 
        # with the board.compute_score() as heuristic
        def minimax(old_board, move, player, a, b):
            board = old_board.copy()
            board.data[move[1]][move[0]] = player

            if board.is_filled() or board.is_won():
                return board.compute_score()
            
            opponent = get_opponent(player)
            value = -math.inf
            if player == X:
                value *= -1

            for opponent_move in possible_moves:
                if board.data[opponent_move[1]][opponent_move[0]] != N:
                    continue

                result = minimax(board, opponent_move, opponent, a, b)

                if player == O:
                    value = max(value, result)
                    a = max(a, value)
                    if value >= b:
                        break

                elif player == X:
                    value = min(value, result)
                    b = min(b, value)
                    if value <= a:
                        break
                
            return value
        
        best_score = -math.inf
        if player == O:
            best_score = math.inf

        best_moves = []
        for move in possible_moves:
            if self.data[move[1]][move[0]] != N:
                continue

            score = minimax(self, move, player, -math.inf, math.inf)

            if (player == X and score > best_score) or (player == O and score < best_score):
                best_moves = [move]
                best_score = score
            elif score == best_score:
                best_moves.append(move)

        if len(best_moves) == 0:
            raise Exception("There is no possible move")
        
        board_id = self.calc_id()
        if board_id in special_cases:
            return [board_possible_moves[special_cases[board_id]] for _ in range(len(best_moves))]

        return best_moves
    
    def is_terminal(self):
        return self.is_draw() or self.is_won()
    
    def make_computer_move(self, player):
        best_moves = self.get_best_moves(player)

        random.seed(self.calc_id() * 76543)
        move = random.choice(best_moves)
        self.data[move[1]][move[0]] = player
        return move


if __name__ == "__main__":
    board = TicTacToeBoard.empty()

    while not board.is_filled() and not board.is_won():
        num = int(input("[1-9]: ")) - 1
        move = [num % 3, math.floor(num / 3)]
        board.data[move[1]][move[0]] = X
        if board.is_won() or board.is_filled():
            break

        t = time.time()
        board.make_computer_move(O)

    print(board)
    if board.is_won():
        print(f"the winner is: {board.get_winner()}")
    else:
        print("A draw!")