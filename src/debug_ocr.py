import sys

from read_document import read_document

words = read_document(sys.argv[1])[1]
for i, w in enumerate(words):
    if "Receipt" in w["text"] or "18873" in w["text"]:
        for v in words[i:i + 3]:
            print(repr(v["text"]), "conf", round(v["conf"]), "box", v["x"], v["y"], v["w"], v["h"])
        print("--")