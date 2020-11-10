import queue
import copy
from CSP import *
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


def file_to_string(fp):
    str = ""
    buffer = fp.readline()
    for i in buffer:
        if i.isdigit():
            str = str + i
    else:
        while buffer != "":
            buffer = fp.readline()
            for i in buffer:
                if i.isdigit():
                    str = str + i
    return str
