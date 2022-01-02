#
# raichu.py : Play the game of Raichu
#
# 
# Name: Rushikesh Pharate
# Username: rpharate
# 
#

"""
Report: Assignment 2 Part 1

After reading the questions first thing that crossed my mind was, Can we do this using minimax?? as I found the minimax algorithm very fascinating when it was taught in the class.
The problem was also satisfying the preconditions for it:
 
- Two player 
- Turn taking 
- Fully observable
- Zero sum 
- Time constrained 


Before diving into coding, I had to think about various factors that will require to implement the algorithm
- As the time constrainet was between 10-30 seconds scanning whole tree was impossible, thus I decided to take horizon of around 2
- One question was should I implement alpha-beta prunning. For this I decided to not to implement it in the first go will keep it for last if i get time.
- First I started with finding successor functions for every possible input (w,b,W,B,@,$) -> This took significant amount of time as I had to handle every edge case.(Also, I printed many boards for edge cases to test its working properly using pritanle_board(board) function that i wrote just for testing) I have covered every successors for every state. atleast i think so ;)
- After this, most crtitical thing to consider was how will i assignemt values to each state at the horizon?? which parameters should i include to decide the values for each state? How to make it fair??
    Refering below evaluation function for chess, I have calculated an evaluation function for our game

    https://www.chessprogramming.org/Evaluation

    f(p) = 200(K-K') + 9(Q-Q') + 5(R-R') + 3(B-B' + N-N') + 1(P-P') 
    where,
    KQRBNP = number of kings, queens, rooks, bishops, knights and pawns

    Evaluation function for our game
     = 200(@-$) + 50(W-B) + 5(w-b) 

- After implementing minmax algorithm and integrating it with proper successors I was not able to get output within timelimit of 10 seconds. Even depth of 3-4 was taking between 100-200 seconds and thus was not efficient and thus i decided to go for depth of 2 only. As i was only taking depth till 2, i thaught implementing alpha-beta prunning will not make significant improvement in running time and hene i decided not to do that and instead work on evaluation funtion which can improve accurancy significantly.
- After running my code with David's random player on tank server, I got an error of invalid move. There was a misunderstnding from my side while interpreting the question. I thought we could be asked to predict next move of any player and we have return move for that player ONLY (Ex. for the below command: python raichu.py 8 w '@....$.$.............................w..................@...@...' 10 --> we will return next move for w only and not for W/@.) but it was wrong and i fixed it. I have kept the code for this part (def succ) to let you guys see that function.
- On the competition thread  I played like 10-12 games out of which I won 3-4, tied 3-4, lost 1 and faced issue of invalid move by my program in 2. I had posted about this issue in Q&A for this but haven't received response. I also attended office hours of Chinmayee Mundhe on 5th Nov regarding this issue and she said sometimes tank server gives random errors and you should be good as your program is running properly beating other players and tied matches. Also, when my friends played their program against mine i exposed their wrong logic for some cases and they were able to fix it.
- Finally, I decided to implement alpha-beta prunning. I have implemented the logic for it but not sure if its accurate. I am getting improved efficiency because of it. The moves which was taking 5-6 seconds are getting returned in 2-3 seconds now. I might not have implemented it the right way but my program has beaten a lot of other teams and tied matches after the implementation. And thats why i'm keeping it :)
- 


"""

import sys
import time
import copy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def printable_board(brd):
    return "\n".join(["".join(row) for row in brd])

