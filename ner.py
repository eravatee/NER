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
    states = list()
    words = list()
    stateCounts = dict()
    wordCounts = dict()
    for sentence in trainData:
        
        for word, tag in sentence:
            wordList.append(word)
            tagList.append(tag)
            states.append(tag)
            words.append(word)
            if tag not in stateCounts:
                stateCounts[tag] = 0
            else: 
                stateCounts[tag] += 1
            if word not in wordCounts:    
                wordCounts[word] = 0
            else:
                wordCounts[word] += 1
           
    print("stateCounts: ", stateCounts)
    return wordList, tagList, stateCounts, wordCounts, states, words

def tagTransitionProbabilities(tagList, stateCounts):
    
    bigrams = zip(tagList, tagList[1:])
    tagTransnProbs = dict()

    for i in stateCounts.keys():
        tagTransnProbs[i] = dict()
        for j in stateCounts.keys():
            tagTransnProbs[i][j] = 0
    
    for bigram in bigrams:
        if bigram[0] in tagTransnProbs:
            if bigram[1] in tagTransnProbs[bigram[0]]:
                tagTransnProbs[bigram[0]][bigram[1]] += 1
    
    for i in tagTransnProbs:
        for j in tagTransnProbs[i]:
            tagTransnProbs[i][j] = round(tagTransnProbs[i][j] / stateCounts[i], 2)

    return tagTransnProbs

def tagEmissionProbabilities(wordCounts, stateCounts, words, states):
    tagEmissionProbs = dict()

    for i in stateCounts.keys():
        tagEmissionProbs[i] = dict()
        for j in wordCounts.keys():
            tagEmissionProbs[i][j] = 0

    wordTagCombos = zip(words, states)

    for wordTagCombo in wordTagCombos:
        word = wordTagCombo[0]
        tag = wordTagCombo[1]
        if tag in tagEmissionProbs:
            if word in tagEmissionProbs[tag]:
                tagEmissionProbs[tag][word] += 1
    
    for tag in tagEmissionProbs:
        for word in tagEmissionProbs[tag]:
            tagEmissionProbs[tag][word] = round(tagEmissionProbs[tag][word] / wordCounts[word], 2)

    print("tagEmissionProbs: ", tagEmissionProbs)
    return tagEmissionProbs

def handleUnkowns(wordList, tagList, stateCounts, wordCounts, states, words):
    
    return wordList, tagList, stateCounts, wordCounts, states, words

InputFileName = "S21-gene-train.txt"

trainingData = open(InputFileName, 'r').readlines()

sentenceArray = getSentences(trainingData)
traindata, testData = train_test_split(sentenceArray, test_size=0.2)
wordList, tagList, stateCounts, wordCounts, states, words = getPOSandWordLists(traindata)

wordList, tagList, stateCounts, wordCounts, states, words = handleUnkowns(wordList, tagList, stateCounts, wordCounts, states, words)

tagTransnProbs = tagTransitionProbabilities(tagList, stateCounts)
tagEmissionProbs = tagEmissionProbabilities(wordCounts, stateCounts, words, states)