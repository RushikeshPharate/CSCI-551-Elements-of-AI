###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids:Sarvesh Ragade Paritosh Sabade Rushikesh pharate
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
from collections import defaultdict


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!

    def posterior(self, model, sentence, label):

        #Calculating log of the posterior probability of a given sentence for Simple
        if model == "Simple":
            postr = 1
            for i in range(len(sentence)):
                if sentence[i] not in self.emissionprob[label[i]]:
                    self.emissionprob[label[i]][sentence[i]] = 10**-20
                postr *= self.emissionprob[label[i]][sentence[i]]
            return math.log(postr)

        #Calculating log of the posterior probability of a given sentence for HMM

        elif model == "HMM":
            postr = 1
            for i in range(len(sentence)):
                if sentence[i] not in self.emissionprob[label[i]]:
                    self.emissionprob[label[i]][sentence[i]] = 10**-20

                if i==0:
                    postr *= self.emissionprob[label[i]][sentence[i]]
                else:
                    postr *= self.emissionprob[label[i]][sentence[i]]*self.transionprob[(label[i-1],label[i])]

            try:
                p = math.log(postr)

            except:

                p = 1

            return p

        #Calculating log of the posterior probability of a given sentence for Complex


        elif model == "Complex":
            postr = 1
            for i in range(len(sentence)):
                if sentence[i] not in self.emissionprob[label[i]]:
                    self.emissionprob[label[i]][sentence[i]] = 10**-20

                if i == 0:
                    postr *= self.emissionprob[label[i]][sentence[i]]
                elif i==1:
                    postr *= self.emissionprob[label[i]][sentence[i]] * self.transionprob[(label[i - 1], label[i])]
                else:
                    postr *= self.emissionprob[label[i]][sentence[i]] * self.transionprob[(label[i - 1], label[i])]*self.transionprob[(label[i - 2], label[i])]

            try:
                p=math.log(postr)

            except:

                p=1

            return p

        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):

        words=[]
        self.wordct={}
        labels=[]
        self.labels = ['det', 'noun', 'adj', 'verb', 'adp', '.', 'adv', 'conj', 'prt', 'pron', 'num', 'x']
        self.labelct = {'adj': 0,
             'adv': 0,
             'adp': 0,
             'conj': 0,
             'det': 0,
             'noun': 0,
             'num': 0,
             'pron': 0,
             'prt': 0,
             'verb': 0,
             'x': 0,
             '.': 0}

        self.datatble = defaultdict(dict)
        self.transct = {}
        self.initct = {}

        #Making a list of words and labels

        for line in data:
            for i in range(len(line[0])):
                words.append(line[0][i])
                labels.append(line[1][i])

        #Calculating Word Count

        for word in words:
            if word in self.wordct:
                self.wordct[word] = 1
            else:
                self.wordct[word] = 1

        #Calculating label Count

        for label in labels:
            self.labelct[label]+=1

        #Calculating Intial Count of the Label

        for line in data:
            label = line[1][0]
            if label not in self.initct:
                self.initct[label] = 1
            else:
                self.initct[label] += 1

        #Making a table with words in each label count

        for line in data:
            for i in range(len(line[0])):
                word = line[0][i]
                label = line[1][i]
                if word not in self.datatble[label]:
                   self.datatble[label][word] = 1
                else:
                   self.datatble[label][word] += 1

        #Calculating Transition Count


        for line in data:
            prevlbl = "noun"
            N=len(line[1])
            t=[]

            for j in range(0, N):
                label = line[1][j]
                t.append((prevlbl, label))
                prevlbl = label

            for i in range(len(t)):
                if t[i] not in self.transct:
                    self.transct[t[i]] = 1
                else:
                    self.transct[t[i]] += 1

        list3 = []
        for x in self.labels:
            for y in self.labels:
                list3.append((x, y))

        for i in list3:
            if i not in self.transct:
                self.transct[i] = min(self.transct.values())




        self.transionprob = {}
        self.emissionprob = defaultdict(dict)
        self.intialprob = {}


        # Emission probability Calculation

        for label in self.datatble:
                totalcx = sum(self.datatble[label].values())
                for word in self.datatble[label]:
                    self.emissionprob[label][word] = float(self.datatble[label][word] / totalcx)


        # Intial probability Calculation
        totalcx = sum(self.initct.values())
        for i in self.initct:
            self.intialprob[i] = float(self.initct[i] / totalcx)

        # Transmission Probability Calculation
        lablx = {'adj': 0,
             'adv': 0,
             'adp': 0,
             'conj': 0,
             'det': 0,
             'noun': 0,
             'num': 0,
             'pron': 0,
             'prt': 0,
             'verb': 0,
             'x': 0,
             '.': 0}

        for i in self.transct:
            lablx[i[0]] += self.transct[i]
        for j in self.transct:
            self.transionprob[j] = float(self.transct[j] / lablx[j[0]])


        pass

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        pos = []
        for word in sentence:
            tempmax = 0
            labelx = "noun"
            for label in self.labels:
                if word in self.emissionprob[label]:
                    if self.emissionprob[label][word] > tempmax  :
                        tempmax = self.emissionprob[label][word]
                        labelx = label
                    else:
                        labelx=labelx
            pos.append(labelx)
        return pos
        # return [ "noun" ] * len(sentence)

    
    #For Code of Viterbi I have taken Reference from Professor David Crandall Viterbi Code Given During Inclass Activity 2 on Viterbi

    def hmm_viterbi(self, sentence):

        fxdict={}

        N=len(sentence)

        #Intialising viterbi Table

        V_table = {'adj': [0]*N,
             'adv': [0]*N,
             'adp': [0]*N,
             'conj': [0]*N,
             'det': [0]*N,
             'noun': [0]*N,
             'num': [0]*N,
             'pron': [0]*N,
             'prt': [0]*N,
             'verb': [0]*N,
             'x': [0]*N,
             '.': [0]*N}

        which_table = {'adj': [0] * N,
                   'adv': [0] * N,
                   'adp': [0] * N,
                   'conj': [0] * N,
                   'det': [0] * N,
                   'noun': [0] * N,
                   'num': [0] * N,
                   'pron': [0] * N,
                   'prt': [0] * N,
                   'verb': [0] * N,
                   'x': [0] * N,
                   '.': [0] * N}

        for s in self.labels:
            if sentence[0] not in self.emissionprob[s]:
                self.emissionprob[s][sentence[0]]=1e-10
            V_table[s][0] = self.intialprob[s] * self.emissionprob[s][sentence[0]]
        for i in range(1, N):
            for s in self.labels:
                if sentence[i] not in self.emissionprob[s]:
                    self.emissionprob[s][sentence[i]] = 1e-10

                (which_table[s][i], V_table[s][i]) = max([(s0, V_table[s0][i - 1] *
                                                           self.transionprob[(s0,s)]) for s0 in self.labels], key=lambda l: l[1])
                V_table[s][i] *= self.emissionprob[s][sentence[i]]

        i=N-1

        viterbi_seq = [""] * N
        for s in self.labels:
            fxdict[s]=V_table[s][i]

        #Calculating Maximum

        max_key = max(fxdict, key=fxdict.get)

        #Finding the sequence

        viterbi_seq[N - 1] = max_key
        for j in range(N - 2, -1, -1):
            viterbi_seq[j] = which_table[viterbi_seq[j + 1]][j + 1]
        
        #Returning the Viterbi Sequence after Calculation


        return viterbi_seq
        # return [ "noun" ] * len(sentence)

    def complex_mcmc(self, sentence):

        intseq=[ "noun" ] * len(sentence)
        samplist=[]

        #Running for 200 Iterations
        for itr in range(200):
            for i in range(len(sentence)):
                cmcmc={}
                for pos in self.labels:
                    word=sentence[i]

                    #Calculating probabilities for 0,1 and remaining according the structure

                    if  i==0:
                        prob = self.emissionprob[pos][word] * self.intialprob[pos]
                    elif i==1:
                        prob = self.emissionprob[pos][word] * self.transionprob[(intseq[i - 1],pos)]
                    else:
                        prob = self.emissionprob[pos][word] * self.transionprob[(intseq[i - 1],pos)] * self.transionprob[(intseq[i - 2],pos)]

                    cmcmc[pos] = prob

                #Calculating sum and normalising

                totalv = sum(cmcmc.values())
                if totalv != 0:
                    for k in cmcmc.keys():
                        cmcmc[k] = float(cmcmc[k] / totalv)


                for j in range(20):
                    # Taking Random to compare with probability
                    rprob = random.random()  
                    postemp = 'noun'
                    for poskey, probval in cmcmc.items():
                        if probval > rprob:
                            postemp = poskey
                            break
                        else:
                            postemp = 'noun'
                    j+=1

                intseq[i] = postemp
            samplist.append(intseq)


        list5=[]

        for i in range(len(sentence)):
            list4 = []
            for j in range(len(samplist)):
                list4.append(samplist[j][i])

            gibbspos = {'adj': 0,
                        'adv': 0,
                        'adp': 0,
                        'conj': 0,
                        'det': 0,
                        'noun': 0,
                        'num': 0,
                        'pron': 0,
                        'prt': 0,
                        'verb': 0,
                        'x': 0,
                        '.': 0}

            for label in list4:
                gibbspos[label]+=1

            maxkey=max(gibbspos,key=gibbspos.get)
            list5.append(maxkey)

        # print(list5)

        #returning list of pos we calculated

        return list5
        # return [ "noun" ] * len(sentence)



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
