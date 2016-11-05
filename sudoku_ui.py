import argparse
import sudoku_solver

from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT, X, Y

BOARDS = ['debug', 'debug2', 'n00b', 'l33t', 'error']  # Available sudoku boards
DEGREES = [2, 3]
SOLVER = ['bruteforce', 'backtrack', 'bnb']
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
SUDOKU_DEGREE = 3
SUDOKU_SIDE = SUDOKU_DEGREE * SUDOKU_DEGREE
WIDTH = HEIGHT = MARGIN * 2 + SIDE * SUDOKU_SIDE  # Width and height of the whole board


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


def parse_arguments():
    """
    Parses arguments of the form:
        sudoku_ui_old.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help="Desired board name",
                            type=str,
                            choices=BOARDS,
                            required=True)
    arg_parser.add_argument("--degree",
                            type=int,
                            help="Sudoku degree, e.g: 3 for 9x9",
                            choices=DEGREES,
                            required=False
                            )
    arg_parser.add_argument("--solver",
                            type=str,
                            help="Choosen solver",
                            choices=SOLVER,
                            required=False
                            )

    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())
    global SUDOKU_DEGREE, SUDOKU_SIDE, WIDTH, HEIGHT
    if args['degree']== 2:
        SUDOKU_DEGREE = args['degree']
    SUDOKU_SIDE = SUDOKU_DEGREE * SUDOKU_DEGREE
    WIDTH = HEIGHT = MARGIN * 2 + SIDE * SUDOKU_SIDE
    return args['board'],args['solver']


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1
        self.__init_ui()

    def __init_ui(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.bottom = Frame(self)
        self.bottom.pack(side=BOTTOM)
        clear_button = Button(self.bottom,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=LEFT)

        solve_button = Button(self.bottom,
                              text="Solve",
                              command=self.__solve)
        solve_button.pack(fill=BOTH, side=RIGHT)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __solve(self):
        solved,self.game.puzzle = self.game.solve()
        if solved:
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            self.game.check_win()
        else:
            self.__draw_invalid()

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into n^2xn^2 squares
        """
        for i in xrange(SUDOKU_SIDE + 1):
            color = "blue" if i % SUDOKU_DEGREE == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in xrange(SUDOKU_SIDE):
            for j in xrange(SUDOKU_SIDE):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * (float(SUDOKU_SIDE) / 2 - 2)
        x1 = y1 = MARGIN + SIDE * (float(SUDOKU_SIDE) / 2 + 2)
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + (float(SUDOKU_SIDE) / 2) * SIDE
        self.canvas.create_text(
            x, y,
            text="Solved!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __draw_invalid(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * (float(SUDOKU_SIDE) / 2 - 2)
        x1 = y1 = MARGIN + SIDE * (float(SUDOKU_SIDE) / 2 + 2)
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark red", outline="red"
        )
        # create text
        x = y = MARGIN + (float(SUDOKU_SIDE) / 2) * SIDE
        self.canvas.create_text(
            x, y,
            text="Invalid\nPuzzle!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __draw_wrong(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * (float(SUDOKU_SIDE) / 2 - 2)
        x1 = y1 = MARGIN + SIDE * (float(SUDOKU_SIDE) / 2 + 2)
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark red", outline="red"
        )
        # create text
        x = y = MARGIN + (float(SUDOKU_SIDE) / 2) * SIDE
        self.canvas.create_text(
            x, y,
            text="Wrong\nMove!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.start_puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()


class SudokuBoard(object):
    """
    Sudoku Board representation
    """

    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != SUDOKU_SIDE:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be " + `SUDOKU_SIDE` + "  chars long."
                )
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-" + `SUDOKU_SIDE`
                    )
                board[-1].append(int(c))

        if len(board) != SUDOKU_SIDE:
            raise SudokuError("Each sudoku puzzle must be " + `SUDOKU_SIDE` + " lines long")
        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """

    def __init__(self, board_file, solver_name):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board
        self.game_over = False
        self.puzzle = []
        self.solver_name = solver_name


    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in xrange(SUDOKU_SIDE):
            self.puzzle.append([])
            for j in xrange(SUDOKU_SIDE):
                val = self.start_puzzle[i][j]
                self.puzzle[i].append(val)

    def check_win(self):
        for row in xrange(SUDOKU_SIDE):
            if not self.__check_row(row):
                return False
        for column in xrange(SUDOKU_SIDE):
            if not self.__check_column(column):
                return False
        for row in xrange(SUDOKU_DEGREE):
            for column in xrange(SUDOKU_DEGREE):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, SUDOKU_SIDE + 1))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in xrange(SUDOKU_SIDE)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in xrange(row * SUDOKU_DEGREE, (row + 1) * SUDOKU_DEGREE)
                for c in xrange(column * SUDOKU_DEGREE, (column + 1) * SUDOKU_DEGREE)
                ]
        )

    def solve(self):
        solver = sudoku_solver.Backtrack(self.start_puzzle)
        if self.solver_name == 'bnb':
            solver = sudoku_solver.BranchAndBound(self.start_puzzle)
        elif self.solver_name == 'bruteforce':
            solver = sudoku_solver.BruteForce(self.start_puzzle)
        return solver.solve()


if __name__ == '__main__':
    board_name, solver_name = parse_arguments()

    with open('%s.sudoku' % board_name, 'r') as boards_file:

        game = SudokuGame(boards_file, solver_name)
        game.start()

        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        root.mainloop()
