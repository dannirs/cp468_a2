import queue
import copy
from csp import *
# ac-3 algorithm


def AC_3(constraints):
    flag = False

    # Creating the queue to store CSPs in
    queue_arcs = queue.Queue()

    # Going through the constraints and storing the csp arcs into the queue
    for links in constraints.arc_consistency:
        queue_arcs.put(links)

    # while the queue is not empty, we retrieve the constraint arcs
    while queue_arcs.empty() != flag:
        (x, y) = queue_arcs.get()

        # check arc-consistency using the Revise() function, to see for all values Xi, there's a value we can use in Xj
        if domain_change(constraints, x, y):

            # if length of the domain is 0, there's no arc-consistency so return false
            if len(constraints.domain[x]) == 0:
                return flag

            for z in (constraints.adjacent[x] - set(y)):
                queue_arcs.put((z, x))
    flag = True
    return flag

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


def backward_track(task, csp):
    # might need change
    if set(task.keys()) == set(csp.elements):
        return task
    var = select_unsigned_var(task, csp)
    domain = copy.deepcopy(csp.domain)
    for v in csp.domain[var]:
        if csp.constraint_consistency(task, var, v):
            task[var] = v
            inferences = {}
            inferences = infer(task, inferences, csp, var, v)

        if inferences != False:
            result = backward_track(task, csp)

            if result != False:
                return result

        csp.domain.update(domain)

    return False


def select_unsigned_var(assignment, csp):
    unassigned_vars = dict((Variables, len(
        csp.domain[Variables])) for Variables in csp.domain if Variables not in assignment.keys())
    return min(unassigned_vars, key=unassigned_vars.get)


def infer(assignment, inferences, csp, var, val):
    inferences[var] = val
    for neighbor in csp.adjacent[var]:
        if neighbor not in assignment and val in csp.domain[neighbor]:
            if len(csp.domain[neighbor]) == 1:
                return False

            remaining = csp.domain[neighbor] = csp.domain[neighbor].replace(
                val, "")

            if len(remaining) == 1:
                flag = infer(assignment, inferences,
                             csp, neighbor, remaining)

                if flag == False:
                    return False

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
