#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Rushikesh Pharate
# Username: rpharate
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p'] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' and isSafe(house_map,r,c)]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k

# Check if inserting pichu in current position will not violate the constraints i.e. They are on either the same row, column, or diagonal
# of the map, and there are no walls between them.
def isSafe(map, row,col):
    total_rows = len(map)
    total_cols = len(map[0])

    #Check if pichu is present below the current location in the entire column
    for i in range(row+1,total_rows):
        if map[i][col] == 'p':
            return False
        if map[i][col] in ('X','@'):
            break

    #Check if pichu is present above the the current location in the entire column
    for i in range(row-1,-1,-1):
        if map[i][col] == 'p':
            return False
        if map[i][col] in ('X','@'):
            break

    #Check if pichu is present to the right side of the current location in the entire row
    for i in range(col+1, total_cols):
        if map[row][i] == 'p':
            return False
        if map[row][i] in ('X','@'):
            break

    #Check if pichu is present to the left side of the current location in the entire row
    for i in range(col-1, -1,-1):
        if map[row][i] == 'p':
            return False
        if map[row][i] in ('X','@'):
            break

    #Check if pichu is present in the bottom right diagonal from the current position
    for i,j in zip(range(row+1,total_rows),range(col+1,total_cols)):
        if map[i][j] == 'p':
            return False
        if map[i][j] in ('X', '@'):
            break

    #Check if pichu is present in the bottom left diagonal from the current position
    for i,j in zip(range(row+1,total_rows),range(col-1,-1,-1)):
        if map[i][j] == 'p':
            return False
        if map[i][j] in ('X', '@'):
            break

    #Check if pichu is present in the top right diagonal from the current position
    for i,j in zip(range(row-1,-1,-1),range(col+1,total_cols)):
        if map[i][j] == 'p':
            return False
        if map[i][j] in ('X', '@'):
            break

    #Check if pichu is present in the top left diagonal from the current position
    for i,j in zip(range(row-1,-1,-1),range(col-1,-1,-1)):
        if map[i][j] == 'p':
            return False
        if map[i][j] in ('X', '@'):
            break

    return True


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):

    if k == 1:
        return (initial_house_map,True)

    fringe = [initial_house_map]
    visited_maps = []  #track visited maps so it should not go in infinite loop
    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop()):

            if is_goal(new_house_map,k): #Check if goal is reached (no. of pichus == k)
                return(new_house_map,True)
            if new_house_map not in visited_maps:
                visited_maps.append(new_house_map)
                fringe.append(new_house_map)

    return ('',False)


# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    #This is k, the number of agents
    k = int(sys.argv[2])

    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


