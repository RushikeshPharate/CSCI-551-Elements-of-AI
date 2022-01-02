# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import copy
import heapq
import time
from pprint import pprint

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

   #Function to flip piece horizontally.Referred from QuintrisGame.py. 
    def hflip_piece(piece):
        return [ str[::-1] for str in piece ]

    #Function rotate piece.Referred from QuintrisGame.py.
    def rotate_piece(piece, rotation):
        rotated_90 = [ "".join([ str[i] for str in piece[::-1] ]) for i in range(0, len(piece[0])) ]
        return { 0: piece, 90: rotated_90, 180: [ str[::-1] for str in piece[::-1] ], 270: [ str[::-1] for str in rotated_90[::-1] ] }[rotation]


    #Function to calculate heuristic value or cost associated with every move. Checking for holes,bumpiness,aggregate height and score.
    #hole is a an empty space with alteast one tile above it.
    #bumpiness is the difference between the height of consecutive columns.
    #aggregate height is the sum of height of all columns.
    #The coefficients are derived using trial and error methods.

    def heuristic_function(state):
        board,score = state
        hs=0
        cnt_hole=0
        agg_height=0
        h1=h2=0
        bumpiness=0
        pile_up=0
        mx_height=0
        
        for i in range(len(board)-1,-1,-1):
            for j in range(0,len(board[0])):
                if board[i][j]==' ':
                    flg1=False
                    for k in range(i-1,-1,-1):
                        if board[k][j]=='x':
                            flg1=True
                            break
                    if flg1==True:
                        cnt_hole+=1
        for j in range(0,len(board[0])):
            for i in range(0,len(board)):
                if board[i][j]=='x':
                    agg_height+=len(board)-i
                    break
        
        for j in range(0,len(board[0])-1):
            for i in range(0,len(board)):
                if board[i][j]=='x':
                    h1+=len(board)-i
                    break
            for i in range(0,len(board)):
                if board[i][j+1]=='x':
                    h2+=len(board)-i
                    break
            bumpiness+=abs(h1-h2)

        for j in range(0,len(board[0])):
            for i in range(0,len(board)):
                if board[i][j]=='x':
                    if mx_height<len(board)-i:
                        mx_height=len(board)-i
                    
        
        
        
        hs+=0.357*cnt_hole+0.185*bumpiness+0.51*agg_height-0.76*score
        
        
        return hs

    
    #Function the finds out successors of state passed to this function.
    def successor_function(quintris,successor_state1):
        piece = successor_state1[3]
        board = successor_state1[2][0]
        rotations=[]
        rotations.append([piece,''])
        if ComputerPlayer.rotate_piece(piece,90)!=piece:
            rotations.append([ComputerPlayer.rotate_piece(piece,90),'n'])
        if ComputerPlayer.rotate_piece(piece,180)!=piece and ComputerPlayer.rotate_piece(piece,180)!=ComputerPlayer.rotate_piece(piece,90):
            rotations.append([ComputerPlayer.rotate_piece(piece,180),'nn'])
        if ComputerPlayer.rotate_piece(piece,270)!=piece and ComputerPlayer.rotate_piece(piece,270)!=ComputerPlayer.rotate_piece(piece,90) and ComputerPlayer.rotate_piece(piece,270)!=ComputerPlayer.rotate_piece(piece,180):
            rotations.append([ComputerPlayer.rotate_piece(piece,270),'nnn'])
        if ComputerPlayer.hflip_piece(piece)!=piece and ComputerPlayer.hflip_piece(piece)!=ComputerPlayer.rotate_piece(piece,270) and ComputerPlayer.hflip_piece(piece)!= ComputerPlayer.rotate_piece(piece,90) and ComputerPlayer.hflip_piece(piece)!=ComputerPlayer.rotate_piece(piece,180):
            rotations.append([ComputerPlayer.hflip_piece(piece),'h'])
        successors = []
        
        state=copy.deepcopy(successor_state1[2])
        
        for rotation in rotations:
            mx=0
            for i in rotation[0]:
                l=len(i)
                if l>mx:
                    mx=l
            for c in range(0,len(board[0])-mx+1):
                successor_state=[successor_state1[0],0,state,rotation[0],successor_state1[4]]
                row=0
                while not quintris.check_collision(*state, rotation[0], row+1, c):
                    row += 1
                
                successor_state[2] = quintris.remove_complete_lines(*quintris.place_piece(*state, rotation[0], row, c))
                
                successor_state[1] = ComputerPlayer.heuristic_function(successor_state[2])
                successor_state[0] +=successor_state[1]
                
                if successor_state[4]=='':
                    successor_state[4]+=rotation[1]
                    curr_col=quintris.col
                    if c<curr_col:
                        while c<curr_col:
                            successor_state[4]+='b'
                            curr_col-=1
                    elif c>curr_col:
                        while c>curr_col:
                            successor_state[4]+='m'
                            curr_col+=1
                
                heapq.heappush(successors,successor_state)
                
        
        return successors

        

    
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        original_board = quintris.get_board()
        board=copy.deepcopy(original_board)
        state=(board,0)
        successor_state=[0,0,state,quintris.get_piece()[0],'']
        successors=ComputerPlayer.successor_function(quintris,successor_state)

        successors2 = []
        for s in successors:
            s[3] = quintris.get_next_piece()
            curr_succ_state = ComputerPlayer.successor_function(quintris,s)
            for s1 in curr_succ_state:
                heapq.heappush(successors2,s1)
            

            
        
        
        curr_successor = heapq.heappop(successors2)
        
        return curr_successor[4]

        
        
        


        #return random.choice("mnbh") * random.randint(1, 10)
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:

            time.sleep(0.1)

            original_board = quintris.get_board()
            board=copy.deepcopy(original_board)
            state=(board,0)
            successor_state=[0,0,state,quintris.get_piece()[0],'']
            successors=ComputerPlayer.successor_function(quintris,successor_state)

            successors2 = []
            for s in successors:
                s[3] = quintris.get_next_piece()
                curr_succ_state = ComputerPlayer.successor_function(quintris,s)
                for s1 in curr_succ_state:
                    heapq.heappush(successors2,s1)
            


            
        
            
            curr_successor = heapq.heappop(successors2)
            curr_successor[4]+=' '
            for mv in curr_successor[4]:
                if mv=='n':
                    quintris.rotate()
                elif mv=='b':
                    quintris.left()
                elif mv=='m':
                    quintris.right()
                elif mv=='h':
                    quintris.hflip()
                elif mv==' ':
                    quintris.down()




           


            


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



