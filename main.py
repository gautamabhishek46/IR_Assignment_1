from os import listdir, walk
import pickle
from math import sqrt

DATA_DIR = 'data'
STOPWORDS_FILE_NAME = 'stopwords_en.txt'
DOCUMENTS_DIR = 'documents/written_1/letters/icic'
# /mnt/CC0091D90091CB3A/Study/7 sem/IR/Assignments/Assignment_1/IR_Assignment_1/data/documents/written_1/journal/slate
DOCUMENTS_INDEX = 'documentIndex.txt'
DOC_INCIDENCE_TABLE_FILE_NAME = 'docIncidenceTable.txt'

def cleanContent(content):
    return content

def removeStopWords(words):
    return words

def writeObjectToFile(object, file):
    with open(file, 'wb') as output:
        pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)

def loadObjectFromFile(file):
    with open(file, 'rb') as input:
        return pickle.load(input)

def indexDocuments():
    print("Updating doc index started")

    documents = dict()

    for root, dirs, files in walk(DATA_DIR + '/' + DOCUMENTS_DIR):
        docID = 0
        for file in files:
            documents[docID] = root + '/' + file
            docID = docID + 1

    writeObjectToFile(documents, DATA_DIR + '/' + DOCUMENTS_INDEX)

    docIncidenceTable = {}          # key = word; value = list of DOCUMENTS

    documentKeys = list(documents.keys())
    documentKeys.sort()

    wordSet = set()

    for key in documentKeys:
        docID = key
        path = documents[key]

        f = open(path, "r")
        content = f.read()
        content = cleanContent(content)
        words = (content.split())
        words = removeStopWords(words)

        for word in words:
            wordSet.add(word)

            if docID in docIncidenceTable:
                docIncidenceTable[docID][word] = docIncidenceTable[docID].get(word, 0) + 1
            else:
                docIncidenceTable[docID] = dict()
                docIncidenceTable[docID][word] = 1

    writeObjectToFile(docIncidenceTable, DATA_DIR + '/' + DOC_INCIDENCE_TABLE_FILE_NAME)

    print("Done updating doc index")

def loadDocIncidenceTable():
    return loadObjectFromFile(DATA_DIR + '/' + DOC_INCIDENCE_TABLE_FILE_NAME)

def rankDocsForQuery(query, docIncidenceTable):
    query = query.split()
    queryFreqDict = {}

    rank = dict()
    queryMod = 0

    for word in query:
        queryFreqDict[word] = queryFreqDict.get(word, 0) + 1

    for word, count in queryFreqDict.items():
        queryMod = queryMod + (count * count)

    queryMod = sqrt(queryMod)

    i = 0

    for docID, words in docIncidenceTable.items():
        cosNeum = 0
        docMod = 0

        for word, count in queryFreqDict.items():
            if word in words:
                cosNeum = cosNeum + (count * words[word])
                docMod = docMod + (words[word] * words[word])

        if docMod != 0:
            cosine = cosNeum / (queryMod * sqrt(docMod))
            if cosine in rank:
                rank[cosine].append(docID)
            else:
                newList = []
                newList.append(docID)
                rank[cosine] = newList.copy()

    return rank

def printDocsRank(rank, docIndex):
    ranks = list(rank.keys())
    ranks.sort(reverse=True)

    print("\n\n\n")

    for r in ranks:
        for docID in rank[r]:
            print(str(docID) + ' :  ' + str(r) + ' : ' + docIndex[docID])

def loadDocTables():
    docIncidenceTable = loadDocIncidenceTable()
    docIndex = loadObjectFromFile(DATA_DIR + '/' + DOCUMENTS_INDEX)

    return docIncidenceTable, docIndex

def main():
    docIncidenceTable, docIndex = loadDocTables()
    choice = 1

    while(choice != 0):
        print("Chose one of the following: ")
        print("     1. Update docIndex")
        print("     2. Give a query")
        print("     3. Use default query")
        print("     0. Exit")

        choice = int(input())

        if choice == 1:
            indexDocuments()
            docIncidenceTable, docIndex = loadDocTables()
        elif choice == 2:
            query = input("Please enter your query : ")
            printDocsRank(rankDocsForQuery(query, docIncidenceTable), docIndex)
        elif choice == 3:
            printDocsRank(rankDocsForQuery("statehouse veteran overturn President Abraham", docIncidenceTable), docIndex)

        print("\n\n\n")

    print("\n\n\n")
    print("Thank you very much")
if __name__ == '__main__':
    main()
