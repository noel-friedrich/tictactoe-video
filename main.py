from board_generator import all_boards, ShowBoard
from board_generator import PLAYER_TOKEN, COMPUTER_TOKEN
from PIL import Image, ImageFont, ImageDraw, ImageColor
from board import TicTacToeBoard, X, O, N, board_win_combinations
import random

# defining useful constants for later use

VIDEO_RESOLUTION = (1920, 1080)
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "outputs"

FIRST_BOARD_REPEATS = 20

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
BOARD_FONT_SIZE = 70
BOARD_FONT_Y_OFFSET = -5

INTRO_OFFSET_SECONDS = 25

ID_FONT_FILE = r"c:\WINDOWS\Fonts\CASCADIACODE.TTF"
ID_FONT_SIZE = 160

ID_POSITION = [1477, 198]
ID_FONT_Y_OFFSET = -17

MAX_BOARD_ID = 3 ** 9 - 1

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
board_font = ImageFont.truetype(ID_FONT_FILE, BOARD_FONT_SIZE) 

def make_img(show_board: ShowBoard, name="auto", save=True):
    output_img = Image.new(mode="RGB", size=VIDEO_RESOLUTION)
    output_draw = ImageDraw.Draw(output_img)

    board = show_board.board

    def place_text(x, y, text):
        center_x, center_y = FIELD_POSITIONS[y][x]
        _, _, w, h = output_draw.textbbox((0, 0), text, font=board_font)
        output_draw.text((
            center_x - w // 2,
            center_y - h // 2 + BOARD_FONT_Y_OFFSET
        ), text, font=board_font, align="center", fill="black") 

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

    def draw_board():
        for x in range(3):
            for y in range(3):
                move_id = y * 3 + x
                token = board.data[y][x]
                if token == N:
                    if not board.is_terminal():
                        child = show_board.move_children_map[move_id]
                        place_text(x, y, f"{child.time(INTRO_OFFSET_SECONDS)}")
                else:
                    img = img_map[token]
                    place_token(x, y, img)
                
        for marked_move in show_board.marked_moves:
            token_img = img_map[show_board.board.data[marked_move[1]][marked_move[0]]]
            place_token(marked_move[0], marked_move[1],
                        token_img, True)

    def draw_win_lines():
        for token in (X, O):
            for i, combination in enumerate(board_win_combinations):
                if board.check_win_combination(combination, token):
                    p1, p2 = BOARD_WIN_LINES[i]
                    color = {X: "blue", O: "red"}[token]
                    output_draw.line(p1 + p2, fill=color, width=20)

    def draw_id():
        text = show_board.time(INTRO_OFFSET_SECONDS)
        _, _, w, h = output_draw.textbbox((0, 0), text, font=id_font)
        output_draw.text((
            ID_POSITION[0] - w // 2,
            ID_POSITION[1] - h // 2 + ID_FONT_Y_OFFSET
        ), text, font=id_font, align="center", fill="black") 
    
    game_state = board.get_state()
    background_img = background_images[game_state]
    output_img.paste(background_img)
    state_counts[game_state] += 1

    draw_board()
    draw_win_lines()
    draw_id()

    if save:
        file_name = name if name != "auto" else f"{(show_board.idx + FIRST_BOARD_REPEATS):0>5}"
        output_img.save(f"{OUTPUT_DIR}/boards/{file_name}.jpg")

for i in range(FIRST_BOARD_REPEATS):
    make_img(all_boards[0], f"{i:0>5}")
for i, show_board in enumerate(all_boards):
    make_img(show_board)
    print(f"{i}/{len(all_boards)}")