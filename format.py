import json
import string
# from sklearn import svm
# from sklearn.dummy import DummyClassifier
import nltk
from nltk import ngrams
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import enchant
import csv
import random
from sklearn.externals import joblib

class MyData:
    def loadFreqData(self):
        print("loading data")
        wordfreqdict = dict()
        with open("./wordfreq.txt") as wf:
            wordfreqinit = wf.readlines()

        for wordacc in wordfreqinit:
            wordaccarr = wordacc.split()
            self.wordfreqdict[wordaccarr[0]] = wordaccarr[1]

    def readData(self):
        for line in self.filecontent:
            self.data.append(json.loads(line))

    def train(self):
        print("training")
        X = self.justgrams
        Y = self.justtags
        print(self.justgrams[0])
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
        print(len(X_train))
        print(len(y_train))
        # clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
        clf = RandomForestClassifier()
        clf2 = RandomForestClassifier()

        fitted = clf.fit(X_train, y_train)
        fitted2 = clf2.fit(X,Y)

        print("split score: " + str(clf.score(X_test, y_test)))
        # clf = DummyClassifier(strategy='most_frequent',random_state=0).fit(X_train,y_train)
        scores = cross_val_score(clf, X, Y, cv = 5)
        scores2 = cross_val_score(clf2, X, Y, cv = 5)

        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

        print("Accuracy2: %0.2f (+/- %0.2f)" % (scores2.mean(), scores2.std() * 2))

        joblib.dump(clf2, 'initmodel4.pkl') 


    def isEnglish(self, word):
        return word in self.wordfreqdict and self.enchanted.check(word)

    def makeMLReady(self):
        print("making ml ready")
        self.taggedwords.append(["word","english"])
        englishg = 0
        totalg = 0
        for i in range(0,len(self.data)):
            text = self.data[i]["content"]
            text = text.translate(str.maketrans('', '', string.punctuation))
            textarr = text.split()
            english = 0
            total = 0
            for i in range(0,len(textarr)):
                word = textarr[i].lower()
                if(".com" in word or any(char.isdigit() for char in word)):
                    continue
                isenglish = self.isEnglish(textarr[i])
                trigrams = ngrams(list("##" + word + "##"), 3)
                trigramslist = list(trigrams)
                for j in range(0,len(trigramslist)):
                    grams = trigramslist[j]
                    self.taggedgrams.append([grams, isenglish])
                    justgrams = list(map(lambda x: ord(x), grams))
                    justgrams.append(j/len(trigramslist))
                    # print(justgrams)
                    self.justgrams.append(justgrams)
                    self.justtags.append(isenglish)
                self.taggedwords.append(["##" + word + "##", isenglish])
                if(isenglish):
                    english+=1
                    englishg+=1
                total+=1
                totalg+=1
            # print("english: " + str(english) + ", total: " + str(total))
            self.data[i]["epercentage"] = english/total if english != 0 and total != 0 else 0
        print(englishg)
        print(totalg)
        print(englishg/totalg)

    def toCSV(self):
        print("writing to CSV")
        # with open("csvoutput.csv", "w") as c:
        #     writer = csv.writer(c)
        #     writer.writerows(self.just)
        with open("csvoutputgrams.csv", "w") as c:
            writer = csv.writer(c)
            writer.writerows(self.taggedgrams)

    def __init__(self, jsonfile):
        self.data = []
        self.taggedwords = []
        self.taggedgrams = []
        self.justgrams = []
        self.justtags = []
        self.wordfreqdict = dict()
        self.enchanted = enchant.Dict('en-US')
        self.file = jsonfile
        with open(jsonfile) as f:
            self.filecontent = f.readlines()
        self.loadFreqData()
        self.readData()
        self.makeMLReady()
        self.train()
        # self.toCSV()

def main():
    jsonfile = "outfile4.json"
    x = MyData(jsonfile)

main()