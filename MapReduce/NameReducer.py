#!/usr/bin/env python

import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

total = 0.0
prev_key = False
	
for line in sys.stdin:
    data = line.strip().split("\t")
		
    # Make sure you got all data and also check the type
    if len(data)!=2 or not is_number(data[1]):
        continue
		
    key = data[0]
    value = data[1]
		
    if prev_key and prev_key!=key:
        # We moved to a different location: stream out
        print>>sys.stdout, "%s\t%s" % (prev_key,total)
        total = 0.0
		
    prev_key = key
    total = total + float(value)
		
#We need to stream the total from the last location
print>>sys.stdout, "%s\t%s" % (prev_key,total)
