import re
from sklearn.model_selection import train_test_split

def getSentences(trainingData):
    numberCheck = "(^[0-9])"
    newLine = list()
    sentenceArray = list()

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

def getPOSandWordLists(trainData):
    wordList = list()
    tagList = list()
    for sentence in trainData:
        for word, tag in sentence:
            wordList.append(word)
            tagList.append(tag)
    return wordList, tagList

def generateBigrams(wordList):
    return zip(wordList, wordList[1:])
# def tagTransitionProbabilities(testData):
#     return

InputFileName = "S21-gene-train.txt"
trainingData = open(InputFileName, 'r').readlines()
sentenceArray = getSentences(trainingData)
traindata, testData = train_test_split(sentenceArray, test_size=0.2)
wordList, tagList = getPOSandWordLists(traindata)
bigrams = generateBigrams(wordList)
print(bigrams)
# print("sentence: ", sentenceArray)
