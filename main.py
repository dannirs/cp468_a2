from csp import *
from functions import *
from sudoku import *

filepath1 = 'ac3_sudoku.txt'
filepath2 = 'sudoku_backward.txt'

fp1 = open(filepath1, "r", encoding="utf-8")
sudoku_string1 = file_to_string(fp1)
print(sudoku_string1)

csp1 = CSP(sudoku_string1)

if AC_3(csp1):
    if csp1.check_solve():
        print("----Solve SUDOKU WITH AC3----")
        csp1.sudoku_output(csp1.zone)

    else:
        print("----Solve SUDOKU WITH BACKTRACKING----")
        sudoku = backward_track({}, csp1)
        if sudoku == False:
            print("Unsolvable")

        else:
            csp1.sudoku_output(sudoku)
else:
    print("Unsolvable")
fp2 = open(filepath2, "r", encoding="utf-8")
sudoku_string2 = file_to_string(fp2)
print(sudoku_string2)

csp2 = CSP(sudoku_string2)

if AC_3(csp2):
    if csp2.check_solve():
        print("----Solve SUDOKU WITH AC3----")
        csp2.sudoku_output(csp2.zone)

    else:
        print("----Solve SUDOKU WITH BACKTRACKING----")
        sudoku = backward_track({}, csp2)
        if sudoku == False:
            print("Unsolvable")

        else:
            csp1.sudoku_output(sudoku)
else:
    print("Unsolvable")
fp1.close()
fp2.close()
