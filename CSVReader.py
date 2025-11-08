import sys
import os
import csv
import ResultsPageOutPutData


def loadResultsDirectly():
    # Get the result from the Python file and convert it to work with current CSV Reader format
    if hasattr(ResultsPageOutPutData, 'result'):
        rawResult = ResultsPageOutPutData.result
        
        # Convert to CSV Reader format (handles index 12 skip)
        convertedResults = {}
        for snakeId, score in rawResult.items():
            snakeId = int( snakeId )
            if snakeId < 12:
                csvKey = snakeId
            else:
                csvKey = snakeId + 1  # Skip index 12
            convertedResults[ csvKey ] = float( score )
        
        return convertedResults
    else:
        return None

def main():
    # Load external results
    externalResults = loadResultsDirectly()
    
    count = 0
    everyLine = []
    scores = {}

    with open('Questions.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:  # makes a giant list of lists where each line in its own list
            tempList = []
            for i in range(0, 24):  # this number has to be exact or index out of range 
                tempList.append(lines[i])
            if(lines[0] != "Snake"):  # makes a dict that will keep track of snake and thier current score
                scores[lines[0]] = 0
            everyLine.append(tempList)

    # Process external results through the questionnaire logic
        # Use external results - process them through the questionnaire logic
    checker = True
    tracker = []
    externalKeys = list(externalResults.keys())
    keyIndex = 0
        
    for externalKey in externalKeys:
        userData = str(externalKey)
            
        # Skip if already processed or invalid
        if userData in tracker:
            continue
        if userData.isdigit() and (int(userData) > 23 or int(userData) < 1):
            continue
        elif userData.isdigit():
            tracker.append(userData)
            keys = list(scores.keys())
            for i in range(1, len(scores) + 1):
                key = keys[i-1]
                currentVal = scores[key]
                scores[key] = float(currentVal) + float(everyLine[i][int(userData)])
        
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