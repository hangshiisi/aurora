#!/usr/bin/env python

#from operator import itemgetter
from collections import defaultdict


import sys

NUMBERS = 10 

current_word = None
current_count = 0.0
word = None
my_counter = defaultdict(float) 

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # convert count (currently a string) to int
    try:
        # parse the input we got from mapper.py
        word, count = line.split(',', 1)
        #print "count, word", word, count
        count = float(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            #print '%s,%s' % (current_word, current_count)
            my_counter[current_word] += current_count 
        current_count = count
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    #print '%s,%s' % (current_word, current_count)
    my_counter[current_word] += current_count 

sorted_counter = sorted(my_counter.iteritems() , key= lambda (k, v):(v, k))

for v in sorted_counter[:NUMBERS]: 
    print("%s,%s"% (v[0],  v[1]))

