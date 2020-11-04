import queue
import sys
import copy
from Constraints import *


def depth_limited_search():
    return


def Inference(assignment, inferences, csp, var, val):
    inferences[var] = val

    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment and val in csp.domain[neighbor]:
            if len(csp.domain[neighbor]) == 1:
                return "Fail"

            remaining = csp.domain[neighbor] = csp.domain[neighbor].replace(
                val, "")

            if len(remaining) == 1:
                flag = Inference(assignment, inferences,
                                 csp, neighbor, remaining)

                if flag == "Fail":
                    return "Fail"

    return inferences


def backward_track(asmt, csp):
    # might need change
    if set(asmt.keys()) == set(csp.variable):
        return asmt
    var = select_unsigned_var(asmt, csp)
    domain = copy.deepcopy(csp.domain)
    for v in csp.domain[var]:
        if csp.consistent(asmt, var, v):
        asmt[var] = v
        inferences = {}
        inferences = Inference(asmt, inferences, csp, var, val)

        if inferences != "Fail":
            result = backward_track(asmt, csp)

            if result != "Fail":
                return result

        csp.domain.update(domain)

    return "Fail"
