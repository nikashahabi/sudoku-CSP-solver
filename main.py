import math
import random


def backtrackingSearch(initialSudoku, varChoosing, valueChoosing):
    values = setDomains(initialSudoku)
    neighbors = setNeighbors(initialSudoku)
    return backtrack(initialSudoku, varChoosing, valueChoosing, values, neighbors)


def backtrack(sudoku, varChoosing, valueChoosing, values, neighbors):
    if isComplete(sudoku):
        return sudoku
    var = selectUnassignedVar(sudoku, varChoosing, values, neighbors)
    for value in selectValue(var, sudoku, values, valueChoosing):
        if isConsistent(var, value, sudoku):
            addVal(sudoku, var, value)
            # inferences = inferences(sudoku)
            # if inferences is True:
            #     addInferences(sudoku, inferences)
            #     result = backtrack(sudoku, varChoosing, valueChoosing, values, neighbors)
            #     if result is not False:
            #         return result
            result = backtrack(sudoku, varChoosing, valueChoosing, values, neighbors)
            if result is not False:
                return result
        # removeInferences(sudoku, inferences)
        removeVal(sudoku, var)
    return False


def addVal(sudoku, var, value):
    (i, j) = var
    sudoku[i][j] = value


def removeVal(sudoku, var, value):
    (i, j) = var
    sudoku[i][j] = 0


def setDomains(sudoku):
    n = len(sudoku)
    values = [[[] for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            setDomain(sudoku, i, j, values)
    return values


def setDomain(sudoku, i, j, values):
    if sudoku[i][j] != 0:
        values[i][j] = [sudoku[i][j]]
        return
    values[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for k in range(len(sudoku)):
        if sudoku[i][k] in values[i][j]:
            values[i][j].remove(sudoku[i][k])
    for k in range(len(sudoku)):
        if sudoku[k][j] in values[i][j]:
            values[i][j].remove(sudoku[k][j])
    (squarei, squarej) = square(i, j)
    for element in getSquare(squarei, squarej, sudoku):
        if element in values[i][j]:
            values[i][j].remove(element)


def setNeighbors(sudoku):
    n = len(sudoku)
    neighbors = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            setNeighbor(sudoku, i, j, neighbors)
    return neighbors


def setNeighbor(sudoku, i, j, neighbors):
    n = len(sudoku)
    for k in range(n):
        for x in range(n):
            if k == i or x == j or square(i, j) == square(k, x):
                neighbors[i][j] += 1


def square(i, j):
    isquare = int(i/3)
    jsquare = int(j/3)
    square = (isquare, jsquare)
    return square


def isComplete(sudoku):
    for i in range(len(sudoku)):
        if checkComplete(sudoku[i]) is False:
            return False
    for j in range(len(sudoku)):
        if checkComplete(getColumn(sudoku, j)) is False:
            return False
    sqrt = math.sqrt(len(sudoku))
    for i in range(sqrt):
        for j in range(sqrt):
            lst = getSquare(i, j, sudoku)
            if checkComplete(lst) is False:
                return False
    return True


def isConsistent(var, value, sudoku):
    (i, j) = var
    if checkConsistent(sudoku[i]) is False:
        return False
    if checkConsistent(getColumn(sudoku, j)) is False:
        return False
    squarei, squarej = square(i, j)
    if checkConsistent(getSquare(squarei, squarej, sudoku)) is False:
        return False
    return True


def getColumn(sudoku, j):
    lst = []
    for i in range(len(sudoku)):
        lst.append(sudoku[i][j])
    return lst


def checkComplete(lst):
    return False if len(lst) != len(set(lst)) or 0 in lst else True


def checkConsistent(lst):
    return False if len(lst) != len(set(lst)) else True


def getSquare(i, j, sudoku):
    lst = []
    sqrt = int(math.sqrt(len(sudoku)))
    i = i * sqrt
    j = j * sqrt
    for k in range(sqrt):
        for x in range(sqrt):
            lst.append(sudoku[i + k][j + x])
    return lst


def selectUnassignedVar(sudoku, varChoosing, values, neighbors):
    if varChoosing == "MRV":
        return selectUnassignedVarWithMRV(sudoku, values)
    if varChoosing == "first unassigned var":
        return selectUnassignedNextVar(sudoku)
    if varChoosing == "degree heuristic":
        return selectUnassignedVarDegreeHeuristic(sudoku, neighbors)
    raise("invalid variable selecting method")


def selectUnassignedVarWithMRV(sudoku, values):
    temp = float("inf")
    n = len(sudoku)
    for i in range(n):
        for j in range(n):
            if sudoku[i][j] == 0:
                if len(values[i][j]) < temp:
                    temp = len(values[i][j])
                    MRV = (i, j)
    return MRV


def selectUnassignedNextVar(sudoku):
    n = len(sudoku)
    for i in range(n):
        for j in range(n):
            if sudoku[i][j] == 0:
                chosen = (i, j)
                return chosen


def selectUnassignedVarDegreeHeuristic(sudoku, neighbors):
    temp = -float("inf")
    n = len(sudoku)
    for i in range(n):
        for j in range(n):
            if sudoku[i][j] == 0:
                if neighbors[i][j] > temp:
                    temp = neighbors[i][j]
                    chosen = (i, j)
    return chosen


def selectValue(var, sudoku, values, valChoosing):
    if valChoosing == "random":
        return selectRandomValue(var, sudoku, values)
    # if valChoosing == "least constraing value":
    #     return selectLeastConstrainintValue(var, sudoku, values)
    raise("invalid value choosing method")


def selectRandomValue(var, sudoku, values):
    (vari, varj) = var
    return random.choice(values[vari][varj])


sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]

print(setDomains(sudoku))


