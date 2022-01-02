#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Rushikesh Pharate
# Email : rpharate@iu.edu
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=[[row+1,col], [row-1,col], [row,col-1], [row,col+1]]

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" )]

def get_move_path(curr_move,move): #returns the step (U,D,L,R) for the current step
        if curr_move[0] > move[0]:
            return 'U'
        elif curr_move[0] < move[0]:
            return 'D'
        elif curr_move[1] > move[1]:
            return 'L'
        elif curr_move[1] < move[1]:
            return 'R'

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[[row_i,col_i] for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]

        move_string = '' #String storing path till now
        curr_dist = 0 #int variable storing distance from initial state
        fringe=[(pichu_loc,curr_dist,move_string)]

        visited_nodes = [pichu_loc] #keeps track of the visited nodes
        while fringe:
                (curr_move, curr_dist,move_string) = fringe.pop()
                for move in moves(house_map, *curr_move):
                        if house_map[move[0]][move[1]]=="@": #check if destination is reached
                            return (curr_dist+1,move_string + get_move_path(curr_move,move)) #update distance, path for the last step and return Answer
                        else:
                            if move not in visited_nodes: #Check if legal move in SUCC function is visited before
                                visited_nodes.append(move) #Add to the visited_nodes list if current node is new
                                fringe.append((move, curr_dist + 1,move_string + get_move_path(curr_move,move))) #update distance, path and add node to fringe


        return (-1,'') #when the goal is not reachable return -1 as distance and no path

# Main Function
if __name__ == "__main__":

        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])



