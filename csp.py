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
        self.elements = []

        for row in ABC:
            for column in NUMS:
                self.elements.append(row + column)

        self.domain = dict(
            (self.elements[i], NUMS if filename[i] == '0' else filename[i]) for i in range(len(filename)))

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
            (s, [u for u in self.constraints_box if s in u])
            for s in self.elements)

        self.adjacent = dict(
            (s, set(sum(self.element_adjacent[s], [])) - set([s]))
            for s in self.elements)

        self.arc_consistency = set()
        for variable in self.elements:
            for neighbor in self.adjacent[variable]:
                self.arc_consistency.add((variable,neighbor))

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
            if len(self.domain[ele]) > 1:
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
            #if len(values[var]) > 1:
            #    domain += '0'
            #if values != False:
            #else:
            if values != False:
                a += str(values[x])

        for i in range(9):

            if (i % 3 == 0):
                print("{:-^12s}".format(HOR_DELIMITER))

            for j in range(9):

                if (j % 3) == 0:
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
