from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import csv
from ast import literal_eval

def main():
    print("reading")
    csvoutput = []
    with open('csvoutputgrams.csv', 'r') as f:
        reader = csv.reader(f)
        csvoutput = list(reader)

    print("finished reading")
    print(csvoutput[0])

    print("training")

    print(literal_eval(csvoutput[0][0]))

    justgrams = list(map(lambda x: list(map(lambda y: ord(y), literal_eval(x[0]))), csvoutput))
    justtags = list(map(lambda x: bool(x[1]), csvoutput))

    print(justgrams[0])
    print(justtags[1])

    X = justgrams[0:10000]
    Y = justtags[0:10000]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    print(len(X_train))
    print(len(y_train))
    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    fitted = clf.fit(X_train, y_train)
    print("split score: " + str(clf.score(X_test, y_test)))
    # clf = DummyClassifier(strategy='most_frequent',random_state=0).fit(X_train,y_train)
    scores = cross_val_score(clf, X, Y, cv = 5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

main()