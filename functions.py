import queue
import copy
from csp import *

#AC-3 algorithm 
def AC_3(constraints):
    
    # returns false if inconsistency is found, otherwise returns true
    flag = False

    # Creating the queue to store CSP's arcs in
    queue_arcs = queue.Queue()

    # Going through the constraints and storing the csp arcs into the queue
    for links in constraints.arc_consistency:
        queue_arcs.put(links)

    # while the queue is not empty, we retrieve the constraint arcs
    while queue_arcs.empty() != flag:
        # x = row, y = col
        (x, y) = queue_arcs.get()

        # Checks arc consistency, if it's not maintained then the domain is changed
        if domain_change(constraints, x, y):

            # If length of the domain is 0, there's no arc-consistency so return false
            if len(constraints.zone[x]) == 0:
                return flag

            # get x's neighboring constraints and insert into queue to check this next
            for z in (constraints.adjacent[x] - set(y)):
                queue_arcs.put((z, x))
    
    # if all constraint arcs have been checked and there are no empty domains, then there are no inconsistencies so return true
    flag = True
    return flag

# Checks if the value is already in the domain, and if it is, change the domain. Return true if domain was changed, false otherwise
def domain_change(constraint, x, y):
    flag = False
    elements = set(constraint.zone[x])
    index = 0

    for i in elements:
        is_consistent = True
        for j in constraint.zone[y]:
            if i != j:
                # is_consistent checks if the domain of the constraint is in the overall set
                is_consistent = False
        if is_consistent:
            constraint.zone[x] = constraint.zone[x].replace(x, '')
            flag = True
        else:
            index += 1


    return flag

# uses backtracking algorithm to solve the puzzle
def backward_track(task, constraint):

    if set(task.keys()) == set(constraint.elements):
        return task
    ele = next_var(task, constraint)
    zone = copy.deepcopy(constraint.zone)
    for e in constraint.zone[ele]:

        if constraint.constraint_consistency(task, ele, e):

            task[ele] = e
            inferences = {}
            inferences = helper_maintain(task, inferences, constraint, ele, e)

            if inferences != False:
                result = backward_track(task, constraint)

                if result != False:
                    return result

        constraint.zone.update(zone)

    return False

#Decides which variable to give an assignment next (minimum remaining value heuristic) 
def next_var(task, constraint):

    next_var = dict((Variables, len(
        constraint.zone[Variables])) for Variables in constraint.zone if Variables not in task.keys())
        
    return min(next_var, key=next_var.get)

# Helper function that maintains csp.  
# Value is taken from domain 
# important so that deduction can be reversed if there's partial assignment.
def helper_maintain(task, i, constraint, r, ele):

    i[r] = ele
    for adjacent in constraint.adjacent[r]:

        if adjacent not in task and ele in constraint.zone[adjacent]:

            if len(constraint.zone[adjacent]) == 1:

                return False


            leftover = constraint.zone[adjacent] = constraint.zone[adjacent].replace(
                ele, "")


            if len(leftover) == 1:

                turn = helper_maintain(task, i,
                             constraint, adjacent, leftover)

                if turn == False:
                    
                    return False

    return i


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
