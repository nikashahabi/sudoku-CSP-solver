import math
import random


def backtrackingSearch(initialSudoku, varChoosing, valueChoosing):
    # performs backtracking on an initial sudoku with a specific varChoosing and valueChoosing method
    values = setDomains(initialSudoku)
    # setDomains performs arc consistency
    # example: values[0][0] = [1, 2, 3]. 1, 2, 3 are legal values for (0,0)
    neighbors = setNeighbors(initialSudoku)
    # example: neighbors[0][0] = [(0,1)]. (0,1) is a unassigned variable which has a binary constraint with (0,0)
    print("performing backtracking +", varChoosing, "+", valueChoosing)
    return backtrack(initialSudoku, varChoosing, valueChoosing, values, neighbors)


def backtrack(sudoku, varChoosing, valueChoosing, values, neighbors):
    # performs recursive backtracking
    if isComplete(sudoku):
        return sudoku
    var = selectUnassignedVar(sudoku, varChoosing, values, neighbors)
    print("chosen variable = ", var)
    for value in selectValue(var, values, valueChoosing, neighbors):
        print("chosen value = ", value)
        inferences = []
        if isConsistent(var, value, sudoku):
            print("chosen value is consistent")
            addVal(sudoku, var, value)
            neighbors = setNeighbors(sudoku)
            inferences = getForwardCheck(var, value, neighbors, values)
            forwardCheck(inferences, values, value)
            result = backtrack(sudoku, varChoosing, valueChoosing, values, neighbors)
            if result is not False:
                return result
        print("backtracked. choosing a new value for", var, "if available")
        removeVal(sudoku, var)
        neighbors = setNeighbors(sudoku)
        reverseForwardCheck(inferences, values, value)
    return False


def getForwardCheck(var, value, neighbors, values):
    lst = []
    (i, j) = var
    for neighbor in neighbors[i][j]:
        (k, x) = neighbor
        if value in values[k][x]:
            lst.append((k, x))
    return lst


def forwardCheck(inferences, values, value):
    for neighbor in inferences:
        (i, j) = neighbor
        values[i][j].remove(value)


def reverseForwardCheck(inferences, values, value):
    for neighbor in inferences:
        (i, j) = neighbor
        values[i][j].append(value)


def addVal(sudoku, var, value):
    (i, j) = var
    sudoku[i][j] = value


def removeVal(sudoku, var):
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
    neighbors = [[[] for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            setNeighbor(sudoku, i, j, neighbors)
    return neighbors


def setNeighbor(sudoku, i, j, neighbors):
    n = len(sudoku)
    for k in range(n):
        for x in range(n):
            if k == i or x == j or square(i, j) == square(k, x):
                neighbors[i][j].append((k, x))


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
    sqrt = int(math.sqrt(len(sudoku)))
    for i in range(sqrt):
        for j in range(sqrt):
            lst = getSquare(i, j, sudoku)
            if checkComplete(lst) is False:
                return False
    return True


def isConsistent(var, value, sudoku):
    (i, j) = var
    if checkConsistent(sudoku[i], value) is False:
        return False
    if checkConsistent(getColumn(sudoku, j), value) is False:
        return False
    squarei, squarej = square(i, j)
    if checkConsistent(getSquare(squarei, squarej, sudoku), value) is False:
        return False
    return True


def getColumn(sudoku, j):
    lst = []
    for i in range(len(sudoku)):
        lst.append(sudoku[i][j])
    return lst


def checkComplete(lst):
    return False if len(lst) != len(set(lst)) or 0 in lst else True


def checkConsistent(lst, value):
    return False if lst.count(value) > 0 else True



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
                if len(neighbors[i][j]) > temp:
                    temp = len(neighbors[i][j])
                    chosen = (i, j)
    return chosen


def selectValue(var, values, valChoosing, neighbors):
    if valChoosing == "value choosing from 1 to 9":
        (i, j) = var
        return [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if valChoosing == "least constraining value":
        return selectLeastConstrainingValue(var, sudoku, values, neighbors)
    raise("invalid value choosing method")


def selectLeastConstrainingValue(var, sudoku, values, neighbors):
    (i, j) = var
    count = [0 for i in range(9)]
    for neighbor in neighbors[i][j]:
        (x, y) = neighbor
        for v in values[x][y]:
            count[v-1] += 1
    lst = []
    while len(lst) < 9:
        minimum = min(count)
        minIndex = count.index(minimum)
        count[minIndex] = float("inf")
        lst.append(minIndex + 1)
    return lst


def printSudoku(sudoku):
    for i in range(9):
        for j in range(9):
            print(sudoku[i][j], end="")
            if j == 2 or j == 5:
                print("|",end="")
        print()
        if i == 2 or i == 5:
            print("------------")




sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]


printSudoku(backtrackingSearch(sudoku, "first unassigned var", "value choosing from 1 to 9"))
sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]
printSudoku(backtrackingSearch(sudoku, "MRV", "value choosing from 1 to 9"))
sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]
printSudoku(backtrackingSearch(sudoku, "degree heuristic", "value choosing from 1 to 9"))
sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]
printSudoku(backtrackingSearch(sudoku, "first unassigned var", "least constraining value"))
sudoku = [[7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]
printSudoku(backtrackingSearch(sudoku, "MRV", "least constraining value"))


