#!/usr/bin/env python

import sys

for line in sys.stdin:
    fields = line.strip().split("")
    sentence = fields[5]
    words = sentence.split()
    for word in words:
        print >> sys.stdout, "%s\t%s" % (word, 1)
