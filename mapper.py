#!/usr/bin/env python3
import sys
import os
import re

# Hadoop Streaming mapper: emit "word<TAB>docID"
pathname = os.environ.get('mapreduce_map_input_file')  # docID source
filename = os.path.basename(pathname)

for line in sys.stdin:
    line = line.strip()              # drop surrounding whitespace
    if not line:
        continue                     # skip blank lines

    line = line.lower()              # normalize case
    line = re.sub(r'[^a-zA-Z0-9\s]', '', line)  # remove punctuation

    words = line.split()             # tokenize on whitespace

    for word in words:
        print(f'{word}\t{filename}') # key-value: word<TAB>docID
