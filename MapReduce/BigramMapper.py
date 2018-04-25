#!/usr/bin/env python

import sys

for line in sys.stdin:
    fields = line.strip().split("")
    sentence = fields[5]
    words = sentence.split()
    mixwords = zip(words[:-1],words[1:])
    for bigram in mixwords:
        print >> sys.stdout, "%s\t%s" % (bigram, 1)
    
