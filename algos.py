import queue
import sys
import copy
from Constraints import *

from csp import *


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
        inferences = CSP.infer(asmt, inferences, CSP, var, val)

        if inferences != "Fail":
            result = backward_track(asmt, c)

            if result != "Fail":
                return result

        CSP.domain.update(domain)

    return "Fail"
