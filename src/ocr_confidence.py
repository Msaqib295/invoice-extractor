import glob
import sys

from read_document import mean_confidence, read_document

paths = [p for arg in sys.argv[1:] for p in (glob.glob(arg) or [arg])]
for path in sorted(paths):
    mc = mean_confidence(read_document(path)[1])
    print(path, "mean confidence:", "n/a (digital PDF)" if mc is None else round(mc, 1))