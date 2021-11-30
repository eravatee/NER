import re

def structureTrainingData(trainingData):
    numberRegex = "(^[0-9])"
    sentence = list()
    structuredTrainingData = list()

    for line in trainingData:
        line.strip()
        if re.search(numberRegex, line):
            chunks = line.split("\n")[0].split("\t")
            sentence.append([chunk for chunk in chunks[1:]])
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
    
    for tag1 in tagCounts:
        for tag2 in tagCounts:
            tagTransitionProbabilities[tag1][tag2] = ((tagTransitionProbabilities[tag1][tag2] if tag2 in tagTransitionProbabilities[tag1] else 0) + 1) / (tagCounts[tag1] + len(tagCounts))

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
            emissionProbabilities[tag][word] = emissionProbabilities[tag][word] / tagCounts[tag]

    return emissionProbabilities

def getStartingProbabilities(structuredTrainingData):
    startingProbabilities = dict()
    
    for sentence in structuredTrainingData:
        if sentence[0] and sentence[0][1]:
            if sentence[0][1] not in startingProbabilities:
                startingProbabilities[sentence[0][1]] = 0
            startingProbabilities[sentence[0][1]] += 1
    
    for tag in tagCounts:
        startingProbabilities[tag] = (startingProbabilities[tag] if tag in startingProbabilities else 0) / len(structuredTrainingData)
                
    return startingProbabilities

def viterbi(structuredTestingData, tagCounts, startingProbabilities, tagTransitionProbabilities, wordCounts, emissionProbabilities):
    for sentence in structuredTestingData:
        viterbiProbabilities = dict()
        backTrack = dict()
        for tag in tagCounts.keys():
            viterbiProbabilities[tag] = list()
            viterbiProbabilities[tag].append(startingProbabilities[tag] * emissionProbabilities[tag][sentence[0] if sentence[0] in list(wordCounts.keys()) else '<UNK>'])
            backTrack[tag] = [0]
        
        for index, word in enumerate(sentence[1:]):
            for tag in tagCounts.keys():     
                maxProbability = max([(viterbiProbabilities[previousTag][index - 1]
                                                        * tagTransitionProbabilities[previousTag][tag]
                                                        * (emissionProbabilities[tag][word] if word in list(emissionProbabilities[tag]) else emissionProbabilities[tag]['<UNK>']), previousTag)
                                                        for previousTag in tagCounts])
                viterbiProbabilities[tag].append(maxProbability[0])
                backTrack[tag].append(maxProbability[1])
    
        ans = max([(viterbiProbabilities[tag][-1], tag) for tag in list(tagCounts.keys())])
        start = ans[1]
        
        print(viterbiProbabilities)

        # for i in range(len(sentence)):
        #     start = backTrack[start][-1 - i]
        #     if start != 'O' and start != 0:
        #         print(sentence[-1 -i], start)
                
trainingFileName = "S21-gene-train.txt"
rawTrainingData = open(trainingFileName, 'r').readlines()

structuredTrainingData = structureTrainingData(rawTrainingData)
words, tags, tagCounts, wordCounts = analyzeTrainingData(structuredTrainingData)

words, tags, tagCounts, wordCounts = handleUnkowns(words, tags, tagCounts, wordCounts)

tagTransitionProbabilities = getTagTransitionProbabilities(tags, tagCounts)
emissionProbabilities = getEmissionProbabilities(words, tags, tagCounts)
startingProbabilities = getStartingProbabilities(structuredTrainingData)

testFileNAme = "F21-gene-test.txt"
rawTestingData = open(testFileNAme, 'r').readlines()
structuredTestingData = structureTrainingData(rawTestingData)

viterbi(structuredTestingData[:1], tagCounts, startingProbabilities, tagTransitionProbabilities, wordCounts, emissionProbabilities)
