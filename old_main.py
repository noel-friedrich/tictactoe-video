from board import TicTacToeBoard, X, O, N, board_win_combinations
import random
from PIL import Image, ImageFont, ImageDraw, ImageColor

VIDEO_RESOLUTION = (1920, 1080)
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "outputs"

FIELD_POSITIONS = [
    [[260, 235], [564, 235], [869, 235]],
    [[260, 540], [564, 540], [869, 540]],
    [[260, 845], [564, 845], [869, 845]]
]

BOARD_WIN_LINES = [
    [[261, 84], [261, 996]],
    [[567, 84], [567, 996]],
    [[869, 84], [869, 996]],
    [[108, 235], [1020, 235]],
    [[108, 540], [1020, 540]],
    [[108, 845], [1020, 845]],
    [[108, 84], [1020, 995]],
    [[1020, 84], [108, 995]],
]

TOKEN_SIZE = 220
SQUARE_SIZE = 284

ID_FONT_FILE = r"c:\WINDOWS\Fonts\CASCADIACODE.TTF"
ID_FONT_SIZE = 160
ID_POSITION = [1477, 198]
ID_FONT_Y_OFFSET = -17

MAX_BOARD_ID = 3 ** 9 - 1

COMPUTER_TOKEN = O

background_images = {
    "normal": Image.open(f"{TEMPLATES_DIR}/background.jpg"),
    "won": Image.open(f"{TEMPLATES_DIR}/background-won.jpg"),
    "lost": Image.open(f"{TEMPLATES_DIR}/background-lost.jpg"),
    "draw": Image.open(f"{TEMPLATES_DIR}/background-draw.jpg"),
    "unreachable": Image.open(f"{TEMPLATES_DIR}/background-unreachable-position.jpg")
}

state_counts = {
    "normal": 0,
    "won": 0,
    "lost": 0,
    "draw": 0,
    "unreachable": 0,
}

# final state: {'normal': 2498, 'won': 1266, 'lost': 2980, 'draw': 112, 'unreachable': 12826}

o_img = Image.open(f"{TEMPLATES_DIR}/o.png")
x_img = Image.open(f"{TEMPLATES_DIR}/x.png")

o_img = o_img.resize((TOKEN_SIZE, TOKEN_SIZE)).convert("RGBA")
x_img = x_img.resize((TOKEN_SIZE, TOKEN_SIZE)).convert("RGBA")

img_map = {O: o_img, X: x_img}

id_font = ImageFont.truetype(ID_FONT_FILE, ID_FONT_SIZE) 

def make_img(board: TicTacToeBoard, name="auto", save=True):
    output_img = Image.new(mode="RGB", size=VIDEO_RESOLUTION)
    output_draw = ImageDraw.Draw(output_img)

    def place_token(x, y, img, mark=False):
        center_x, center_y = FIELD_POSITIONS[y][x]

        if mark:
            top_left = (
                center_x - SQUARE_SIZE // 2,
                center_y - SQUARE_SIZE // 2
            )
            bottom_right = (
                center_x + SQUARE_SIZE // 2,
                center_y + SQUARE_SIZE // 2
            )
            output_draw.rectangle((top_left, bottom_right),
                fill="#FFFFD1")

        output_img.paste(img, (
            center_x - TOKEN_SIZE // 2,
            center_y - TOKEN_SIZE // 2
        ), img)

    def draw_board(board):
        for x in range(3):
            for y in range(3):
                token = board.data[y][x]
                if token == N:
                    continue
                img = img_map[token]
                place_token(x, y, img)

    board_id = board.calc_id()
    og_board = board.copy()

    background_img = None

    computer_move = None

    if board.get_state() == "normal":
        try:
            best_move = board.get_best_moves(COMPUTER_TOKEN)
            computer_move = random.choice(best_move)
            move_x, move_y = computer_move
            board.data[move_y][move_x] = COMPUTER_TOKEN
        except Exception as e:
            print(f"-- Error at board#{board.calc_id()} --\n{board}\nErrorMsg: {e}")
            exit()

    new_game_state = board.get_state()

    background_img = background_images[new_game_state]
    output_img.paste(background_img)

    if new_game_state == "unreachable":
        # reverse the executed computer move
        board = og_board
        computer_move = None

    state_counts[new_game_state] += 1

    draw_board(board)
    
    if computer_move:
        computer_img = img_map[COMPUTER_TOKEN]
        place_token(computer_move[0], computer_move[1],
                    computer_img, True)

    def draw_win_lines():
        for token in (X, O):
            for i, combination in enumerate(board_win_combinations):
                if board.check_win_combination(combination, token):
                    p1, p2 = BOARD_WIN_LINES[i]
                    color = {X: "blue", O: "red"}[token]
                    output_draw.line(p1 + p2, fill=color, width=20)

    def draw_id():
        text = f"{board_id:0>5}"
        _, _, w, h = output_draw.textbbox((0, 0), text, font=id_font)
        output_draw.text((
            ID_POSITION[0] - w // 2,
            ID_POSITION[1] - h // 2 + ID_FONT_Y_OFFSET
        ), text, font=id_font, align="center", fill="black") 
    
    draw_win_lines()
    draw_id()

    if save:
        file_name = name if name != "auto" else f"{board_id:0>5}"
        output_img.save(f"{OUTPUT_DIR}/boards/{file_name}.jpg")

random.seed(42)
for i in range(3 ** 9):
    board = TicTacToeBoard.from_id(i)
    make_img(board)
    
    if (i % 50 == 0):
        print(f"{i} ({round(i / MAX_BOARD_ID * 100, 2)}%)")