import copy
import sys
from variables import Variables
import queue



NUMS = "123456789"
HOR_DELIMITER = "-"
VER_DELIMITER = "|"
ABC = 'ABCDEFGHI'



class CSP:

    def __init__(self, filename):

        # Assigning labels to each value in the elements array
        # Creating the set array
        self.elements = []

        for row in ABC:
            for column in NUMS:
                self.elements.append(row + column)

        self.zone = dict(
            (self.elements[j], NUMS if filename[j] == '0' else filename[j]) for j in range(len(filename)))

        # Storing the column constraints into x
        col_cstr = []
        # Storing row constraints into y
        row_cstr = []
        # Storing 3x3 block constraints into z
        block_cstr = []

        # Runs through the row, column, and block constraint arcs and stores them in the arrays
        for i in range(9):
            col_cstr.append(self.column_neighbor_arc(self.elements, i))

        for i in range(9):
            row_cstr.append(self.row_neighbor_arc(self.elements, i))

        for r in range(9):
            for c in range(9):
                block_cstr.append(self.block_neighbor_arc(self.elements, r, c))

        box_constraints = col_cstr + row_cstr + block_cstr
        self.constraints_box = (box_constraints)

        self.element_adjacent = dict(
            (c, [w for w in self.constraints_box if c in w])
            for c in self.elements)

        self.adjacent = dict(
            (c, set(sum(self.element_adjacent[c], [])) - set([c]))
            for c in self.elements)

        self.arc_consistency = set()
        for element in self.elements:
            for adjacent in self.adjacent[element]:
                self.arc_consistency.add((element,adjacent))

    # Stores all column values and their neighbours inside the neighbors array

    def column_neighbor_arc(self, y, c):

        column_arc = []

        for i in range(c, len(y), 9):
            column_arc.append(y[i])

        return column_arc

    # stores all row values and their neighbours inside the neighbors array

    def row_neighbor_arc(self, y, r):

        row_arc = []

        last = (r + 1) * 9
        begin = last - 9

        for k in range(begin, last, 1):
            row_arc.append(y[k])

        return row_arc

    # stores values in 3x3 blocks into neighbors array
    def block_neighbor_arc(self, y, r, c):

        block_constraint = []

        # Calculating the column domain
        col_domain = c - c % 3
        # Calculating the row domain
        row_domain = r - r % 3

        for cl in range(3):
            for rw in range(3):
                arr = y[(cl + col_domain) + (rw + row_domain) * 9]
                block_constraint.append(arr)

        return block_constraint

    # Helper function which checks to see if the puzzle is solved
    def check_solve(self):
        is_solved = True
        for ele in self.elements:
            if len(self.zone[ele]) > 1:
                is_solved = False
                break
        return is_solved

    # Prints the solution of the sudoku puzzle
    def sudoku_output(self, values):

        print("Solution:")
        thread = ""
        a = ""
        sum = 0

        for x in self.elements:
            if values != False:
                a += str(values[x])

        for k in range(9):

            if (k % 3 == 0):
                print("{:-^12s}".format(HOR_DELIMITER))

            for l in range(9):

                if (l % 3) == 0:
                    thread += VER_DELIMITER

                thread += a[sum]
                sum += 1
            print(thread + VER_DELIMITER)
            thread = ''
            
        print("{:-^12s}".format(HOR_DELIMITER))

    # Checks arc consistency to make sure it's maintained
    def constraint_consistency(self, task, ele, res):

        consistent = True

        for n in self.adjacent[ele]:

            if n in task.keys() and task[n] == res:
                consistent = False
        
        return consistent
