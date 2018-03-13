from sklearn.externals import joblib
from nltk import ngrams
import json
import string
import enchant
import random

class Classify:
    def __init__(self):
        self.filename = 'initmodel.pkl'
        self.model = joblib.load(self.filename)

    def getTrigrams(self, word):
        trigrams = ngrams(list("##" + word + "##"), 3)
        trigramslist = list(trigrams)
        finalized = []
        for j in range(0,len(trigramslist)):
            grams = trigramslist[j]
            justgrams = list(map(lambda x: ord(x), grams))
            justgrams.append(j/len(trigramslist))
            finalized.append(justgrams)
        # print(finalized)
        return finalized

    def assignProbs(self, trigramslist):
        return list(map(lambda x: self.model.predict_proba([x]), trigramslist))


    def splitProbs(self, word):
        trigrams = self.getTrigrams(word)
        trigramprobs = self.assignProbs(trigrams)
        # print(trigramprobs)
        return trigramprobs

    def wordProb(self,trigramprobs, word):
        # print("calculating word probabilites for " + word)
        engprob = 1
        telprob = 1
        grams = list(ngrams("##" + word + "##", 3))
        for i in range(0,len(trigramprobs)):
            prob = trigramprobs[i]
            # print(grams[i])
            # print("engprob: " + str(engprob))
            # print("telprob: " + str(telprob))
            # print(prob)
            engprob *= prob[0][1]
            telprob *= prob[0][0]
            tsum = engprob + telprob
            engprob = engprob/tsum
            telprob = telprob/tsum
        return [telprob/(engprob+telprob), engprob/(engprob+telprob)]

    def classifyWord(self,word):
        # res = []
        # print("on word " + word)
        trigramprobs = self.splitProbs(word)
        return self.wordProb(trigramprobs, word)
        # res.append(self.wordProb(trigramprobs, word))
        # return res


    