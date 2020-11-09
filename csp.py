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

    # Checks arc consistency, compares to see if value is already in the constraint
    def arc_consistent(self, assignment, var, val):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment.keys() and assignment[neighbor] == val:
                return False

        return True

# ac-3 algorithm


def AC_3(csp):

    # Creating the queue to store CSPs in
    queue_arcs = queue.Queue()

    # Going through the constraints and storing the csp arcs into the queue
    for arc in csp.constraints:
        queue_arcs.put(arc)

    # while the queue is not empty, we retrieve the constraint arcs
    while not queue_arcs.empty():
        (Xi, Xj) = queue_arcs.get()
        # check arc-consistency using the Revise() function, to see for all values Xi, there's a value we can use in Xj
        if domain_change(csp, Xi, Xj):
            # if length of the domain is 0, there's no arc-consistency so return false
            if len(csp.domain[Xi]) == 0:
                return False

            for Xk in (csp.neighbors[Xi] - set(Xj)):
                queue_arcs.put((Xk, Xi))
    return True

# Checks if the value is already in the domain, and if it is, change the domain. Return true if domain was changed, false otherwise


def domain_change(csp, Xi, Xj):
    flag = False
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
            flag = True
        else:
            index += 1

        # if not isConsistent(csp, x, Xi, Xj):
        #    csp.domain[Xi] = csp.domain[Xi].replace(x, '')
        #    revised = True

    return flag

# def consistency_check(csp, x, Xi, Xj):
#    for y in csp.domain[Xj]:
#        if Xj in csp.neighbors[Xi] and y != x:
#            return True
#
#    return False

# uses backtracking algorithm to solve the puzzle


def backward_track(asmt, csp):
    # might need change
    if set(asmt.keys()) == set(csp.elements):
        return asmt
    var = select_unsigned_var(asmt, csp)
    domain = copy.deepcopy(csp.domain)
    for v in csp.domain[var]:
        if csp.arc_consistent(asmt, var, v):
            asmt[var] = v
            inferences = {}
            inferences = infer(asmt, inferences, csp, var, v)

        if inferences != "Fail":
            result = backward_track(asmt, csp)

            if result != "Fail":
                return result

        csp.domain.update(domain)

    return "Fail"


def select_unsigned_var(assignment, csp):
    unassigned_vars = dict((Variables, len(
        csp.domain[Variables])) for Variables in csp.domain if Variables not in assignment.keys())
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


#csp = CSP('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
