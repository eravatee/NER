import re
from sklearn.model_selection import train_test_split

def getSentences(trainingData):
    numberCheck = "(^[0-9])"
    newLine = []
    sentenceArray=[]
    for line in trainingData:
        check = re.search(numberCheck, line)
        line.strip()
        line = line.split("\n")[0]
        chunks = line.split("\t")
        if check:
            newLine.append((chunks[1], chunks[2]))
        else:
            sentenceArray.append(newLine)
            newLine = []
    return sentenceArray

InputFileName = "S21-gene-train.txt"
trainingData = open(InputFileName, 'r').readlines()
sentenceArray = getSentences(trainingData)
train, test= train_test_split(sentenceArray, test_size=0.2)
print("sentence: ", sentenceArray)

