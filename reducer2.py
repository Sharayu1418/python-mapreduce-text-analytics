#!/usr/bin/env python3
import sys

top_n = 10
lines_printed = 0

for line in sys.stdin:
    # We only print if we haven't printed 10 lines yet
    if lines_printed < top_n:
        # Split the line into its components
        doc_count, word, doc_list_str = line.strip().split('\t', 2)
        
        # Reformat for the final desired output
        print(f"{word} | {int(doc_count)} | {doc_list_str}")
        lines_printed += 1
    
    # We don't use 'else: break' here. The loop will continue
    # to read and discard the rest of the input lines without printing them.