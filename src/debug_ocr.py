import sys

from read_document import read_document

text, words = read_document(sys.argv[1])
for line in text.splitlines():
    if "receipt" in line.lower():
        print(repr(line))
print([w["text"] for w in words if "004" in w["text"] or w["text"] in ("O", "0")])