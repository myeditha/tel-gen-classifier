import json
import string
from sklearn import svm
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from scipy.sparse import lil_matrix
from classify import Classify
from sklearn.metrics import confusion_matrix
import numpy as np

def get_dims(mystr, worddict):
    # arr = mystr.split(" ")
    # numwords = worddict["counter"]
    # for word in arr:
    #     if(".com" in word or any(char.isdigit() for char in word)):
    #         continue
    #     word = word.translate(str.maketrans('', '', string.punctuation)).lower()
    #     if word not in worddict:
    #         worddict[word] = numwords
    #         numwords += 1
    #         worddict["counter"] = numwords
    return

def has_word(arr, fn):
    tel = 0
    for word in arr:
        res = fn(word)
        if(res[0] > res[1]):
            tel += 1
    # if (tel <= (len(arr)//10)):
    if(tel <= 0):
        return 0
    # if (tel >= (len(arr)-(len(arr)//10))):
    elif(tel == len(arr)):
        return 1
    else:
        return 2

# def flush(input):

def preprocess(arr):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    arr = " ".join(arr).lower().translate(translator).split(" ")
    # arr = list(filter(lambda x: flush(x), arr))
    return list(filter(lambda x: x != "" and not (".com" in x or any(char.isdigit() for char in x)), arr))
        

def create_bag(mystr, doc, worddict, features, fn):
    arr = mystr.split(" ")
    arr = preprocess(arr)
    for word in arr:
        if(word in worddict):
            num = worddict[word]
            features[doc, num] += 1
    eng = has_word(arr, fn)
    # print(str(arr) + ", " + str(eng))
    features[doc, 3] = 1 if (features[doc, 1] > 0 and features[doc,2] > 0) else 0
    features[doc, 1] = features[doc, 2] - features[doc, 1]
    features[doc, 2] = 0
    features[doc, 0] = eng
    

def load_tagged(file):
    with open(file) as f:
        taggedjsons = f.readlines()
        loaded = list(map(lambda x: json.loads(x), taggedjsons))
        worddict = dict()
        worddict["counter"] = 0 
        rows = 0
        for num, row in enumerate(loaded):
            get_dims(row["content"], worddict)
            rows = num

        # Raw features
        worddict = { "counter": 2, "lo": 1, "ni": 1, "ante": 1, "ee": 1, "ga": 1, "ani": 1, "e": 1, "aa": 1, "aaa": 1, "nenu": 1, "ee": 1, "in": 2, "to": 2, "it": 2, "i": 2, "or": 2, "a": 2, "for": 2, "be": 2, "he": 2, "she": 2 }
        cols = worddict["counter"]
        content = lil_matrix((rows+1, cols+2))

        classify = Classify()

        for doc, x in enumerate(loaded):
            create_bag(x["content"], doc, worddict, content, classify.classifyWord)
        

        strs = list(map(lambda x: " ".join(preprocess(x["content"].split(" "))), loaded))

        # print(content)
        tags = list(map(lambda x: x["ptype"], loaded))
        
        content = content.toarray()

        print(repr(content))
        print(content)
    return content, tags, strs

def main():
    content_train, tags_train, str_train = load_tagged('taggedcmtypes3.json')
    content_test, tags_test, str_test = load_tagged('taggedcmtypes.json')
    trials = 1
    score = 0
    # change this
    clf = svm.SVC(kernel = "rbf")
    clf.fit(content_train, tags_train)
    print(confusion_matrix(tags_test, clf.predict(content_test)))
    score += clf.score(content_test, tags_test)
    print(score/trials)
    debug_arr = list(zip(content_test, tags_test))
    for i in range(0,len(debug_arr)):
        item, label = debug_arr[i]
        result = clf.predict([item])
        if (result != label):
            print("predicted label for '%s' is %s, but true label is %s: classes: %s" % (str_test[i],result, label, item))

main()
