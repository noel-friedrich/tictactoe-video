from board_generator import all_boards, ShowBoard
from board_generator import PLAYER_TOKEN, COMPUTER_TOKEN
from PIL import Image, ImageFont, ImageDraw, ImageColor
from board import TicTacToeBoard, X, O, N, board_win_combinations, board_possible_moves
import random

from midiutil.MidiFile import MIDIFile

mf = MIDIFile(3) # num tracks
x_track = 0
o_track = 1
boom_track = 2

time = 0

mf.addTrackName(x_track, time, "X Track")
mf.addTempo(x_track, time, 120)

mf.addTrackName(o_track, time, "O Track")
mf.addTempo(o_track, time, 120)

mf.addTrackName(boom_track, time, "Boom Track")
mf.addTempo(boom_track, time, 120)

channel = 0
volume = 100

for i, show_board in enumerate(all_boards):
    board_time = i * 2
    duration = 2 / len(board_possible_moves)
    board = show_board.board

    mf.addNote(boom_track, 1, 50, board_time, duration, volume)
    
    for j, move in enumerate(board_possible_moves):
        if not board.field_is_free(move):
            token = board.data[move[1]][move[0]]
            time = board_time + j / len(board_possible_moves) * 2

            pitch = 55 + j

            if token == X:
                mf.addNote(x_track, 2, pitch, time, duration, volume)
            elif token == O:
                mf.addNote(o_track, 3, pitch, time, duration, volume)

with open("outputs/music/output.mid", 'wb') as outf:
    mf.writeFile(outf)