#!/usr/bin/python
"""
Perform optical character recognition, usage:
    python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png

Authors: Rushikesh Pharate
(based on skeleton code by D. Crandall, Oct 2020)


As we need to implement HMM, I started with calculating transition, emission and initial probabilities for each word in the training set.
I had created a dict (word_freq) with each word as key  and value of that key is a another dict with keys as {'count':1,'initial_count':0,'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0}.
I was using the count key for calculating prior probability , initial_count key to calculate initial probability of that particular word and other keys to calculate emission probabilities for each label for each word. 
For transition probability i had made as 12*12 dict of dict (you can see it in the code). here i was calculating probability of NOUN->NOUN, NOUN->ADJ, NOUN->CONJ basically every possible transition of pos. initially i thaught it wil be needed for Viterbi. But, spending so much time on this i realised this will not help :). I have kept my code for this part in the file. Please check calculate_probabilities function to check it out.

After that, i started again, this time i wanted to implement bayes net first and then move to viterbi. I completed the implementation for bayes net but accuracy was not that great.For test_image-0_0 i was getting below output -->Simple: SUPREME CQURT?QEjTHE UNITEDpSTATES. As you can see accuracy was not that great. I experimented a lot to increase the accurecy like taking into account black_non_matched pixels, whites pixels but it didn't increase the accuracy when the image had a lot of noise. So, after a lot of experimentation with assigning weights for emmision probability i observerd that when the input image has a lot of noise then  assigning more weight for black_matched pixels gives accurate results and when the pixel density is less then assigning slightly less weight to back_match pixels gives accurate results. So I have incorporated this logic for getting different emission prob based on the density of the image. 

For viterbi I started with calculating emission probabilities and initial probabilities based on the training data. Viterbi seemed very hard and i was not able to do it. I watched the module for viterbi once again but still was not able to clearly think how to implement it. One of my teammate told me about the viterbi code provided by Prof. David in one of the in class activity. So, i looked at the code and implemented similar logic for my problem and it worked !! (I was so happy ;) ). I got some issues like probabilities mutplications were giving 0 ans, string was not correct etc but i was able to fix everything and now getting a decent output.

First letter of the string is getting printed wrong somehow. I looked at my logic for calculating initial_probabilities and made few changes but still not able to get correct ans for first letter. I don't know what to do for that part

For all the test images provided (0-19) i am able to get accuracy of over 90% (I think) and I'm happy with it.

"""


import time
from PIL import Image, ImageDraw, ImageFont
import sys
import copy
from math import log

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    # print(im.size)
    # print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }


