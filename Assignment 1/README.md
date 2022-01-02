


# Part 1: 
State Space: State Space consist of all the possible states of the board that can be reached by any combination of permitted moves on the initial board. These moves are: <br>
Sliding rows, R (right) or L (left).<br>
Sliding columns, U (up) or D (down).<br>
Rotating I (inner) or O (outer) ring in clockwise(c) or counterclockwise (cc).<br>
For Example, board_state2 given below is in the state space as it can be reached from initial_board in moves L1 and U5.<br>
initial_board=[2,23,4,5,10,1,7,3,9,11,6,13,8,15,20,12,17,14,19,25,16,21,22,18,24]
board_state2=[23,4,5,10,11,1,7,3,9,20,6,13,8,15,25,12,17,14,19,25,16,21,22,18,2].<br>

Initial State: The state of the board given by the user as input. It is the state before performing any moves.

Goal State: State of the board in canonical form. That is [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]].

Successor function: The successor function returns all possible successors of the current state. For each state of the board, one can:<br>
Move row left or right. There are 5 rows so 10 possible successors.<br>
Move column Up and Down. There are 5 columns so 10 possible successors.<br>
Move outer ring Clockwise or counter-clockwise. So 2 possible successors.<br>
Move inner ring Clockwise or counter-clockwise. So 2 possible successors.<br>
So for each state, the successor function will return 24 successors.<br>


Cost Function: Cost function is defined as: <br>
 f(s) = g(s) + h(s)<br>
g(s) is the cost to reach the current state. h(s) is the estimated cost to reach the goal state.
Everytime we reach a state we increement g(s) by 1. 

Heuristic function: For the heuristic function for Row and Column operation, I take the Manhattan distance between the position of the tile in the current state and the goal state. Then I Integer divide this distance by the number of rows(i.e 5) to make this heuristic admissible. We do this as the total number of tiles displaced during the move was 5.<br>
For the heuristic function for outer ring movement, I Integer divide the Manhattan distance by 16 as the total number of tiles displaced during the move was 16.This makes the heuristic function admissible.<br>
For the heuristic function for inner ring movement, I Integer divide the Manhattan distance by 8 as the total number of tiles displaced during the move was 8.This makes the heuristic function admissible.

Questions:
1. In this problem, what is the branching factor of the search tree?<br>
Ans: The Branching factor of the search tree is 24. As Each state will have 24 possible sucessors, so every node will have 24 children. <br>

2. If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? A rough answer is fine.<br>
Ans: BFS traverses all the nodes starting from the root node till a goal node is found. It will traverse all nodes at depth 0 followed by depth1 then depth 2 and so on.
Number of nodes traversed are as follow:
1. At root: 24<sup>0</sup> = 1
2. At depth 1: 24<sup>1</sup> = 24<br>
3. At depth 2: 24<sup>2</sup> = 576<br>
4. At depth 3: 24<sup>3</sup> = 13824<br>
5. At depth 4: 24<sup>4</sup> = 331776<br>
6. At depth 5: 24<sup>5</sup> = 7962624<br>
7. At depth 6: 24<sup>6</sup> = 191102976<br>
8. At depth 7: 24<sup>7</sup> = 4586471424<br>
Best case scenario: Best case is that the first state we search at depth 7 is the goal node. If so, nodes traversed at depth 7 is one. Therefore, total states explored is 24<sup>0</sup> + 24<sup>1</sup> + 24<sup>2</sup> + 24<sup>3</sup> + 24<sup>4</sup> + 24<sup>5</sup> + 24<sup>6</sup> + 1 = 199411802.<br>
Worst case scenario: Worst case is that the goal state is present as the last node at depth 7. If so, nodes traversed at depth 7 is 24<sup>7</sup>. Therefore, total states explored is 24<sup>0</sup> + 24<sup>1</sup> + 24<sup>2</sup> + 24<sup>3</sup> + 24<sup>4</sup> + 24<sup>5</sup> + 24<sup>6</sup> + 24<sup>7</sup> = 4785883225.<br>
Reference: For moving the outer and inner rings clockwise and counter-clockwise, the logic was reffered from the given testfile.


# Part 2
Initial State- Initial State was the city from which we are starting to find path to the goal city.

Goal State- It was the city we must reached by choosing optimal path depending upon cost function

Successor Function- Here we are finding the neighbors of the city and then according to the cost function we are moving towards next optimal node

Cost Function-
There are 4 Cost Function According to which path to the goal city is decided 
They are Distance, Time, Segments and Delivery.
With Distance, we find the path that has minimum distance between start city to goal city
With Time, we find the path that requires minimum time between start city to goal city
With Segments, we find the path that has minimum number of segments between start city to goal city
With Delivery, We find the Fastest Route where a Delivery Driver can drive on Particular Road, Considering there is less chance of falling the package or getting destroyed and they have to travel again

Heuristic Function-
For Distance I have used Heuristic Function called Haversine Distance which gives distance between 2 Nodes based on longitude to latitude
For Time I have used Same Haversine Distance Divided by Maximum Speed Possible between nodes which I have take as 65mph by looking at dataset
For Segments I have defined Heuristic Function where we find the Number of nodes between next city and goal city and choose the next city which has less number of nodes
For Delivery, I used Heuristic Function as used for time plus delivery time

Approach-
We first Find the Neighbors of the given node or city and proceeded according to requirement
For distance we put normal distance up to a node and Haversine distance from that node to goal city and put it into Priority Queue which will then take values which have minimum distance cost and find the optimal solution. For time and Delivery we used the Same Approach, like For time we take time required to travel on that particular node plus Haversine distance divided by maximum speed possible to travel between that node and goal city. We choose the segments that have minimum time required.
For Segments we took the path that have minimum number of segments from next node to goal city   



# Part 3:

- State Space: Groups of all the users where each group has all the users in the combination of 1/2/3
- Initial State: Users arranged in the groups of 1 each
- Succesor Function: For the current state, successor function is all the unique combinations of teams derived after arranging  
- Goal State: There is no particular goal state here, we are searching for arrangements of given users into groups of 1/2/3 such that the the staff has to do minimum work
- Cost Function: For a given combination of groups, the cost function is total amount of time the staff has to spend for this combination
Calculation of time spent on current combination was not that hard to implement as it was just about handling every case for time required mentioned in the assignment
The hardest part of the assignment was to come up with the successor function and initial state.
When I first started thinking about the problem, forming groups of 3 seemed like a good option for initial state because the time for grading each assignment is 5 mins and having less teams means less cost. But, after spending some time thinking about what will be the successor function I dropped that thought as I was not able to come up with a logic for successor function. 
After spending a day or two on thinking about the initial state and successor functions, I came up with an idea to start with groups of 1 user each and then increment the group size one at a time. The successor function in this case return all the valid combination of group arrangement with size increased by 1.
While coding the logic for calculating successor functions I made a lot of mistakes but after spending significant amount of time on dubugging finally I was able to implement it correctly.
Also, when I was working on defining successor function I had a high level discussion with Nikhil Kambale from EAI-b551 in person batch about how we can implement it

"""
