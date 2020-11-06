import queue
import sys
import copy
from Constraints import *

from csp import *
import csp as c


def depth_limited_search():
    return


def backward_track(asmt):
    # might need change
    if set(asmt.keys()) == set(c.variable):
        return asmt
    var = c.select_unsigned_var(asmt, c)
    domain = copy.deepcopy(c.domain)
    for v in c.domain[var]:
        if c.consistent(asmt, var, v):
        asmt[var] = v
        inferences = {}
        inferences = c.inference(asmt, inferences, c, var, val)

        if inferences != "Fail":
            result = backward_track(asmt, c)

            if result != "Fail":
                return result

        c.domain.update(domain)

    return "Fail"
