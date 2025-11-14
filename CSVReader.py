import sys
import os
import csv

def testQuestionaire( qnaResults ):

    
    count = 0
    everyLine = []
    scores = {}

    with open('Questions.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:  # makes a giant list of lists where each line in its own list
            tempList = []
            if(lines[0] != "Snake"):  # makes a dict that will keep track of snake and thier current score
                scores[lines[0]] = 0
                for i in range(0, 24):  # this number has to be exact or index out of range 
                    tempList.append(lines[i])
            if len(tempList) > 0:
                everyLine.append(tempList)

    print(everyLine)
    checker = True
    keyIndex = 0
        
    for i in range(len(qnaResults)):
        keys = list(scores.keys())
        for j in range(1, len(scores) + 1):
            key = keys[j-1]
            currentVal = scores[key]
            scores[key] = float(currentVal) + float(everyLine[i][int(qnaResults[i])])
        
    checker = False  # End the while loop

        # now to organize by most points to least points
        # skips index 12 
    rating = {}
    indexes = []

    values = list(scores.values())
    value = list(scores.values())  # making a second list to get index value to for return 
    keys = list(scores.keys())
        
    for i in range(len(values)):
        maxValue = max(values)  # gets the max value from pr
        indexMax = values.index(maxValue)  # gets the index of that max
        
        for i in range(len(value)):  # get a list of the indexes of top scores in order
            if(maxValue == value[i]):
                if(i < 11):  # to compensate for the messup on the database skipping 12
                    rating[i + 1] = float(maxValue)  # plus 1 so its 1-11
                else:
                    rating[i + 2] = float(maxValue)  # plus 2 so its 13-18

        # remove to avoid repeats
        del values[indexMax]
        del keys[indexMax]

    # Return the rating dictionary
    return rating