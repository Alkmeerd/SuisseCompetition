import logging
import json

from copy import deepcopy

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def findingAdjacentPatient(target, row, col):
    x = []
    x.append([target[0]+1,target[1]])
    x.append([target[0]-1,target[1]])
    x.append([target[0],target[1]+1])
    x.append([target[0],target[1]-1])

    #print("Adjacent: ", x)
    for i in range(len(x)):
        if x[i][0] < 0 or x[i][0] >= row:
            x[i] = False
            continue
        if x[i][1] < 0 or x[i][1] >= col:
            x[i] = False
            continue
    x = list(filter((False).__ne__, x))
    #print("Adjacent: ", x)
    return x

####finding DIAGONAL and removing out of bounds 
def findingDiagonalPatient(target, row, col):
    x = []
    x.append([target[0]+1,target[1]+1])
    x.append([target[0]-1,target[1]-1])
    x.append([target[0]-1,target[1]+1])
    x.append([target[0]+1,target[1]-1])

    #print("Diagonal: ", x)
    for i in range(len(x)):
        if x[i][0] < 0 or x[i][0] >= row:
            x[i] = False
            continue
        if x[i][1] < 0 or x[i][1] >= col:
            x[i] = False
            continue
    x = list(filter((False).__ne__, x))
    #print("Diagonal: ", x)
    return x

def question_1_and_2(grid, interestedIndividuals):
    # print("=========QUESTION1AND2=========")
    ####finding patient zero and building lists
    #visited = []
    distance = []
    queue = []

    row = len(grid)
    col = len(grid[0])

    for i in range(len(grid)):
        #visited.append([])
        distance.append([])

        for j in range(len(grid[i])):
            if grid[i][j] == 3:
                origin_x, origin_y = i,j
            #visited[i].append(False)
            distance[i].append(-1)
        
    #print(origin_x,origin_y)

    distance[origin_x][origin_y] = 0
    queue.append([origin_x,origin_y])
    #visited[origin_x][origin_y] = True

    while len(queue) != 0:
        
        target = queue.pop(0)
        #print("Target = ", target)
        adj = findingAdjacentPatient(target, row, col)

        for i in adj:
            if grid[i[0]][i[1]] == 1:
                queue.append(i)
                distance[i[0]][i[1]] = distance[target[0]][target[1]] + 1
                grid[i[0]][i[1]] = 3

    result1 = {}
    for ind in interestedIndividuals:
        ls = ind.split(",")
        result1[ind] = distance[int(ls[0])][int(ls[1])]

    result2 = 0
    for i in range(row):
        for j in range(col):
            if distance[i][j] > result2:
                result2 = distance[i][j]
            if grid[i][j] == 1:
                result2 = -1
                break
        else:
            continue
        break
    
    # print("============RESULT============")
    # print("Question 1: ", result1)
    # print("Question 2: ", result2)
    return result1, result2

def question_3(grid):
    # print("=========QUESTION3=========")
    ####finding patient zero and building lists
    #visited = []
    distance = []
    queue = []

    row = len(grid)
    col = len(grid[0])

    for i in range(len(grid)):
        #visited.append([])
        distance.append([])

        for j in range(len(grid[i])):
            if grid[i][j] == 3:
                origin_x, origin_y = i,j
            #visited[i].append(False)
            distance[i].append(-1)
        
    #print(origin_x,origin_y)

    distance[origin_x][origin_y] = 0
    queue.append([origin_x,origin_y])
    #visited[origin_x][origin_y] = True

    while len(queue) != 0:
        
        target = queue.pop(0)
        #print("Target = ", target)
        adj = findingAdjacentPatient(target, row, col) + findingDiagonalPatient(target,row,col)
        print(adj)

        for i in adj:
            if grid[i[0]][i[1]] == 1:
                queue.append(i)
                distance[i[0]][i[1]] = distance[target[0]][target[1]] + 1
                grid[i[0]][i[1]] = 3

    result3 = 0
    for i in range(row):
        for j in range(col):
            if distance[i][j] > result3:
                result3 = distance[i][j]
            if grid[i][j] == 1:
                result3 = -1
                break
        else:
            continue
        break
    
    # print("============RESULT============")
    # print("Question 3: ", result3)
    return result3

#print("Queue: ",queue)
#print("Visited: ", visited)
#print("Grid: ", grid)
#print("Distance: ", distance)


@app.route('/parasite', methods=['POST'])
def evaluateparasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    submission = []

    for i in range(2):
        ROOM = data[i].get("room")
        GRID = data[i].get("grid")
        interestedIndividuals = data[i].get("interestedIndividuals")


        grid = deepcopy(GRID)
        a,b = question_1_and_2(grid, interestedIndividuals)

        grid = deepcopy(GRID)
        c = question_3(grid)
        d = c

        answer = {}
        answer["room"] = ROOM
        answer["p1"] = a
        answer["p2"] = b
        answer["p3"] = c
        answer["p4"] = c-1

        submission.append(answer)


    logging.info("My result :{}".format(submission))
    return json.dumps(submission)

