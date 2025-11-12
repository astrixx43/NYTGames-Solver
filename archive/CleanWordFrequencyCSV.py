
wordFrequencyCSV = open('unigram_freq.csv', 'r', newline='')

fiveLetterWordFrequencyFile = open('fiveLetterWordFrequency.csv', 'w')

wordList = []

totalCount = 0

wordFrequencyCSV.readline()

for line in wordFrequencyCSV:
    line = line.split(',')
    if len(line[0]) == 5:
        wordList.append([line[0], float(line[1])])
        totalCount += int(line[1])

wordFrequencyCSV.close()

for wordFreq in wordList:
    wordFreq[1] /= totalCount

    fiveLetterWordFrequencyFile.writelines(wordFreq[0] + "," +
                                           str(wordFreq[1]) + "\n")

fiveLetterWordFrequencyFile.close()
