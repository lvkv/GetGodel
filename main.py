import random
import enum
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel


class Direction(enum.Enum):
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3


def rotate_list_right(board):
    return [list(r) for r in zip(*board[::-1])]


class Board:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.board = [[None] * w for i in range(h)]

    def insert_tile(self, val, ri, ci):
        self.board[ri][ci] = val

    def insert_random_tile(self):
        rand_val = random.choice([2, 4])
        empty_tiles = []
        for ri, row in enumerate(self.board):
            for ci, item in enumerate(row):
                if item is None:
                    empty_tiles.append((ri, ci))
        if len(empty_tiles) > 0:
            rand_row, rand_col = random.choice(empty_tiles)
            self.insert_tile(rand_val, rand_row, rand_col)
            return rand_row, rand_col
        return None

    def shift(self, direction):
        rotations_needed = direction.value
        board_rotated = self.board
        for i in range(rotations_needed):
            board_rotated = rotate_list_right(board_rotated)
        for row_index, row in enumerate(board_rotated):
            prev_val = None
            prev_index = None
            for col_index, value in enumerate(row):
                if value == prev_val and value is not None:
                    board_rotated[row_index][prev_index] += value
                    board_rotated[row_index][col_index] = None
                    prev_val = None
                    prev_index = None
                elif value is not None:
                    prev_val = value
                    prev_index = col_index
            len_w_none = len(row)
            new_row = [x for x in board_rotated[row_index] if x is not None]
            len_wo_none = len(new_row)
            for i in range(len_w_none - len_wo_none):
                new_row.append(None)
            board_rotated[row_index] = new_row
        for i in range(4 - rotations_needed):
            board_rotated = rotate_list_right(board_rotated)
        self.board = board_rotated

    def display(self):
        for row in self.board:
            for item in row:
                if item is None:
                    item = 0
                print(f'{item}\t\t', end='')
            print()


class App(QWidget):
    key_mappings = {87: Direction.UP, 83: Direction.DOWN, 65: Direction.LEFT, 68: Direction.RIGHT}
    number_mappings = {
        None: 'images/empty.jpg',
        2: 'images/church.jpg',
        4: 'images/turing.jpg',
        8: 'images/frege.jpg',
        16: 'images/russell.jpg',
        32: 'images/post.jpg',
        64: 'images/quine.jpg',
        128: 'images/curry.jpg',
        256: 'images/hilbert.jpg',
        512: 'images/tarski.jpg',
        1024: 'images/montague.jpg',
        2048: 'images/goedel.jpg',
    }

    def __init__(self):
        super().__init__()
        board_side_len = 4
        board = Board(board_side_len, board_side_len)
        self.board = board
        self.title = 'Get Godel'
        self.grid = None
        self.waiting = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        window_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        for row_index, row in enumerate(self.board.board):
            for col_index in range(len(row)):
                label = QLabel(self)
                label.setPixmap(QPixmap(App.number_mappings[None]))
                grid_layout.addWidget(label, row_index, col_index)
        window_layout.addLayout(grid_layout)
        self.grid = grid_layout
        self.setLayout(window_layout)
        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        if key in App.key_mappings:
            self.board.shift(App.key_mappings[key])
            self.board.insert_random_tile()
            self.update_board_gui()

    def update_board_gui(self):
        board = self.board.board
        for row_index, row in enumerate(board):
            for col_index in range(len(row)):
                tile_widget = self.grid.itemAtPosition(row_index, col_index).widget()
                tile_widget.setPixmap(QPixmap(App.number_mappings[board[row_index][col_index]]))
                # tile_widget.setText(str(board[row_index][col_index]))


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
