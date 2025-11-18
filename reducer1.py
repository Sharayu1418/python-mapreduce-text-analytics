#!/usr/bin/env python3
import sys

for line in sys.stdin:
    # Split the line into word and the doc list string
    word, doc_list_str = line.strip().split('\t', 1)
    
    # Count the number of documents by counting commas and adding 1
    doc_count = doc_list_str.count(',') + 1
    
    # Output: count, word, and the original doc list string
    # We pad the count with leading zeros to ensure correct sorting in the next stage
    print(f"{doc_count:04d}\t{word}\t{doc_list_str}")