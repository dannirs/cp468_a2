import copy
import sys
import queue
from variables import Variables


NUMS = "123456789"
HOR_DELIMITER = "-"
VER_DELIMITER = "|"


class CSP:

    def __init__(self, filename):

        self.elements = [
            row + column for row in 'ABCDEFGHI' for column in '123456789']

        self.domain = dict(
            (self.elements[i], NUMS if filename[i] == '0' else filename[i]) for i in range(len(filename)))

        x = [self.column_neighbor_arc(self.elements, i)
             for i in range(9)]

        y = [self.row_neighbor_arc(self.elements, i)
             for i in range(9)]

        z = [self.blockNeighbors(self.elements, i, j)
             for i in range(9) for j in range(9)]

        self.box = (x + y + z)

        self.cellNeighbors = dict(
            (s, [u for u in self.box if s in u])
            for s in self.elements)

        self.neighbors = dict(
            (s, set(sum(self.cellNeighbors[s], [])) - set([s]))
            for s in self.elements)

        self.constraints = {(variable, neighbor)
                            for variable in self.elements for neighbor in self.neighbors[variable]}

    # Creates columns, appends to neighbors array

    def column_neighbor_arc(self, y, col):
        neighbors = []
        for i in range(col, len(y), 9):
            neighbors.append(y[i])

        return neighbors

    # Creates rows, appends to neighbors array

    def row_neighbor_arc(self, y, row):
        neighbors = []
        end = (row + 1) * 9
        start = end - 9
        for i in range(start, end, 1):
            neighbors.append(y[i])

        return neighbors

    # Creates the 3x3 block and stores it in the neighbours array
    def blockNeighbors(self, y, row, col):
        neighbors = []
        domRow = row - row % 3
        domCol = col - col % 3
        for j in range(3):
            for i in range(3):
                v = y[(j + domCol) + (i + domRow) * 9]
                neighbors.append(v)

        return neighbors

    # Checks if the puzzle is check_solve
    def check_solve(self):
        is_solved = True
        for v in self.elements:
            if len(self.domain[v]) > 1:
                is_solved = False
                break
        return is_solved

    # Prints the sudoku puzzle
    def sudoku_output(self, values):
        print("SUDOKU:")
        line = ""
        sum = 0
        domain = ""

        for var in self.elements:
            #if len(values[var]) > 1:
            #    domain += '0'
            #if values != False:
            #else:
            if values != False:
                domain += str(values[var])

        for i in range(9):
            if (i % 3 == 0):
                print("{:-^12s}".format(HOR_DELIMITER))

            for j in range(9):
                if (j % 3) == 0:
                    line += VER_DELIMITER

                line += domain[sum]
                sum += 1

            print(line + VER_DELIMITER)
            line = ''
        print("{:-^12s}".format(HOR_DELIMITER))

    # Checks arc consistency, compares to see if value is already in the constraint
    def arc_consistent(self, assignment, var, val):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment.keys() and assignment[neighbor] == val:
                return False

        return True
