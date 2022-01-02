**Part 1: Raichu**
-----------------------------------------------------------------------------------------------------------------------

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


**Part 2: The Game of Quintris**
-----------------------------------------------------------------------------------------------------------------------
First we need to find all the possible moves that can be performed for a given state of the game.To find out all possible moves we need to find out all possible rotations and horizontal flips that can be performed on the current piece. For every operation on the current piece we need to find all possible positions of the piece on the board. We need to do the same for the next piece. Then we choose the state with minimum cost. The cost is calculated by the heuristic_function() function.<br>

For selecting the successor with minimum priority I am using priority queue with cost as the priority.

For evaluating cost we are considering the following factors:


- Holes: A hole is defined as an empty space such that there is at least one tile in the same column above it. We need to minimize this parameter.

- Aggregate height: It is the sum of the height of each column (the distance from the highest tile in each column to the bottom of the grid). We need to minimize this parameter. 

- Bumpiness: Bumpiness is the difference between the height of consecutive columns. We need to minimize this parameter.

- Score: It is the number of rows that are completed on choosing this state as successor. We need to maximize this parameter.

The Coefficients are decided using trial and error method. The basic idea of the range for trial and error was taken from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/. 




**Part 3: Truth be Told**
-----------------------------------------------------------------------------------------------------------------------

So,First we have a train data and test data.
Train data consist of labels,objects which are basically reviews for the hotels and classes like Truthful and Deceptive
We have to classify are those reviews truthful or just deceptive.

With the Help of train data we can train our model that we could use on test data to find labels.
As for each sentence,label is given so we divided the train data objects into 2 parts, Deceptive and Truthful objects.
We then took the words present in deceptive and find the probability for each word.
Similarly, We did with Truthful data we find the Probability of each word.
But Before Finding the Probability we first cleaned the data by removing any punctuation,converting the sentences in lower cases and other.
This is because this increases the accuracy of prediction.

After finding the probability of each word, we take the test data which only consists of objects whose labels we have to predict.
We will take each review, Divide it into bag of words.Then we add log probability of each word and calculate total log probability for each sentence.
we calculate total log probability of each sentence with respect to probabilities that are taken from deceptive,that is Total deceptive log probability of each review
similarly we calculate total truthful log probability of the review.If the total log probability for the deceptive is greater than the truthful
we could consider the review as deceptive otherwise it is truthful.

P (Deceptive|w1, w2, ..., wn) > P (Truthful|w1, w2, ..., wn)  The label is Deceptive
P (Deceptive|w1, w2, ..., wn) < P (Truthful|w1, w2, ..., wn)  The label is Truthful

we took log here because the probabilities were very low,so log function would provide better results and as we took the log probability we added the probability instead of multiplication
because of function of log.

if 
Log(P(w1|Deceptive))+log(P(w2|Deceptive))+log(P(w3|Deceptive))+.....>Log(P(w1|Truthful))+log(P(w2|Truthful))+log(P(w3|Truthful))+.....

The label is Deceptive

otherwise 

The label is Truthful


Finally, We stored the labels in list and returned the list to get accuracy.



