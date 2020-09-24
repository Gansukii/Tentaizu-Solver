from itertools import combinations
import numpy as np

f = open("tentaizugiven.txt","r")
puzzle_collection = []
given = []
container = []
counter = 0
for line in f.read():
    if counter == 7:
        counter = 0
        given_append = given.copy()
        puzzle_collection.append(given_append)
        given.clear()
        continue
    if line == '\n':
        container_append = container.copy()
        given.append(container_append)
        container.clear()
        counter+=1
    else:
        container.append(line)

container_append = container.copy()
given.append(container_append)
given_append = given.copy()
puzzle_collection.append(given_append)
f.close()

##for i in puzzle_collection:
##    print(np.matrix(i))
##    print()

def check(i,j):
    if i == 0 and j==0:
        return [(0,1),(1,0),(1,1)]
    elif i == 0 and j == 6:
        return [(0,5),(1,6),(1,6)]
    elif i == 6 and j == 0:
        return [(5,0),(5,1),(6,1)]
    elif i == 6 and j == 6:
        return [(5,5),(5,6),(6,5)]
    elif i == 0:
        return [(0,j-1),(0,j+1),(1,j-1),(1,j),(1,j+1)]
    elif i == 6:
        return [(5,j-1),(5,j),(5,j+1),(6,j-1),(6,j+1)]
    elif j == 0:
        return [(i-1,0),(i+1,0),(i-1,1),(i,1),(i+1,1)]
    elif j == 6:
        return [(i-1,6),(i+1,6),(i-1,5),(i,5),(i+1,5)]
    else:
        return [(i-1,j-1),(i-1,j),(i-1,j+1),
                (i,j-1),(i,j+1),
                (i+1,j-1),(i+1,j),(i+1,j+1)]

def initial_check(given):
    for i in range (7):
        for j in range(7):
            if given[i][j] == '0':
                zeros = check(i, j)
                for x in zeros:
                    taken.add(x)
                taken.add((i, j))
            elif given[i][j] != '.':
                taken.add((i,j))

def print_given(given):
    for i in range (7):
        print('-----------------------------')
        for j in range(7):
            if j == 0:
                print("|",end = ' ')
            if given[i][j] == '.':
                print("  |", end = ' ')
                continue
            print(given[i][j],"|",end=' ')
        print()
    print('-----------------------------')



def add_taken(arr):
    for i in arr:
        taken.add(i)
    

def modify_taken(arr):
    newarr = arr.copy()
    for x in arr:
        if x in taken:
            newarr.remove(x)
    return newarr

def remove_taken(arr):
    for i in arr:
        if i in taken:
            taken.remove(i)



def solve(stars,givenz):
    for i in range(7):
        for j in range(7):
            ijcoord = (i, j)
            if ijcoord in skips:
                continue
            if givenz[i][j] == '0':
                continue
            if givenz[i][j] != '.' and givenz[i][j] != '*':
                clue = int(givenz[i][j])
                arr = check(i,j)
                for item in arr:
                    if givenz[item[0]][item[1]] == '*':
                        clue -= 1
                        if clue < 0:
                            return
                newarr = modify_taken(arr)
                newarrpos = list(combinations(newarr,clue))
                if clue == 0:
                    add_taken(newarr)
                    skips.add((i,j))
                    solve(stars,givenz)
                    remove_taken(newarr)
                    skips.remove((i, j))
                    return
                if clue > 0:
                    if len(newarrpos) == 0:
                        return
                    for x in newarrpos:
                        for coord in x:
                            givenz[coord[0]][coord[1]] = '*'
                        stars += clue
                        if stars > 10:
                            for coord in x:
                                givenz[coord[0]][coord[1]] = '.'
                            return
                        add_taken(newarr)
                        skips.add((i,j))
                        solve(stars,givenz)
                        stars -= clue
                        for coord in x:
                            givenz[coord[0]][coord[1]] = '.'
                    remove_taken(newarr)
                    skips.remove((i, j))
                    return

    print_given(givenz)
    global valid
    valid = True


for i in range(len(puzzle_collection)):
    skips = set({})
    taken = set({})
    valid = False
    initial_check(puzzle_collection[i])
    print("QUESTION ", i+1,":")
    print_given(puzzle_collection[i])
    print("Answer:")
    solve(0,puzzle_collection[i])
    if not valid:
        print("The puzzle is not valid!")