# Calculate successors of pichu
def pichu_succ(board,player,row,col):
    pichu_succ=[]

    if player=='w':
        # print("Calculating SUCC for ({},{})".format(row,col))
        # Calculate right diagonal successor of white pichu
        if col<len(board)-1 and row<len(board)-1:
            if board[row+1][col+1]=='.':
                temp=copy.deepcopy(board)
                if row==len(board)-2:
                    temp[row+1][col+1]='@'    
                else:
                    temp[row+1][col+1]='w'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate right diagonal succsessors of white pichu")
                # print(printable_board(temp))
                # print('\n')

        # Calculate right diagonal jumpover successor of white pichu
        if col<len(board)-2 and row<len(board)-2:
            if board[row+1][col+1]=='b' and board[row+2][col+2]=='.':
                temp=copy.deepcopy(board)
                if row==len(board)-3:
                    temp[row+2][col+2]='@'
                else:
                    temp[row+2][col+2]='w'
                temp[row+1][col+1]='.'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate right diagonal jumpover successor of white pichu")
                # print(printable_board(temp))
                # print('\n')

        # Calculate left diagonal successor of white pichu
        if col>0 and row<len(board)-1:
            if board[row+1][col-1]=='.':
                temp=copy.deepcopy(board)
                if row==len(board)-2:
                    temp[row+1][col-1]='@'    
                else:
                    temp[row+1][col-1]='w'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate left diagonal successor of white pichu")
                # print(printable_board(temp))
                # print('\n')

        # Calculate left diagonal jumpover successor of white pichu
        if col>1 and row<len(board)-2:
            if board[row+1][col-1]=='b' and board[row+2][col-2]=='.':
                temp=copy.deepcopy(board)
                if row==len(board)-3:
                    temp[row+2][col-2]='@'
                else:
                    temp[row+2][col-2]='w'
                temp[row+1][col-1]='.'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate left diagonal jumpover successor of white pichu")
                # print(printable_board(temp))
                # print('\n')

    if player=='b':
        # print("Calculating SUCC for ({},{})".format(row,col))
        # Calculate right diagonal successor of black pichu
        if col<len(board)-1 and row>0:
            if board[row-1][col+1]=='.':
                temp=copy.deepcopy(board)
                if row==1:
                    temp[row-1][col+1]='$'    
                else:
                    temp[row-1][col+1]='b'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate right diagonal successor of black pichu")
                # print(printable_board(temp))
                # print('\n')

        # Calculate right diagonal jumpover successor of black pichu
        if col<len(board)-2 and row>1:
            if board[row-1][col+1]=='w' and board[row-2][col+2]=='.':
                temp=copy.deepcopy(board)
                if row==2:
                    temp[row-2][col+2]='$'
                else:
                    temp[row-2][col+2]='b'
                temp[row-1][col+1]='.'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print(" Calculate right diagonal jumpover successor of black pichu")
                # print(printable_board(temp))
                # print('\n')

        # Calculate left diagonal successor of black pichu
        if col>0 and row>0:
            if board[row-1][col-1]=='.':
                temp=copy.deepcopy(board)
                if row==1:
                    temp[row-1][col-1]='$'    
                else:
                    temp[row-1][col-1]='b'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate left diagonal succsessors of black pichu")
                # print(printable_board(temp))
                # print('\n')

        # Calculate left diagonal jumpover successor of black pichu
        if col>1 and row>1:
            if board[row-1][col-1]=='w' and board[row-2][col-2]=='.':
                temp=copy.deepcopy(board)
                if row==2:
                    temp[row-2][col-2]='$'
                else:
                    temp[row-2][col-2]='b'
                temp[row-1][col-1]='.'
                temp[row][col]='.'
                pichu_succ.append(temp)
                # print("# Calculate left diagonal jumpover successor of black pichu")
                # print(printable_board(temp))
                # print('\n')

    return pichu_succ

