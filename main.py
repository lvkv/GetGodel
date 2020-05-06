import random
import enum
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QMessageBox


class Direction(enum.Enum):
    """
    The value of each direction is the number of 90° clockwise board rotations needed to make swiping in <Direction>
    equivalent to to swiping Left.
    """
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3


def rotate_list_right(x):
    """Returns list x but rotated 90° clockwise. I didn't write this. To be honest, it's an abomination."""
    return [list(r) for r in zip(*x[::-1])]


class Board:
    """
    A representation of the game's state (aka the board!).
    Supports rectangular, not just square, boards.
    """

    def __init__(self, height, width):
        self.board = [[None] * width for i in range(height)]  # None corresponds to an empty tile

    def insert_tile(self, val, ri, ci):
        """Change the value of the tile located at coordinates (ri, ci) to val"""
        self.board[ri][ci] = val

    def insert_random_tile(self):
        """Inserts a 2 (Church) or 4 (Turing) into a random empty tile. Returns False if no empty tiles exist."""
        rand_val = random.choice([2, 4])
        empty_tiles = []
        for ri, row in enumerate(self.board):
            for ci, item in enumerate(row):
                if item is None:
                    empty_tiles.append((ri, ci))
        if len(empty_tiles) > 0:
            rand_row, rand_col = random.choice(empty_tiles)
            self.insert_tile(rand_val, rand_row, rand_col)
            return True
        return False

    def shift(self, direction):
        """
        Update the state of the board to that after swiping in Direction direction.
        Returns True if shifting changed the state of the board, False if it didn't.
        """
        rotations_needed = direction.value  # This problem can actually be solved in a general way
        board_rotated = self.board.copy()
        for i in range(rotations_needed):  # We just need to rotate the board based on the direction
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
        for i in range(4 - rotations_needed):  # Un-rotate the board after we're done
            board_rotated = rotate_list_right(board_rotated)
        something_changed = self.board != board_rotated
        self.board = board_rotated
        return something_changed


class App(QWidget):
    """Represents the GUI and drives the game."""

    key_mappings = {  # Maps keyboard codes to directions
        87: Direction.UP,  # 'W'
        83: Direction.DOWN,  # 'A'
        65: Direction.LEFT,  # 'S'
        68: Direction.RIGHT  # 'D'
    }

    number_mappings = {  # Maps tile values to images of logicians and philosophers
        None: 'images/empty.jpg',
        2: 'images/church.jpg',
        4: 'images/turing.jpg',  # Church-Turing hypothesis
        8: 'images/frege.jpg',
        16: 'images/russell.jpg',  # Frege's theorem and Russell's paradox
        32: 'images/post.jpg',
        64: 'images/quine.jpg',  # Our 'Post and Quine' puzzles
        128: 'images/curry.jpg',
        256: 'images/hilbert.jpg',  # Obligatory Hilbert for Mei Rose
        512: 'images/tarski.jpg',
        1024: 'images/montague.jpg',
        2048: 'images/goedel.jpg',  # The game is 'incomplete' until you get to Godel :)
    }

    def __init__(self):
        super().__init__()
        self.board = Board(4, 4)
        self.title = 'Get Godel'
        self.grid = None
        self.window_text = None
        self.init_ui()

    def init_ui(self):
        """Initializes the window with a layout and a grid"""
        self.setWindowTitle(self.title)
        window_layout = QVBoxLayout()
        self.window_text = QLabel('Use the W, A, S, D keys to combine logicians. Get to Godel!')
        window_layout.addWidget(self.window_text)
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
        self.board.insert_random_tile()
        self.update_board_gui()

    def check_for_win(self):
        for row in self.board.board:
            for item in row:
                if item == 2048:
                    self.window_text.setText('You got to Godel!')
                    App.key_mappings = {}  # Big brain way of stopping the game

    def lose(self):
        self.window_text.setText('Oh no, you lost! Restart the app to try again.')

    def keyPressEvent(self, event):
        """Triggered when a key is pressed. Advances the game if the pressed key has a mapping"""
        key = event.key()
        if key in App.key_mappings:
            self.board.shift(App.key_mappings[key])
            tile_inserted = self.board.insert_random_tile()
            self.update_board_gui()
            if not tile_inserted:  # If there's no more space to insert tiles, the player has lost
                self.lose()
            self.check_for_win()

    def update_board_gui(self):
        """Updates the GUI to reflect the state of the game."""
        board = self.board.board
        for row_index, row in enumerate(board):
            for col_index in range(len(row)):
                tile_widget = self.grid.itemAtPosition(row_index, col_index).widget()
                tile_widget.setPixmap(QPixmap(App.number_mappings[board[row_index][col_index]]))


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
