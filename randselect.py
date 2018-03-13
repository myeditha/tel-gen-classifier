import random
import json

def main():
    with open('outfile4.json') as f1:
        filecontent = f1.readlines()
        samples = random.sample(list(filecontent), 100)
        with open('taggedcmtypes3.json', 'w') as f2:
            for jsample in samples:
                sample = json.loads(jsample)
                words = sample["content"]
                print(words)
                # Prompt to sort into types. Types are as follows:
                # 1. All English
                # 2. All Telugu
                # 3. English grammar with Telugu words
                # 4. Telugu grammar with English words
                # 5. Phrasal flipping (phrase in english, phrase in Telugu)
                # 6. Other
                ptype = ""
                while ptype == "":
                    ptype = input("Type: ")

                sample["ptype"] = int(ptype)
                newjsample = json.dumps(sample)
                f2.write("%s\n" % newjsample)
        print("finished")
main()