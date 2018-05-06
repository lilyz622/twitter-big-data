#!/usr/bin/env python
import sys

for line in sys.stdin:

    # Extract the needed information
    fields = line.strip().split("")
    name = fields[7]
    print >> sys.stdout, "%s\t%s" % (name, 1)
  
    
    # Print out the intermediate record as "key \t value"
    