def calculate_probilities(fname):
    f = open(fname,'r')
    word_freq={}
    
    total_words = 0 # to count the total number of words in the training file apart from the labels. We will need this to calculate prior probability
    total_statements = 0 # to count total statement. This will be needed to calculate initial probabilities.

    # variables for keping count of the labels
    total_adj = 0
    total_adv = 0
    total_adp = 0
    total_conj = 0
    total_det = 0
    total_noun = 0
    total_num = 0
    total_pron = 0
    total_prt = 0
    total_verb = 0
    total_x = 0
    total_dot = 0


    labels = ['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
    init_prob={'count':1,'initial_count':0,'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0}
    # init_prob={'count':1}
    for line in f:
        lst = line.split()
        
        for i in range(len(lst)-1):
            # lst[i]
            if lst[i] in labels:
                # skip this iteration of loop as the current word is a label
                continue
            if not lst[i].lower() in word_freq.keys(): # if the word is not present in the dict as a key then insert it as a key and assign default values
                temp = copy.deepcopy(init_prob)
                if i==0:
                    temp['initial_count'] = temp['initial_count'] + 1  # for first word of the current statement, increase count by 1
                    total_statements = total_statements + 1
                label = lst[i+1] # Get label of the current word
                if label in labels:
                    temp[label] =  temp[label] + 1
                    if label == 'ADJ':
                        total_adj += 1
                    elif label == 'ADV':
                        total_adv += 1
                    elif label == 'ADP':
                        total_adp += 1
                    elif label == 'CONJ':
                        total_conj += 1
                    elif label == 'DET':
                        total_det += 1
                    elif label == 'NOUN':
                        total_noun += 1
                    elif label == 'NUM':
                        total_num += 1
                    elif label == 'PRON':
                        total_pron += 1
                    elif label == 'PRT':
                        total_prt += 1
                    elif label == 'VERB':
                        total_verb += 1
                    elif label == 'X':
                        total_x += 1
                    elif label == '.':
                        total_dot += 1

                word_freq[lst[i].lower()] = temp
                total_words += 1
            else:
                temp  = word_freq[lst[i].lower()]
                temp['count'] = temp['count'] + 1
                if i==0:
                    temp['initial_count'] = temp['initial_count'] + 1 
                    total_statements = total_statements + 1
                label = lst[i+1]
                if label in labels:
                    temp[label] =  temp[label] + 1
                    if label == 'ADJ':
                        total_adj += 1
                    elif label == 'ADV':
                        total_adv += 1
                    elif label == 'ADP':
                        total_adp += 1
                    elif label == 'CONJ':
                        total_conj += 1
                    elif label == 'DET':
                        total_det += 1
                    elif label == 'NOUN':
                        total_noun += 1
                    elif label == 'NUM':
                        total_num += 1
                    elif label == 'PRON':
                        total_pron += 1
                    elif label == 'PRT':
                        total_prt += 1
                    elif label == 'VERB':
                        total_verb += 1
                    elif label == 'X':
                        total_x += 1
                    elif label == '.':
                        total_dot += 1

                word_freq[lst[i].lower()] = temp
                total_words += 1

    # print(word_freq)
    
    # print("Adj: ",total_adj)
    # print("Adv: ",total_adv)
    # print("Adp: ",total_adp)
    # print("Conj: ",total_det)
    # print("Det: ",total_det)
    # print("Nouns: ",total_noun)
    # print("Num: ",total_num)
    # print("Pron: ",total_pron)
    # print("prt: ",total_prt)
    # print("Verb: ",total_verb)
    # print("X: ",total_x)
    # print(".: ",total_dot)

    for key, value in word_freq.items():
        for value_key in value.keys():
            if value_key not in ('count','initial_count'):
                # value[value_key] = value[value_key]/value['count'] 
                if value_key == 'ADJ' and total_adj>0:
                    value[value_key] = value[value_key]/total_adj
                elif value_key == 'ADV' and total_adv>0:
                    value[value_key] = value[value_key]/total_adv
                elif value_key == 'ADP' and total_adp>0:
                    value[value_key] = value[value_key]/total_adp
                elif value_key == 'CONJ' and total_conj>0:
                    value[value_key] = value[value_key]/total_conj
                elif value_key == 'DET' and total_det>0:
                    value[value_key] = value[value_key]/total_det
                elif value_key == 'NOUN' and total_noun>0:
                    value[value_key] = value[value_key]/total_noun
                elif value_key == 'NUM' and total_num>0:
                    value[value_key] = value[value_key]/total_num
                elif value_key == 'PRON' and total_pron>0:
                    value[value_key] = value[value_key]/total_pron
                elif value_key == 'PRT' and total_prt>0:
                    value[value_key] = value[value_key]/total_prt
                elif value_key == 'VERB' and total_verb>0:
                    value[value_key] = value[value_key]/total_verb
                elif value_key == 'X' and total_x>0:
                    value[value_key] = value[value_key]/total_x
                elif value_key == '.' and total_dot>0:
                    value[value_key] = value[value_key]/total_dot
        value['count'] = value['count']/total_words
        value['initial_count'] = value['initial_count']/total_statements

    f.close()
    # print(word_freq)

    """   Below code is for calculating transition_prob  """ 

    f = open(fname,'r')
    # dict for storing each combination of transition prob
    transition_prob={'ADJ':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'ADV':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'ADP':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'CONJ':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'DET':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'NOUN':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'NUM':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'PRON':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'PRT':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'VERB':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    'X':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0},
    '.':{'ADJ':0,'ADV':0,'ADP':0,'CONJ':0,'DET':0,'NOUN':0,'NUM':0,'PRON':0,'PRT':0,'VERB':0,'X':0,'.':0}
    }

    labels = ['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
    
    # init_prob={'count':1}
    for line in f:
        lst = line.split()
        for i in range(len(lst)-1):
            # lst[i]
            if lst[i] in labels:

                # Find next label
                for j in range(i+1,len(lst)): 
                    if lst[j] in labels:
                        break
                # Increase count only when word returned by j is label         
                if lst[j] in labels:         
                    next_label_counts = transition_prob[lst[i]]
                    next_label_counts[lst[j]] += 1
    
    # print(transition_prob)

    for key, value in transition_prob.items():
    
        if key == 'ADJ' and total_adj>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_adj
        elif key == 'ADV' and total_adv>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_adv
        elif key == 'ADP' and total_adp>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_adp
        elif key == 'CONJ' and total_conj>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_conj
        elif key == 'DET' and total_det>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_det
        elif key == 'NOUN' and total_noun>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_noun
        elif key == 'NUM' and total_num>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_num
        elif key == 'PRON' and total_pron>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_pron
        elif key == 'PRT' and total_prt>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_prt
        elif key == 'VERB' and total_verb>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_verb
        elif key == 'X' and total_x>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_x
        elif key == '.' and total_dot>0:
            for value_key in value.keys():
                value[value_key] = value[value_key]/total_dot
              
    return word_freq, transition_prob


def cal_initial_prob(fname):

    f = open(fname,'r')

    initial_prob = {}
    total_lines = 0
    labels = ['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']

    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for line in f:
        # words = line.split()
        # print(line)
        # print(words)
        # print('\n')

        total_lines += 1
        for i in range(len(line)):
            if line[i] in TRAIN_LETTERS:
                # print(line[i])
                initial_prob[line[i]] = initial_prob.get(line[i],0) + 1
                break

    # print(initial_prob)
    for key in initial_prob.keys():
        initial_prob[key] = initial_prob[key]/total_lines 

    f.close()
    return initial_prob


def cal_transition_prob(fname):

    f = open(fname,'r')

    transition_prob = {}
    total_lines = 0
    labels = ['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
    for line in f:
        words = line.split()
        # print(line)
        # print(words)
        # print('\n')

        total_lines += 1
        
        for i in range(len(words)-1):
            # lst[i]
            if words[i] in labels:
                # skip this iteration of loop as the current word is a label
                continue

            curr_word = words[i]

            for char_num in range(0,len(curr_word)):
                # print(curr_word[char_num],'\n')
                if char_num == 0:
                    transition_prob[curr_word[0]] = transition_prob.get(curr_word[0],{})
                    # transition_prob[" "][curr_word[0]] = transition_prob.get(" ",{}).get(curr_word[char_num],0) + 1

                    # For first letter of the word adding transition prob from " " (trans_pob(" "=> first letter of the word)
                    if " " not in transition_prob:
                        temp_in = {curr_word[0]:1}
                        transition_prob[" "] = temp_in
                    else:
                        transition_prob[" "][curr_word[0]] = transition_prob[" "].get(curr_word[0],0) + 1
                    continue

                if not curr_word[char_num-1] in transition_prob:
                    temp = {curr_word[char_num]:1}
                    transition_prob[curr_word[char_num-1]] = temp
                else:
                    temp_dict = transition_prob[curr_word[char_num-1]]
                    if curr_word[char_num] in temp_dict:
                        temp_dict[curr_word[char_num]] = temp_dict[curr_word[char_num]] + 1
                    else:
                        temp_dict[curr_word[char_num]] = 1

                    transition_prob[curr_word[char_num-1]] = temp_dict
            
            #  After end of the word adding " " as the transition prob for last letter of the word (trans_prob(last leter of the word --> " "))
            if not curr_word[-1] in transition_prob:
                    temp = {" ":1}
                    transition_prob[curr_word[-1]] = temp
            else:
                temp_dict = transition_prob[curr_word[-1]]
                if " " in temp_dict:
                    temp_dict[" "] = temp_dict[" "] + 1
                else:
                    temp_dict[" "] = 1
                transition_prob[curr_word[-1]] = temp_dict

    # print(transition_prob)
    # print(transition_prob['U']['P'])

    for key, value in transition_prob.items():
        total = 0
        for value_key in value:
            total = total + value[value_key]
        for value_key in value:
            value[value_key] = value[value_key]/total 

    f.close()
    # print(transition_prob)
    return transition_prob


def cal_emission_prob(train_letters, test_string):
    emission_prob = {}

    test_img_total_black_pixels = 0
    test_img_total_white_pixels = 0

    # Counting total white and black pixels in the test image
    for char in test_string:
        for row in range(len(char)):
            for col in range(len(char[0])):
                if char[row][col]=='*':
                    test_img_total_black_pixels += 1
                else:
                    test_img_total_white_pixels += 1

    # print("test_img_total_black_pixels: ", test_img_total_black_pixels)
    # print("test_img_total_white_pixels: ", test_img_total_white_pixels)

    for char_num in range(len(test_string)):
        emission_prob[char_num] = {}
        curr_test_letter = test_string[char_num]

        for train_letter in train_letters:
            black_match = 0
            white_match = 0
            black_non_match = 0
            white_non_match = 0
            curr_train_letter = train_letters[train_letter]
            for row_test, row_train in zip(range(len(curr_test_letter)),range(len(curr_train_letter))):
                for col_test, col_train in zip(range(len(curr_test_letter[0])),range(len(curr_train_letter[0]))):
                    if(curr_test_letter[row_test][col_test]==curr_train_letter[row_train][col_train]) and curr_test_letter[row_test][col_test]=='*':
                        black_match += 1
                    elif(curr_test_letter[row_test][col_test]==curr_train_letter[row_train][col_train]) and curr_test_letter[row_test][col_test]==' ':
                        white_match += 1
                    elif(curr_test_letter[row_test][col_test]!=curr_train_letter[row_train][col_train]) and curr_test_letter[row_test][col_test]=='*':
                        black_non_match += 1
                    elif(curr_test_letter[row_test][col_test]!=curr_train_letter[row_train][col_train]) and curr_test_letter[row_test][col_test]==' ':
                        white_non_match += 1
            
            # Assigning diifferent weights to emission_prob based on the pixel density in the test image        
            # For calculating weights to improve accuracy i had a brief discussion with Aishwarys Bhudhkar about the weights we neeed to allocate for the different variables
            if test_img_total_black_pixels > 0.2*test_img_total_white_pixels: # This improved accuracy to great extent because initially i was very bad results for densely populated pixels
                emission_prob[char_num][train_letter] = pow(0.8, black_match)*pow(0.7, white_match)*pow(0.2, black_non_match)*pow(0.3,white_non_match)
            else:
                emission_prob[char_num][train_letter] = pow(0.9, black_match)*pow(0.6, white_match)*pow(0.1, black_non_match)*pow(0.4,white_non_match)
            
    return emission_prob


def simple_bayes_net(emission_prob):
    image_text = ""

    for char, value in emission_prob.items():
        temp = None
        for value_keys in value:
            if temp == None:
                temp = value_keys
                continue
            if value[value_keys] >= value[temp]:
                temp = value_keys
        image_text += temp

    return image_text


# Below viterbi code written after referring code for Prof David's in class Viterbi activity 
def hmm_viterbi(train_letters,test_letters,em_prob,trans_prob,init_prob):
    N = len(test_letters)

    # V_table = {"R": [0] * N, "S" : [0] * N}
    # which_table = {"R": [0] * N, "S" : [0] * N}

    V_table = {}
    which_table={}
    for key in train_letters:
        V_table[key] = [0]*N
    for key in train_letters:
        which_table[key] = [0]*N

    for s in train_letters:
        if s not in init_prob:
            V_table[s][0] = 0
        else:
            V_table[s][0] = log(init_prob[s])
    
    for i in range(1, N):
        for s in train_letters:
            # V_table[s][0] = init_prob[s]

            (which_table[s][i], V_table[s][i]) =  max( [ (s0, V_table[s0][i-1] + 2*log((trans_prob.get(s0,{})).get(s,pow(10,-10)))) for s0 in train_letters ], key=lambda l:l[1] ) 
            V_table[s][i] = V_table[s][i] + 3*log(em_prob[i][s])

    viterbi_seq = [""] * N
    # viterbi_seq[N-1] = "R" if V_table["R"][i] > V_table["S"][i] else "S"

    temp = None
    max_key = None
    for key, value in V_table.items():
        if temp == None:
            temp = value[i]
            max_key = key
        if value[i]>temp:
            temp = value[i]
            max_key = key

    viterbi_seq[N-1] = max_key
    for i in range(N-2, -1, -1):
        viterbi_seq[i] = which_table[viterbi_seq[i+1]][i+1]

    return "".join(w for w in viterbi_seq)


#####
# main program
start_time = time.time()

if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

# initial_emission_prob , transition_prob = calculate_probilities(train_txt_fname)
# print(transition_prob)

initial_probability =  cal_initial_prob(train_txt_fname)
transition_probability = cal_transition_prob(train_txt_fname)
emission_probability = cal_emission_prob(train_letters, test_letters)

ans_simple_bayes = simple_bayes_net(emission_probability)
ans_viterbi_map = hmm_viterbi(train_letters,test_letters,emission_probability,transition_probability,initial_probability)

print("Total Time elapsed: ",time.time()-start_time)


# The final two lines of your output should look something like this:
print("Simple: " + ans_simple_bayes)
print("   HMM: " + ans_viterbi_map) 
