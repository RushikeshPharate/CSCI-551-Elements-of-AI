#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np
import copy
from pprint import pprint
import heapq
import math

ROWS=5
COLS=5

# Function to print the board
def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#Function to Transpose the board. Required for clockwise and anticlockwise movement of board.
def transpose_board(board):
  return [list(col) for col in zip(*board)]

# Function for right movement on given row on the board.
def right_shift(board,row):
    board[row].insert(0,board[row].pop())
    return board

# Function for left movement on given row on the board.
def left_shift(board,row):

    board[row].append(board[row].pop(0))
    return board

# Function to place the number that moves from row to column(or vice versa) during circular rotation.  
def right_rotate(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

# Function to place the number that moves from row to column(or vice versa) during circular rotation.
def left_rotate(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

# Function for clockwise movement
def move_clockwise(given_board):
    given_board[0]=[given_board[1][0]]+given_board[0]
    residual=given_board[0].pop()
    given_board=transpose_board(given_board)
    residual=right_rotate(given_board,-1,residual)
    given_board=transpose_board(given_board)
    residual=left_rotate(given_board,-1,residual)
    given_board=transpose_board(given_board)
    residual=left_rotate(given_board,0,residual)
    given_board=transpose_board(given_board)
    return given_board

# Function for counter-clockwise movement
def move_cclockwise(given_board):
    given_board[0]=given_board[0]+[given_board[1][-1]]
    residual=given_board[0].pop(0)
    given_board=transpose_board(given_board)
    residual=right_rotate(given_board,0,residual)
    given_board=transpose_board(given_board)
    residual=right_rotate(given_board,-1,residual)
    given_board=transpose_board(given_board)
    residual=left_rotate(given_board,-1,residual)
    given_board=transpose_board(given_board)
    return given_board

# Function to check position of a number in goal board
def check_position_in_goal(board,number):
    
    for i in range(5):
        for j in range(5):
            if board[i][j] == number:
                return i, j

# Function for heuristic function. Manhattan distance is twisted for an admissible function.
def heuristic_function(board):
    manhattan_distance = 0
    goal_board=[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    for row in range(ROWS):
        for col in range(COLS):
            number = board[row][col]
            if number != 0:
                goal_x, goal_y = check_position_in_goal(goal_board,number)
                manhattan_distance += abs(goal_x - row) + abs(goal_y - col)
    return manhattan_distance
    


# return a list of possible successor states
def successors(current_board_state):
    
    successor_states=[]
    for i in range(ROWS):
        state=copy.deepcopy(current_board_state)
        successor_board1=right_shift(copy.deepcopy(state[3]),i)
        state[3]=successor_board1
        state[1]+=1
        state[2]=heuristic_function(state[3])//5
        state[0]=state[1]+state[2]
        state[4]+="R"+str(i+1)+" "
        successor_states.append(state)

        state=copy.deepcopy(current_board_state)
        successor_board2=left_shift(copy.deepcopy(state[3]),i)
        state[3]=successor_board2
        state[1]+=1
        state[2]=heuristic_function(state[3])//5
        state[0]=state[1]+state[2]
        state[4]+="L"+str(i+1)+" "
        successor_states.append(state)

    
    for i in range(COLS):
        state=copy.deepcopy(current_board_state)
        
        transposeboard=transpose_board(copy.deepcopy(state[3]))
        rightshift=right_shift(copy.deepcopy(transposeboard),i)
        leftshift=left_shift(copy.deepcopy(transposeboard),i)
        successor_board1=transpose_board(rightshift)
        successor_board2=transpose_board(leftshift)
        state[3]=successor_board1
        state[4]+="D"+str(i+1)+" "
        state[1]+=1
        state[2]=heuristic_function(state[3])//5
        state[0]=state[1]+state[2]
        successor_states.append(state)

        state=copy.deepcopy(current_board_state)
        state[3]=successor_board2
        state[4]+="U"+str(i+1)+" "
        state[1]+=1
        state[2]=heuristic_function(state[3])//5
        state[0]=state[1]+state[2]
        successor_states.append(state)
        

    state=copy.deepcopy(current_board_state)
    successor_board1=move_clockwise(copy.deepcopy(state[3]))
    state[3]=successor_board1
    state[4]+="Oc "
    state[1]+=1
    state[2]=heuristic_function(state[3])//16
    state[0]=state[1]+state[2]
    successor_states.append(state)

    state=copy.deepcopy(current_board_state)
    successor_board2=move_cclockwise(copy.deepcopy(state[3]))
    state[3]=successor_board2
    state[4]+="Occ "
    state[1]+=1
    state[2]=heuristic_function(state[3])//16
    state[0]=state[1]+state[2]
    successor_states.append(state)

    state=copy.deepcopy(current_board_state)
    board=np.array(state[3])
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_clockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    state[3]=board
    state[4]+="Ic "
    state[1]+=1
    state[2]=heuristic_function(state[3])//8
    state[0]=state[1]+state[2]
    successor_states.append(state)

    
    state=copy.deepcopy(current_board_state)
    board=np.array(state[3])
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_cclockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    state[3]=board
    state[4]+="Icc "
    state[1]+=1
    state[2]=heuristic_function(state[3])//8
    state[0]=state[1]+state[2]
    successor_states.append(state)
    
    return successor_states


# check if we've reached the goal
def is_goal(state):
    goal_list=[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    if state==goal_list:
        return True
    else:
        return False



def solve(initial_board):
    
    closed=[]
    
    state = np.array(initial_board).reshape(ROWS, COLS).tolist()
    current_board_state=[0,0,0,state,""]

    

    res = is_goal(current_board_state[3])
    if res:
        return current_board_state[4]
    fringe = []
    heapq.heappush(fringe, current_board_state)            #using heapq for implementing priority queue
    while len(fringe):
        s = heapq.heappop(fringe)
        if s[3] in closed:
            continue
        if is_goal(s[3]):
            s[4]=s[4].strip()
            moves_seq=s[4].split(" ")
            return moves_seq
        closed.append(s[3])
        for s1 in successors(s):
            heapq.heappush(fringe, s1)
    return False


    #return ["Oc","L2","Icc", "R4"]

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
