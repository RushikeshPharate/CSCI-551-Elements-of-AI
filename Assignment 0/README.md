# a0

Problem 1: Navigation
----------------------------------------------------
State Space: All the states on the map where pichu can possibly sit (State represented by '.' on the map)

Initial State: Initial position of pichu (location of 'p' on the map)

Goal State: My position in the room (Location of '@' on the map)

Successor Function: All the valid moves pichu can make from current position (Moves() Function is predefined for this activity)

Cost Function: Cost associated with each move 

The Function is going into infinite loop because we are allowing our algorithm to go to nodes which are visited before. 
(new list visited_nodes is defined to keep track of visited node)

After maintaining visited_nodes, correct count was displayed for different goal locations

For getting the path, we have to maintain travelled path so far (move string) when we append fringe with possible legal moves

New function is defined (get_move_path) to get the current move (D,U,L,R) and add it to move_string 

Lastly, goal state not found condition is handled.


Problem 2: Hide-and-seek
---------------------------------------------------
State Space: Valid configuration of k agents on the map such that no agent is facing another agent directly nor diagonally

Initial State: One agent located on the map

Goal State: k agents on the map, no agent faces another agent directly nor diagonally

Successor Function: List of house maps with one extra pichu added without violating the constraints i.e. no pichus are on either the same row, column, or diagonal
of the map, and there are no walls between them.

Cost Function: cost assosiated with placing new pichu in the map.


The function was giving wrong answer initially because after finding '.', it was directly inserting pichu at that location.
I wrote a function isGoal(map,row,col) to check if placing pichu at the current location will not violate any cnstraints i.e. no pichus are on either the same row, column, or diagonal
of the map, and there are no walls between them.

To optimize the solution, I'm keeping track of the visited_maps so that the function will not get stuck in infinite loop

Added logic to handle negative scenario

Added logic to handle k==1







