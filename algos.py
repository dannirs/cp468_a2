import queue
import sys
import copy
#from Constraints import *

from csp import *


def AC3(csp):
    q = queue.Queue()

    for arc in csp.constraints:
        q.put(arc)
        
    while not q.empty():
        (Xi, Xj) = q.get()

        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False
                
            for Xk in (csp.neighbors[Xi] - set(Xj)):
                q.put((Xk, Xi))
    return True


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