# Calculate successors of pikachu          
def pikachu_succ(board,player,row,col):
    pikachu_succ=[]

    if player=='W':

        # print("Calculating SUCC for ({},{})".format(row,col))
         # Calculate 1 step Forward move of white pikachu
        if row<len(board)-1 and board[row+1][col]=='.':
            temp=copy.deepcopy(board)
            if row==len(board)-2:
                temp[row+1][col]='@'
            else:
                temp[row+1][col]='W'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 1 step Forward move of white pichu")
            # print(printable_board(temp))
            # print('\n')

         # Calculate 2 steps Forward move of white pikachu
        if row<len(board)-2 and board[row+1][col]=='.' and board[row+2][col]=='.':
            temp=copy.deepcopy(board)
            if row==len(board)-3:
                temp[row+2][col]='@'
            else:
                temp[row+2][col]='W'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("Calculate 2 steps Forward move of white pikachu")
            # print(printable_board(temp))
            # print('\n')

         # Calculate jumpover 2 steps forward move of white pikachu
        if row<len(board)-2 and board[row+1][col] in ('b','B') and board[row+2][col]=='.':
            temp=copy.deepcopy(board)
            if row==len(board)-3:
                temp[row+2][col]='@'
            else:
                temp[row+2][col]='W'
            temp[row][col]='.'
            temp[row+1][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate jumpover 2 steps forward move of white pikachu")
            # print(printable_board(temp))
            # print('\n')

         # Calculate jumpover 3 steps forward move of white pikachu
        if (row<len(board)-3 and board[row+1][col] in ('b','B') and board[row+2][col]=='.' and board[row+3][col]=='.') or (row<len(board)-3 and board[row+1][col]=='.' and board[row+2][col] in ('b','B') and board[row+3][col]=='.'):
            temp=copy.deepcopy(board)
            if row==len(board)-4:
                temp[row+3][col]='@'
            else:
                temp[row+3][col]='W'
            temp[row][col]='.'
            temp[row+1][col]='.'
            temp[row+2][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate jumpover 3 steps forward move of white pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 1 step to right move of white pikachu
        if col<len(board)-1 and board[row][col+1]=='.':
            temp=copy.deepcopy(board)
            temp[row][col+1]='W'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 1 step to right move of white pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 2 steps to right move of white pikachu
        if col<len(board)-2 and board[row][col+1]=='.' and board[row][col+2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col+2]='W'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 steps to right move of white pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 2 step jumpover to right move of white pikachu
        if col<len(board)-2 and board[row][col+1] in ('b','B') and board[row][col+2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col+2]='W'
            temp[row][col+1]='.'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 step jumpover to right move of white pikachu")
            # print(printable_board(temp))
            # print('\n')


        #Calculate 3 steps jumpover to right move of white pikachu
        if (col<len(board)-3 and board[row][col+1] in ('b','B') and board[row][col+2]=='.' and board[row][col+3]=='.') or (col<len(board)-3 and board[row][col+1]=='.' and board[row][col+2] in ('b','B') and board[row][col+3]=='.'):
            temp=copy.deepcopy(board)
            temp[row][col+3]='W'
            temp[row][col]='.'
            temp[row][col+1]='.'
            temp[row][col+2]='.'
            pikachu_succ.append(temp)
            # print("#Calculate 3 steps jumpover to right move of white pikachu")
            # print(printable_board(temp))
            # print('\n')
            
        # Calculate 1 step to left move of white pikachu
        if col>0 and board[row][col-1]=='.':
            temp=copy.deepcopy(board)
            temp[row][col-1]='W'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 1 step to left move of white pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 2 steps to left of white pikachu
        if col>1 and board[row][col-1]=='.' and board[row][col-2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col-2]='W'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 steps to left of white pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 2 step jumpover to left of white pikachu
        if col>1 and board[row][col-1] in ('b','B') and board[row][col-2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col-2]='W'
            temp[row][col-1]='.'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 step jumpover to left of white pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 3 step jumpover to left of white pikachu
        if (col>2 and board[row][col-1] in ('b','B') and board[row][col-2]=='.' and board[row][col-3]=='.') or (col>2 and board[row][col-1]=='.' and board[row][col-2] in ('b','B') and board[row][col-3]=='.'):
            temp=copy.deepcopy(board)
            temp[row][col-3]='W'
            temp[row][col]='.'
            temp[row][col-1]='.'
            temp[row][col-2]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 3 step jumpover to left of white pikachu")
            # print(printable_board(temp))
            # print('\n')

    if player=='B':
        # print("Calculating SUCC for ({},{})".format(row,col))
         # Calculate 1 step Forward move of black pikachu
        if row>0 and board[row-1][col]=='.':
            temp=copy.deepcopy(board)
            if row==1:
                temp[row-1][col]='$'
            else:
                temp[row-1][col]='B'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 1 step Forward move of black pikachu")
            # print(printable_board(temp))
            # print('\n')      

         # Calculate 2 steps Forward move black pikachu
        if row>1 and board[row-1][col]=='.' and board[row-2][col]=='.':
            temp=copy.deepcopy(board)
            if row==2:
                temp[row-2][col]='$'
            else:
                temp[row-2][col]='B'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print(" Calculate 2 steps Forward move black pikachu")
            # print(printable_board(temp))
            # print('\n')  
        
         # Calculate jumpover 2 steps forward move of black pikachu
        if row>1 and board[row-1][col] in ('w','W') and board[row-2][col]=='.':
            temp=copy.deepcopy(board)
            if row==2:
                temp[row-2][col]='$'
            else:
                temp[row-2][col]='B'
            temp[row][col]='.'
            temp[row-1][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate jumpover 2 steps forward move of black pikachu")
            # print(printable_board(temp))
            # print('\n')

         # Calculate jumpover 3 steps forward move of black pichu
        if (row>2 and board[row-1][col] in ('w','W') and board[row-2][col]=='.' and board[row-3][col]=='.') or (row>2 and board[row-1][col]=='.' and board[row-2][col] in ('w','W') and board[row-3][col]=='.'):
            temp=copy.deepcopy(board)
            if row==3:
                temp[row-3][col]='$'
            else:
                temp[row-3][col]='B'
            temp[row][col]='.'
            temp[row-1][col]='.'
            temp[row-2][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate jumpover 3 steps forward move of black pichu")
            # print(printable_board(temp))
            # print('\n')
        
        # Calculate 1 step to right move of black pikachu
        if col<len(board)-1 and board[row][col+1]=='.':
            temp=copy.deepcopy(board)
            temp[row][col+1]='B'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 1 step to right move of black pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 2 steps to right move of black pikachu
        if col<len(board)-2 and board[row][col+1]=='.' and board[row][col+2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col+2]='B'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 steps to right move of black pikachu")
            # print(printable_board(temp))
            # print('\n')
           
        # Calculate 2 step jumpover to right of black pikachu
        if col<len(board)-2 and board[row][col+1] in ('w','W') and board[row][col+2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col+2]='B'
            temp[row][col+1]='.'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 step jumpover to right of black pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 3 steps jumpover to right of black pikachu
        if (col<len(board)-3 and board[row][col+1] in ('w','W') and board[row][col+2]=='.' and board[row][col+3]=='.') or (col<len(board)-3 and board[row][col+1]=='.' and board[row][col+2] in ('w','W') and board[row][col+3]=='.'):
            temp=copy.deepcopy(board)
            temp[row][col+3]='B'
            temp[row][col]='.'
            temp[row][col+1]='.'
            temp[row][col+2]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 3 steps jumpover to right of black pikachu")
            # print(printable_board(temp))
            # print('\n')
        
        # Calculate 1 step to left of black pikachu
        if col>0 and board[row][col-1]=='.':
            temp=copy.deepcopy(board)
            temp[row][col-1]='B'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 1 step to left of black pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 2 steps to left of black pikachu
        if col>1 and board[row][col-1]=='.' and board[row][col-2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col-2]='B'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 steps to left of black pikachu")
            # print(printable_board(temp))
            # print('\n')
        
        # Calculate 2 step jumpover to left of black pikachu
        if col>1 and board[row][col-1] in ('w','W') and board[row][col-2]=='.':
            temp=copy.deepcopy(board)
            temp[row][col-2]='B'
            temp[row][col-1]='.'
            temp[row][col]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 2 step jumpover to left of black pikachu")
            # print(printable_board(temp))
            # print('\n')

        # Calculate 3 step jumpover to left of black pikachu
        if (col>2 and board[row][col-1] in ('w','W') and board[row][col-2]=='.' and board[row][col-3]=='.') or (col>2 and board[row][col-1]=='.' and board[row][col-2] in ('w','W') and board[row][col-3]=='.'):
            temp=copy.deepcopy(board)
            temp[row][col-3]='B'
            temp[row][col]='.'
            temp[row][col-1]='.'
            temp[row][col-2]='.'
            pikachu_succ.append(temp)
            # print("# Calculate 3 step jumpover to left of black pikachu")
            # print(printable_board(temp))
            # print('\n')

    return pikachu_succ

# Calculate successors of raichu
def raichu_succ(board,player,row,col):
    raichu_succ=[]
    N = len(board)-1
    
    if player=='@':  
        # print("Calculating SUCC for ({},{})".format(row,col))
        # Calculate all forward moves of white raichu till pichu/pikachu/raichu is encaountered
        for i in range(row+1,len(board)):
            if board[i][col]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][col]='@'
                raichu_succ.append(temp)
                # print("# Calculate all forward moves of white raichu till pichu/pikachu/raichu is encaountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate all jump forward moves of white raichu when black pichu/pikachu/raichu is encaountered
        for i in range(row+1,len(board)):
                if board[i][col]=='.':
                    continue
                elif board[i][col] in ('b','B','$'):
                    
                    for j in range(i+1,len(board)):
                        if board[j][col]=='.':
                            temp=copy.deepcopy(board)
                            temp[j][col]='@'
                            temp[row][col]='.'
                            temp[i][col]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jump forward moves white when black pichu/pikachu/raichu is encaountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

        # Calculate all backward moves white raichu till pichu/pikachu/raichu is encaountered
        for i in range(row-1,-1,-1):
            if board[i][col]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][col]='@'
                raichu_succ.append(temp)    
                # print("# Calculate all backward moves till pichu/pikachu/raichu is encaountered")
                # print(printable_board(temp))
                # print('\n')

         # Calculate all jumpover backward moves white raichu when black pichu/pikachu/Raichu is encaountered
        for i in range(row-1,-1,-1):
                if board[i][col]=='.':
                    continue
                elif board[i][col] in ('b','B','$'):
                    
                    for j in range(i-1,-1,-1):
                        if board[j][col]=='.':
                            temp=copy.deepcopy(board)
                            temp[j][col]='@'
                            temp[row][col]='.'
                            temp[i][col]='.'
                            raichu_succ.append(temp)
                            # print("Calculate all jump backward moves when pichu/pikachu is encaountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
         
        # Calculate all right moves of white raichu till pichu/pikachu/raichu is encountered 
        for i in range(col+1,len(board)):
            if board[row][i]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[row][i]='@'
                raichu_succ.append(temp)    
                # print("# Calculate all right moves till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate all jumpover right moves white when black pichu/pikachu/Raichu is encountered
        for i in range(col+1,len(board)):
                if board[row][i]=='.':
                    continue
                elif board[row][i] in ('b','B','$'):
                    
                    for j in range(i+1,len(board)):
                        if board[row][j]=='.':
                            temp=copy.deepcopy(board)
                            temp[row][j]='@'
                            temp[row][col]='.'
                            temp[row][i]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jump right moves when pichu/pikachu/Raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

        # Calculate all left moves white raichu till pichu/pikachu/raichu is encountered 
        for i in range(col-1,-1,-1):
            if board[row][i]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[row][i]='@'
                raichu_succ.append(temp)    
                # print("# Calculate all left moves till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate all jumpover left moves of white raichu when pichu/pikachu/Raichu is encountered
        for i in range(col-1,-1,-1):
                if board[row][i]=='.':
                    continue
                elif board[row][i] in ('b','B','$'):
                    
                    for j in range(i-1,-1,-1):
                        if board[row][j]=='.':
                            temp=copy.deepcopy(board)
                            temp[row][j]='@'
                            temp[row][col]='.'
                            temp[row][i]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jump left moves when pichu/pikachu/Raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate top right diagonal moves of white raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col+1,len(board))):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='@'
                raichu_succ.append(temp)    
                # print("# Calculate top right diagonal moves of white raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate top right diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col+1,len(board))):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('b','B','$'):
                    
                    for k,l in zip(range(i-1,-1,-1),range(j+1,len(board))):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='@'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jump right moves when pichu/pikachu/Raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate bottom right diangonal moves of white raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board))):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='@'
                raichu_succ.append(temp)    
                # print("# Calculate bottom right diangonal moves of white raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate bottom right diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board))):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('b','B','$'):
                    
                    for k,l in zip(range(i+1,len(board)),range(j+1,len(board))):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='@'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate bottom right diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate top left diangonal moves of white raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col-1,-1,-1)):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='@'
                raichu_succ.append(temp)    
                # print("# Calculate top left diangonal moves of white raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate top left diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('b','B','$'):
                    
                    for k,l in zip(range(i-1,-1,-1),range(j-1,-1,-1)):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='@'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate top left diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate bottom left diangonal moves of white raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col-1,-1,-1)):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='@'
                raichu_succ.append(temp)    
                # print("# Calculate bottom left diangonal moves of white raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate bottom left diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col-1,-1,-1)):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('b','B','$'):
                    
                    for k,l in zip(range(i+1,len(board)),range(j-1,-1,-1)):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='@'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate bottom left diangonal jumpover moves of white raichu after black pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

    if player=='$':
        # print("Calculating SUCC for ({},{})".format(row,col))
        # Calculate all forward moves of black raichu till black/white pichu/pikachu/raichu is encaountered
        for i in range(row-1,-1,-1):
            if board[i][col]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][col]='$'
                raichu_succ.append(temp)

                # print("# Calculate all forward moves of black raichu till white pichu/pikachu/raichu is encaountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate all forward jumpover moves of black raichu when white pichu/pikachu/raichu is encaountered
        for i in range(row-1,-1,-1):
                if board[i][col]=='.':
                    continue
                elif board[i][col] in ('w','W','@'):
                    
                    for j in range(i-1,-1,-1):
                        if board[j][col]=='.':
                            temp=copy.deepcopy(board)
                            temp[j][col]='$'
                            temp[row][col]='.'
                            temp[i][col]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all forward jumpover moves of black raichu when white pichu/pikachu/raichu is encaountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

        # Calculate all backward moves of black raichu till pichu/pikachu/raichu is encaountered
        for i in range(row+1,len(board)):
            if board[i][col]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][col]='$'
                raichu_succ.append(temp)

                # print("# Calculate all backward moves of black raichu till pichu/pikachu/raichu is encaountered")
                # print(printable_board(temp))
                # print('\n')

         # Calculate all jump backward moves of black raichu when white pichu/pikachu/Raichu is encaountered
        for i in range(row+1,len(board)):
                if board[i][col]=='.':
                    continue
                elif board[i][col] in ('w','W','@'):
                    
                    for j in range(i+1,len(board)):
                        if board[j][col]=='.':
                            temp=copy.deepcopy(board)
                            temp[j][col]='$'
                            temp[row][col]='.'
                            temp[i][col]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jump backward moves of black raichu when white pichu/pikachu/Raichu is encaountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

        # Calculate all right moves of black raichu till pichu/pikachu/raichu is encountered 
        for i in range(col+1,len(board)):
            if board[row][i]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[row][i]='$'
                raichu_succ.append(temp)    
                # print("## Calculate all right moves of black raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate all jumpover right moves of blach pichu when white pichu/pikachu/Raichu is encountered
        for i in range(col+1,len(board)):
                if board[row][i]=='.':
                    continue
                elif board[row][i] in ('w','W','@'):
                    
                    for j in range(i+1,len(board)):
                        if board[row][j]=='.':
                            temp=copy.deepcopy(board)
                            temp[row][j]='$'
                            temp[row][col]='.'
                            temp[row][i]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jumpover right moves of blach pichu when white pichu/pikachu/Raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

        # Calculate all left moves of black raichu till pichu/pikachu/raichu is encountered 
        for i in range(col-1,-1,-1):
            if board[row][i]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[row][i]='$'
                raichu_succ.append(temp)    
                # print("# Calculate all left moves of black raichu till pichu/pikachu/raichu is encountered ")
                # print(printable_board(temp))
                # print('\n')

        # Calculate all jumpover left moves black when white pichu/pikachu/Raichu is encountered
        for i in range(col-1,-1,-1):
                if board[row][i]=='.':
                    continue
                elif board[row][i] in ('w','W','@'):
                    
                    for j in range(i-1,-1,-1):
                        if board[row][j]=='.':
                            temp=copy.deepcopy(board)
                            temp[row][j]='$'
                            temp[row][col]='.'
                            temp[row][i]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate all jumpover left moves black when white pichu/pikachu/Raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

        # Calculate top right diagonal moves of black raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col+1,len(board))):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='$'
                raichu_succ.append(temp)    
                # print("# Calculate top right diagonal moves of black raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate top right diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col+1,len(board))):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('w','W','@'):
                    
                    for k,l in zip(range(i-1,-1,-1),range(j+1,len(board))):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='$'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate top right diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate bottom right diangonal moves of black raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board))):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='$'
                raichu_succ.append(temp)    
                # print("# Calculate bottom right diangonal moves of black raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate bottom right diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board))):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('w','W','@'):
                    
                    for k,l in zip(range(i+1,len(board)),range(j+1,len(board))):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='$'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate bottom right diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate top left diangonal moves of black raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col-1,-1,-1)):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='$'
                raichu_succ.append(temp)    
                # print("# Calculate top left diangonal moves of black raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate top left diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered
        for i,j in zip(range(row-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('w','W','@'):
                    
                    for k,l in zip(range(i-1,-1,-1),range(j-1,-1,-1)):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='$'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate top left diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break
        
        # Calculate bottom left diangonal moves of black raichu till pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col-1,-1,-1)):
            if board[i][j]!='.':
                break
            else:
                temp=copy.deepcopy(board)
                temp[row][col]='.'
                temp[i][j]='$'
                raichu_succ.append(temp)    
                # print("# Calculate bottom left diangonal moves of black raichu till pichu/pikachu/raichu is encountered")
                # print(printable_board(temp))
                # print('\n')

        # Calculate bottom left diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered
        for i,j in zip(range(row+1,len(board)),range(col-1,-1,-1)):
                if board[i][j]=='.':
                    continue
                elif board[i][j] in ('w','W','@'):
                    
                    for k,l in zip(range(i+1,len(board)),range(j-1,-1,-1)):
                        if board[k][l]=='.':
                            temp=copy.deepcopy(board)
                            temp[k][l]='$'
                            temp[row][col]='.'
                            temp[i][j]='.'
                            raichu_succ.append(temp)
                            # print("# Calculate bottom left diangonal jumpover moves of black raichu after white pichu/pikachu/raichu is encountered")
                            # print(printable_board(temp))
                            # print('\n')

                        else:
                            break             
                break

    return raichu_succ

# Calculate successors of the initial state
def succ(board,player):
    if player=='w':
        pichu_succ_w=[]
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                if board[i][j]=='w':
                    pichu_succ_w= pichu_succ_w + pichu_succ(board,'w',i,j)
        return pichu_succ_w

    elif player=='W':
        pikachu_succ_W=[]
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                if board[i][j]=='W':
                    pikachu_succ_W=pikachu_succ_W + pikachu_succ(board,'W',i,j)
        return pikachu_succ_W

    elif player=='@':
        raichu_succ_wW=[]
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                if board[i][j]=='@':
                    raichu_succ_wW= raichu_succ_wW + raichu_succ(board,'@',i,j)
        return raichu_succ_wW
    
    elif player=='b':
        pichu_succ_b=[]
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                if board[i][j]=='b':
                    pichu_succ_b=pichu_succ_b + pichu_succ(board,'b',i,j)
        return pichu_succ_b

    elif player=='B':
        pikachu_succ_B=[]
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                if board[i][j]=='B':
                    pikachu_succ_B= pikachu_succ_B + pikachu_succ(board,'B',i,j)
        return pikachu_succ_B

    elif player=='$':
        raichu_succ_bB=[]
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                if board[i][j]=='$':
                    raichu_succ_bB= raichu_succ_bB + raichu_succ(board,'$',i,j)
        return raichu_succ_bB
          
# Check if give state is a terminal state
def is_terminal_state(board):
    w_count=0
    W_count=0
    w_raichu_count=0
    b_count=0
    B_count=0
    b_raichu_count=0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]=='w':
                w_count+=1
            elif board[i][j]=='W':
                W_count+=1
            elif board[i][j]=='@':
                w_raichu_count+=1
            elif board[i][j]=='b':
                b_count+=1
            elif board[i][j]=='B':
                B_count+=1
            elif board[i][j]=='$':
                b_raichu_count+=1

    if (w_count + W_count + w_raichu_count)==0:
        return True
    elif (b_count + B_count + b_raichu_count)==0:
        return True
    else:
        return False

# Evaluation function
def eval_board(board,players):

    w_count=0
    W_count=0
    w_raichu_count=0
    b_count=0
    B_count=0
    b_raichu_count=0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]=='w':
                w_count+=1
            elif board[i][j]=='W':
                W_count+=1
            elif board[i][j]=='@':
                w_raichu_count+=1
            elif board[i][j]=='b':
                b_count+=1
            elif board[i][j]=='B':
                B_count+=1
            elif board[i][j]=='$':
                b_raichu_count+=1

    val = 200*(w_raichu_count-b_raichu_count) + 50*(W_count-B_count) + 5*(w_count-b_count)
    if 'w' in players:
        return val
    else:
        return -val

