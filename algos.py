import queue
import sys
import copy
from Constraints import *

from csp import *


def forwardCheck(self, key, value):
    # still need to fix this
    savedData = {}
    savedData[key] = copy.copy(self.CSP.values[key])
    self.unassigned[key] = False

    self.CSP.values[key] = [value]
    for Xk in self.CSP.getNeighbors(key):
        index = 0
        domain = self.CSP.values[Xk]
        copied = False
        for dValue in domain:
            if (dValue == value):
                if not copied:
                    savedData[Xk] = copy.copy(domain)
                    copied = True
                domain.pop(index)
            else:
                index += 1

    return savedData


def depth_limited_search():
    return


def backward_track(asmt):
    # might need change
    if set(asmt.keys()) == set(CSP.variables):
        return asmt
    var = CSP.select_unsigned_var(asmt, CSP)
    domain = copy.deepcopy(CSP.domain)
    for v in CSP.domain[var]:
        if CSP.consistent(asmt, var, v):
        asmt[var] = v
        inferences = {}
        inferences = CSP.infer(asmt, inferences, CSP, var, v)

        if inferences != "Fail":
            result = backward_track(asmt, c)

            if result != "Fail":
                return result

        CSP.domain.update(domain)

    return "Fail"
