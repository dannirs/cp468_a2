'''
Created on 2020 M11 4

@author: Danni
'''
from csp import CSP
col = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
row = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


class sudoku:

    def __init__(self):
        self.cells = dict()
        self.empty = []

    def make_board(self, filepath):
        board = []

        with open(filepath) as fp:
            line = fp.readline()
            while line:
                values = line.split(' ')
                values.pop()
                board.append(values)
                line = fp.readline()

        for i in range(len(board)):
            for j in range(len(board)):
                if int(board[i][j]) == 0:
                    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                else:
                    domain = [int(board[i][j])]
                self.cells[col[j] + row[i]] = domain
        print(self.cells)
        print()

        return

    def print_board(self):
        count = 0
        rows = 0
        for key, item in self.cells.items():
            # print(item)
            # print(len(item))
            if count % 9 == 0:
                print()
                rows += 1
                if rows == 4 or rows == 7 or rows == 10:
                    print("----------------------", end="")
                    print()
            elif count % 3 == 0:
                print("|", end=" ")
            if len(item) == 1:
                print(*item, end=" ")
            else:
                print(0, end=" ")
            count += 1

    def find_empty(self):
        for key, item in self.cells.items():
            if len(item) > 1:
                self.empty.append(key)

        print("Empty:")
        print(self.empty)
        # for i in self.empty:
        #    print(i)

        return

    def mrv(self):

        cell = None
        smallest = len(col) + 1
        for key, item in self.cells.items():
            if len(item) != 1 and len(item) < smallest:
                smallest = len(item)
                cell = key

        if (cell == None):
            return None
        else:
            return cell

    def filled(self):
        for key, item in self.cells.items():
            if len(item) > 1:
                return False
        return True


sudoku = sudoku()
filepath = 'sudoku_input.txt'
board = sudoku.make_board(filepath)
sudoku.print_board()
print()
print()
sudoku.find_empty()
cell = sudoku.mrv()
print("Minimum remaining value:", cell)
filled = sudoku.filled()
print("All cells filled:", filled)
