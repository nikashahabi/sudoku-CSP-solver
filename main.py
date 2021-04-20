import math


def backtrackingSearch(initialSudoku):
    return backtrack(initialSudoku)


def backtrack(sudoku, varChoosing, ):
    if isComplete(sudoku):
        return sudoku
    var = selectUnassignedVar(sudoku, varChoosing)
    for value in selectValue(var, sudoku):
        if isConsistent(var, value, sudoku):
            addVal(sudoku, var, value)
            inferences = inferences(sudoku)
            if inferences is True:
                addInferences(sudoku, inferences)
                result = backtrack(sudoku)
                if result is not False:
                    return result
        removeInferences(sudoku, inferences)
        removeVal(sudoku, var, value)
    return False


def isComplete(sudoku):
    for i in range(len(sudoku)):
        if checkComplete(sudoku[i]) is False:
            return False
    for j in range(len(sudoku)):
        lst = []
        for i in range(len(sudoku)):
            lst.append(sudoku[i][j])
        if checkComplete(lst) is False:
            return False
    sqrt = math.sqrt(len(sudoku))
    for i in range(sqrt):
        for j in range(sqrt):
            lst = getSquare(i, j, sudoku)
            if checkComplete(lst) is False:
                return False
    return True


def checkComplete(lst):
    return False if len(lst) != len(set(lst)) or 0 in lst else True


def getSquare(i, j, sudoku):
    lst = []
    sqrt = int(math.sqrt(len(sudoku)))
    i = i * sqrt
    j = j * sqrt
    for k in range(sqrt):
        for x in range(sqrt):
            lst.append(sudoku[i + k][j + x])
    return lst

def selectUnassignedVar(sudoku, varChoosing):
    if varChoosing == "MRV":
        return selectUnassignedVarWithMRV(sudoku)
    if varChoosing == "random":
        return selectUnassignedVarRandomly(sudoku)
    if varChoosing == "degree heuristic":
        return selectUnassignedVarDegreeHeuristic(sudoku)

def selectUnassignedVarWithMRV(sudoku):
    

def selectUnassignedVarRandomly(sudoku):


def selectUnassignedVarDegreeHeuristic(sudoku):

sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]


