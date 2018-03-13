from classify import Classify
import warnings

def main():
    clf = Classify()
    while(True):
        word = input('Word: ')
        classification = clf.classifyWord(word)
        if(classification[0]>classification[1]):
            print("Telugu, with prob matrix")
        else:
            print("English, with prob matrix")
        print(classification)

# def main():
#     clf = Classify()
#     enchanted = enchant.Dict('en-US')
#     words = []
#     with open('outfile4.json') as f:
#         filecontent = f.readlines()
#         for line in filecontent:
#             pwords = json.loads(line)["content"].split()
#             for word in pwords:
#                 if(".com" in word or any(char.isdigit() for char in word)):
#                     continue
#                 words.append(word.translate(str.maketrans('', '', string.punctuation)).lower())

#     nwords = random.sample(words,100000)

#     enchanged = enchant.Dict('en-US')

#     correct = 0
#     total = 0

#     incorrect = dict()
#     nwords = list(filter(lambda x: x != '', nwords))

#     for (i,probs) in enumerate(map(clf.classifyWord, nwords)):
#         word = nwords[i]
#         total+=1
#         lang = "english" if probs[1] > probs[0] else "telugu"
#         is_eng = enchanted.check(word)
#         correctness = "CORRECT" if ((is_eng and lang == "english" or not is_eng and lang=="telugu")) else "INCORRECT"
#         print(correctness + ": " + nwords[i] + " is " + lang + " with probabilities " + str(probs))
#         if correctness=="CORRECT":
#             correct+=1
#         else:
#             if word not in incorrect:
#                 incorrect[word] = 1
#             else:
#                 incorrect[word] += 1

#     print("correct: " + str(correct/total))
#     print(incorrect)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    main()