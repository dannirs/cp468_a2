import copy
import sys
import queue
NUMS = "123456789"


class Variables:
    def __init__(self, row, col, value):
        self.row = row
        self. col = col
        self.value = value
        self.assigned_value = None
        self.cur_dom = [True] * len(CSP.domain)

    def is_assigned(self):
        return self.assignedValue != None

    def assign(self, value):

        if self.is_assigned() or not self.in_cur_domain(value):
            print("ERROR: trying to assign variable", self,
                  "that is already assigned or illegal value (not in curdom)")
            return

        self.assignedValue = value

    def unassign(self):
        if not self.is_assigned():
            print("ERROR: trying to unassign variable",
                  self, " not yet assigned")
            return
        self.assignedValue = None

    def get_assigned_value(self):
        return self.assignedValue

    def in_cur_domain(self,  value):

        if not value in CSP.domain:
            return False
        if self.is_assigned():
            return value == self.get_assigned_value()
        else:
            return self.cur_dom[self.value_index(value)]

    def value_index(value):
        return CSP.domain.index(value)


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

    def consistent(self, assignment, var, val):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment.keys() and assignment[neighbor] == val:
                return False

        return True

    def Revise(csp, Xi, Xj):
        revised = False
        values = set(csp.domain[Xi])

        for x in values:
            if not isConsistent(csp, x, Xi, Xj):
                csp.domain[Xi] = csp.domain[Xi].replace(x, '')
                revised = True

        return revised

    def isConsistent(csp, x, Xi, Xj):
        for y in csp.domain[Xj]:
            if Xj in csp.neighbors[Xi] and y != x:
                return True
            else:
                return False

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
