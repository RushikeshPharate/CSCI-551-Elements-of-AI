# SeekTruth.py : Classify text objects into two categories
#
# SARVESH RAGADE SRAGADE 
# PARITOSH SABADE PSABADE
# RUSHIKESH PHARATE RPHARATE
# Based on skeleton code by D. Crandall, October 2021
#
import math
import sys
import re

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!



#I SARVESH RAGADE has also taken Course CSCI-B 555 Machine Learning in this semester, 
# We had a similar assingment on Naive Bayes as our first programming assingment. That was a individual assingment.
#the code i used here, I have used some concepts i learn in Machine Learning course.

def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!


    listf=[]
    listff=[]
    listt=[]
    list1=[]
    list2=[]
    for line in train_data["objects"]:
        list1.append(line)                     #Creating a list that contains all sentences
    for label in train_data["labels"]:
        list2.append(label)                    #Creating a list that contains all labels of corresponding sentences

    for i in range(len(list2)):
        if list2[i]==train_data["classes"][1]:        
            listf.append(list1[i])              #Making a list that has sentences with deceptive labels
        else :
            listt.append(list1[i])              #Making a list that has sentences with truthful labels

    decwords=[]


    for line in listf:
        chars = " ".join(re.findall("[a-zA-Z]+", line)).lower()      #Removing Punctuation,Converting to lower case
        words = chars.split()
        for word in words:
          if word not in decwords:
            decwords.append(word)                 #creating a list with Deceptive words

    truwords=[]
    for line in listt:
        chars = " ".join(re.findall("[a-zA-Z]+", line)).lower()        #Removing Punctuation,Converting to lower case
        words = chars.split()
        for word in words:
          if word not in truwords:
            truwords.append(word)                 #creating a list with truthful words

    vocabcount = truwords + decwords        #Total number of words
    vocabcount1 = set(vocabcount)           # Total number of words after Removing Duplicates words
    posarr = {}
    for line in listt:
        chars = " ".join(re.findall("[a-zA-Z]+", line)).lower()
        words = chars.split()
        for word in words:
           if word in posarr:                #Here we are calculating how many times words are repeated in truthful list
            posarr[word] += 1                  
           else:
            posarr[word] = 1

    negarr = {}
    for line in listf:
        chars = " ".join(re.findall("[a-zA-Z]+", line)).lower()
        words = chars.split()
        for word in words:
          if word in negarr:                 #Here we are calculating how many times words are repeated in truthful list
            negarr[word] += 1
          else:
            negarr[word] = 1

    MLpos = (len(listt) / len(list1))  # ML FOR POSITIVE
    MLneg = (len(listf) / len(list1))  # ML FOR NEGATIVE
    MAPpos = dict()
    MAPneg = dict()
    sf=1
    for word in vocabcount1:  # CALCULATING MAP or Probability FOR EACH WORD
        MAPpos[word] = math.log((posarr.get(word, 0) + sf) / (len(truwords) + (sf *len(vocabcount1))))
        MAPneg[word] = math.log((negarr.get(word, 0) + sf) / (len(decwords) + (sf * len(vocabcount1))))

    rcounts = 0
    tpcounts = 0
    doc = []
    for doc in test_data["objects"]:      #Taking Test Data
        twordsl = set()
        prn = MLneg
        prp = MLpos
        test_document = doc.split("\t")            #Taking Each Sentence
        chars = " ".join(re.findall("[a-zA-Z]+", test_document[0])).lower()

        for word in chars.split(" "):              #taking Each words
           twordsl.add(word)                       #Creating list of Each word

        for word in twordsl:  # CALCULATING NEGATIVE AND POSITIVE POSTERIOR OF SENTENCE
           prn += MAPneg.get(word, 0) if word in vocabcount1 else math.log(1)
           prp += MAPpos.get(word, 0) if word in vocabcount1 else math.log(1)
        if prn >= prp :            #Checking Total Probability 
          observed_prediction = train_data["classes"][1]
        else :
          observed_prediction = train_data["classes"][0]
        listff.append(observed_prediction)


    return listff            #Returning list with Labels


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")
    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")
    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    results= classifier(train_data, test_data_sanitized)
    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
