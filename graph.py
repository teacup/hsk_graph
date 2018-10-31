import sys

from .utils.HSKUtils import isHanzi, hSKLevel

# Summary:
# 	For each tuple, get last value. Call hSKLevel on value and build new array. Sort array and return count of each value

# dataBasePath = 'data/collection-copy.anki2'
# datesAndHanzi = getData(dataBasePath)
# datesIndex = list(key[0][0].date() for key in datesAndHanzi)

# If updating graphProfiles.CharacterFrequency.graphColumnNames, need to update characterFrequencyRange
graphProfiles = {
    'HSK': {'graphColumnNames': ['HSK 1', 'HSK 2', 'HSK 3', 'HSK 4', 'HSK 5', 'HSK 6', 'Non-HSK'],
            'countingFunctions': hSKLevel,
            'range': (1, 8)}  # ,
    # 'CharacterFrequency': { 'graphColumnNames': [300, 600, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 10000],
    # 						'countingFunctions': characterFrequencyLevel,
    # 						'range': (0, 11) }
}

graphColumnColours = ['#A00041', '#D73C4C', '#F66D3A', '#FFAF59', '#FFE185', '#FFFFBC', '#ECEBCA']
graphBackgroundColour = '#D9D9D9'


def processHanzi(hanziList, countingFunc, graphType):
    # param: 1. list of tuples holding date learnt and hanzi 2. function to call to count data
    # 		eg. [[(datetime.datetime(2016, 9, 28, 11, 26, 42), u'\u4ed6\u79bb\u4f60\u5f88\u8fd1')]]
    # returns: list of lists
    learnedHanzi = {}
    processedDatesAndHanzi = []

    def processSentence(day, sentence):
        charactersInSentence = list(sentence)
        for character in charactersInSentence:
            if character not in learnedHanzi and isHanzi(character):
                learnedHanzi[character] = True
                processedDatesAndHanzi.append((day, countingFunc(character)))
        return

    for index, hanziByDay in enumerate(hanziList):
        day, hanzi = hanziByDay[0], hanziByDay[1]
        if len(hanzi) > 4 or graphType == 'CharacterFrequency':  # break sentences down into individual characters!
            processSentence(day, hanzi)

        elif hanzi not in learnedHanzi:
            learnedHanzi[hanzi] = True
            processedDatesAndHanzi.append((day, countingFunc(hanzi)))
    # sys.stderr.write(str(processedDatesAndHanzi))
    return processedDatesAndHanzi


def countFreqOccurances(hanziList, graphType):
    # summary: For each day, count the number of hanzi learnt in each frequency level
    # returns: list of lists

    hanziOccuranceList = []
    columnNames = graphProfiles[graphType]['graphColumnNames']
    columnRange = graphProfiles[graphType]['range']
    counting = (graphType == 'CharacterFrequency')

    for firstIndex, listOfHanziLevels in enumerate(hanziList):
        hanziOccuranceList.append([])
        for secondIndex in range(columnRange[0], columnRange[1]):
            if counting == True:
                hanziOccuranceList[firstIndex].append(listOfHanziLevels.count(columnNames[secondIndex]))
            else:
                hanziOccuranceList[firstIndex].append(listOfHanziLevels.count(secondIndex))
    return hanziOccuranceList


def processGraphData(graph, graphType):
    processedHanziList = processHanzi(datesAndHanzi, graph, graphType)
    return countFreqOccurances(processedHanziList, graphType)
