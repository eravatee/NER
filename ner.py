import re

def structureTrainingData(trainingData):
    numberRegex = "(^[0-9])"
    sentence = list()
    structuredTrainingData = list()

    for line in trainingData:
        line.strip()
        if re.search(numberRegex, line):
            chunks = line.split("\n")[0].split("\t")
            sentence.append((chunks[1], chunks[2]))
        else:
            structuredTrainingData.append(sentence)
            sentence = []
    return structuredTrainingData

def analyzeTrainingData(structuredTrainingData):
    words = list()
    tags = list()
    tagCounts = dict()
    wordCounts = dict()

    for sentence in structuredTrainingData:
        for word, tag in sentence:
            words.append(word)
            tags.append(tag)
            wordCounts[word] = wordCounts[word] + 1 if word in wordCounts else 1
            tagCounts[tag] = tagCounts[tag] + 1 if tag in tagCounts else 1
           
    return words, tags, tagCounts, wordCounts


def handleUnkowns(words, tags, tagCounts, wordCounts):
    singleFrequencyWordsCount = 0
    for index in range(len(words)):
        if wordCounts[words[index]] == 1:
            singleFrequencyWordsCount += 1
            del wordCounts[words[index]]
            words[index] = '<UNK>'
    
    wordCounts['<UNK>'] = singleFrequencyWordsCount
    return words, tags, tagCounts, wordCounts

def getTagTransitionProbabilities(tags, tagCounts):
    tagTransitionProbabilities = dict()
    
    for bigram in zip(tags, tags[1:]):
        if bigram[0] not in tagTransitionProbabilities:
            tagTransitionProbabilities[bigram[0]] = dict()
        if bigram[1] not in tagTransitionProbabilities[bigram[0]]:
            tagTransitionProbabilities[bigram[0]][bigram[1]] = 0
        tagTransitionProbabilities[bigram[0]][bigram[1]] += 1
    
    for tag1 in tagTransitionProbabilities:
        for tag2 in tagTransitionProbabilities[tag1]:
            tagTransitionProbabilities[tag1][tag2] = round(tagTransitionProbabilities[tag1][tag2] / tagCounts[tag1], 2)

    return tagTransitionProbabilities

def getEmissionProbabilities(words, tags, tagCounts):
    emissionProbabilities = dict()

    for word, tag in zip(words, tags):
        if tag not in emissionProbabilities:
            emissionProbabilities[tag] = dict()
        if word not in emissionProbabilities[tag]:
            emissionProbabilities[tag][word] = 0
        emissionProbabilities[tag][word] += 1
    
    for tag in emissionProbabilities:
        for word in emissionProbabilities[tag]:
            emissionProbabilities[tag][word] = round(emissionProbabilities[tag][word] / tagCounts[tag], 2)

    return emissionProbabilities

def getStartingProbabilities(structuredTrainingData):
    startingProbabilities = dict()
    
    for sentence in structuredTrainingData:
        if sentence[0] and sentence[0][1]:
            if sentence[0][1] not in startingProbabilities:
                startingProbabilities[sentence[0][1]] = 0
            startingProbabilities[sentence[0][1]] += 1
    
    for tag in startingProbabilities:
        startingProbabilities[tag] = round(startingProbabilities[tag] / len(structuredTrainingData), 2)
                
    return startingProbabilities

trainingFileName = "S21-gene-train.txt"
rawTrainingData = open(trainingFileName, 'r').readlines()

structuredTrainingData = structureTrainingData(rawTrainingData)
words, tags, tagCounts, wordCounts = analyzeTrainingData(structuredTrainingData)

words, tags, tagCounts, wordCounts = handleUnkowns(words, tags, tagCounts, wordCounts)

tagTransitionProbabilities = getTagTransitionProbabilities(tags, tagCounts)
emissionProbabilities = getEmissionProbabilities(words, tags, tagCounts)
startingProbabilities = getStartingProbabilities(structuredTrainingData)