# Calculate all the successors of min/max state
def successor_min_max(board,min_max_players):
    successors=[]
    # print("min_max_players: ",min_max_players)
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] in min_max_players:
                if board[i][j]=='w':
                    successors= successors + pichu_succ(board,'w',i,j)
                if board[i][j]=='W':
                    successors= successors + pikachu_succ(board,'W',i,j)
                if board[i][j]=='@':
                    successors= successors + raichu_succ(board,'@',i,j)
                if board[i][j]=='b':
                    successors= successors + pichu_succ(board,'b',i,j)
                if board[i][j]=='B':
                    successors= successors + pikachu_succ(board,'B',i,j)
                if board[i][j]=='$':
                    successors= successors + raichu_succ(board,'$',i,j)
    return successors                       

# Min player function
def min(board,max_players,min_players,depth,alpha, beta):
    if is_terminal_state(board): 
        return 9999 # return big value as we want max player to pick this state as the next step
    elif depth==0:
        return eval_board(board,max_players)

    min_val = 999999
    for s in successor_min_max(board,min_players):
        # print(s)
        val = max(s,max_players,min_players,depth-1,alpha,beta)
        if val<min_val:
            min_val=val
        if min_val < beta:
            beta = min_val
        if min_val <= alpha:
            return min_val
    return min_val

