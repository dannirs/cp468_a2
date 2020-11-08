import copy
import sys
import queue

NUMS = "123456789"
HOR_DELIMITER = "-"
VER_DELIMITER = "|"


class Variables:
    def __init__(self, row, col, value):
        self.row = row
        self. col = col
        self.value = value
        #self.assigned_value = None
        #self.cur_dom = [True] * len(csp.domain)

    # def is_assigned(self):
    #    return self.assignedValue != None

    # def assign(self, value):

    #   if self.is_assigned() or not self.in_cur_domain(value):
    #        print("ERROR: trying to assign variable", self,
    #              "that is already assigned or illegal value (not in curdom)")
    #        return

    #    self.assignedValue = value

    # def unassign(self):
    #    if not self.is_assigned():
    #        print("ERROR: trying to unassign variable",
    #              self, " not yet assigned")
    #        return
    #    self.assignedValue = None

    # def get_assigned_value(self):
    #    return self.assignedValue

    # def in_cur_domain(self,  value):

    #    if not value in csp.domain:
    #        return False
    #    if self.is_assigned():
    #        return value == self.get_assigned_value()
    #    else:
    #        return self.cur_dom[self.value_index(value)]

    # def value_index(value):
    #    return csp.domain.index(value)


class CSP:
    def __init__(self, filename):
        self.variables = [r + c for r in 'ABCDEFGHI' for c in '123456789']
        self.domain = dict(
            (self.variables[i], NUMS if filename[i] == '0' else filename[i]) for i in range(len(filename)))
        a = [self.colNeighbors(self.variables, i) for i in range(9)]
        b = [self.rowNeighbors(self.variables, i) for i in range(9)]
        c = [self.blockNeighbors(self.variables, i, j)
             for i in range(9) for j in range(9)]
        self.cells = (a + b + c)
        self.cellNeighbors = dict(
            (s, [u for u in self.cells if s in u]) for s in self.variables)
        self.neighbors = dict(
            (s, set(sum(self.cellNeighbors[s], [])) - set([s])) for s in self.variables)
        self.constraints = {(variable, neighbor)
                            for variable in self.variables for neighbor in self.neighbors[variable]}

    # Creates column row, appends to neighbours array
    def colNeighbors(self, b, col):
        neighbors = []
        for i in range(col, len(b), 9):
            neighbors.append(b[i])

        return neighbors

    def rowNeighbors(self, b, row):
        neighbors = []
        end = (row + 1) * 9
        start = end - 9
        for i in range(start, end, 1):
            neighbors.append(b[i])

        return neighbors

    def blockNeighbors(self, b, row, col):
        neighbors = []
        domRow = row - row % 3
        domCol = col - col % 3
        for j in range(3):
            for i in range(3):
                v = b[(j + domCol) + (i + domRow) * 9]
                neighbors.append(v)

        return neighbors

    def solved(self):
        for v in self.variables:
            if len(self.domain[v]) > 1:
                return False

        return True

    def printSudoku(self, values):
        print("SUDOKU:")
        line = ""
        sum = 0
        domain = ""

        for var in self.variables:
            if len(values[var]) > 1:
                domain += '0'

            else:
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

    def consistent(self, assignment, var, val):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment.keys() and assignment[neighbor] == val:
                return False

        return True


def AC3(csp):

    # Creating the queue to store CSPs in
    queue_arcs = queue.Queue()

    # Going through the constraints and storing the csp arcs into the queue
    for arc in csp.constraints:
        queue_arcs.put(arc)

    # while the queue is not empty, we retrieve the constraint arcs
    while not queue_arcs.empty():
        (Xi, Xj) = queue_arcs.get()
        # check arc-consistency using the Revise() function, to see for all values Xi, there's a value we can use in Xj
        if Revise(csp, Xi, Xj):
            # if length of the domain is 0, there's no arc-consistency so return false
            if len(csp.domain[Xi]) == 0:
                return False

            for Xk in (csp.neighbors[Xi] - set(Xj)):
                queue_arcs.put((Xk, Xi))
    return True


def Revise(csp, Xi, Xj):
    revised = False
    values = set(csp.domain[Xi])
    index = 0

    for x in values:
        is_consistent = True
        for y in csp.domain[Xj]:
            if x != y:
                # is_consistent checks if there is a value that is consistent with x
                is_consistent = False
        if is_consistent:
            csp.domain[Xi] = csp.domain[Xi].replace(x, '')
            revised = True
        else:
            index += 1

        # if not isConsistent(csp, x, Xi, Xj):
        #    csp.domain[Xi] = csp.domain[Xi].replace(x, '')
        #    revised = True

    return revised


def isConsistent(csp, x, Xi, Xj):
    for y in csp.domain[Xj]:
        if Xj in csp.neighbors[Xi] and y != x:
            return True

    return False


def backward_track(asmt, csp):
    # might need change
    if set(asmt.keys()) == set(csp.variables):
        return asmt
    var = csp.select_unsigned_var(asmt, csp)
    domain = copy.deepcopy(csp.domain)
    for v in csp.domain[var]:
        if csp.consistent(asmt, var, v):
            asmt[var] = v
            inferences = {}
            inferences = csp.infer(asmt, inferences, csp, var, v)

        if inferences != "Fail":
            result = backward_track(asmt, csp)

            if result != "Fail":
                return result

        csp.domain.update(domain)

    return "Fail"


def select_unsigned_var(assignment, csp):
    unassigned_vars = dict((cell, len(
        csp.domain[cell])) for cell in csp.domain if cell not in assignment.keys())
    return min(unassigned_vars, key=unassigned_vars.get)


def infer(assignment, inferences, csp, var, val):
    inferences[var] = val

    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment and val in csp.domain[neighbor]:
            if len(csp.domain[neighbor]) == 1:
                return "Fail"

            remaining = csp.domain[neighbor] = csp.domain[neighbor].replace(
                val, "")

            if len(remaining) == 1:
                flag = infer(assignment, inferences,
                             csp, neighbor, remaining)

                if flag == "Fail":
                    return "Fail"

    return inferences


csp = CSP(
    '003020600900305001001806400008102900700000008006708200002609500800203009005010300')

if AC3(csp):
    if csp.solved():
        print("----SOLVED SUDOKU WITH AC3----")
        csp.printSudoku(csp.domain)

    else:
        print("----SOLVED SUDOKU WITH BACKTRACKING----")
        sudoku = backward_track({}, csp)
        if sudoku == "Fail":
            print("Unsolvable")

        else:
            csp.printSudoku(sudoku)