# Max player function
def max(board,max_players,min_players,depth,alpha, beta):
    if is_terminal_state(board):
        return -9999 # return very small value as we want min player to pick this state as the next step
    elif depth==0:
        return eval_board(board,min_players)
    
    max_val = -999999
    for s in successor_min_max(board,max_players):
        # print(s)   
        val = min(s,max_players,min_players,depth-1,alpha,beta)   
        if val > max_val:
            max_val=val
        if max_val > alpha:
            alpha = max_val

        if max_val >= beta:
            return max_val
    return max_val

def find_best_move(board, N, player, timelimit):
    
    board_list=[]
    count=0
    temp_list=[]
    # Converting the given board string into a list of lists
    for itm in board:
        temp_list.append(itm)
        count+=1
        while(count==N):
            board_list.append(temp_list)
            count=0
            temp_list=[]
    
    
    if player in ('w','W','@'):
        min_players=['b','B','$']
        max_players=['w','W','@']
    elif player in ('b','B','$'):
        min_players=['w','W','@']
        max_players=['b','B','$']

    depth = 2
    max_val = -999999
    max_move = None
    alpha = -999999
    beta = 999999
    # Calculate initial layer of successors based on the player provided
    for s in successor_min_max(board_list,max_players):
        # print(s,"\n")
        val = min(s,max_players,min_players,depth, alpha, beta)
        if val > max_val:
            max_val=val
            max_move=s

    # print(printable_board(max_move))
    
    return ''.join(''.join(row) for row in max_move)
        
    # succ(board_list,player)
        

if __name__ == "__main__":

    start_time = time.time()
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wbWB@$":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    
    
    new_board = find_best_move(board, N, player, timelimit)
    print("TIME TAKEN TO RUN PROGRAM: ",time.time()-start_time)
    print(new_board)
    
    # for new_board in find_best_move(board, N, player, timelimit):
    #     print(new_board)


