#!/usr/bin/env python3
import sys

current_word = None
current_docs = []

# Read from standard input, line by line
for line in sys.stdin:
    # Clean up the line and split into word and docID
    line = line.strip()
    word, doc_id = line.split('\t', 1)

    # This if-statement is the core of the reducer logic.
    # It works because Hadoop sorts the mapper output by key (the word)
    # before sending it to the reducer.
    if current_word == word:
        # This word is the same as the previous one, append its docID
        current_docs.append(doc_id)
    else:
        # We've moved to a new word.
        # First, process and print the results for the PREVIOUS word.
        if current_word:
            # [cite_start]Get the unique docIDs and sort them [cite: 12]
            unique_sorted_docs = sorted(list(set(current_docs)))
            # Format the list as a string
            doc_list_str = f"[{', '.join(unique_sorted_docs)}]"
            print(f'{current_word}\t{doc_list_str}')
        
        # Now, reset the variables for the NEW word.
        current_word = word
        current_docs = [doc_id]

# After the loop, we need to print the last word's data
if current_word:
    unique_sorted_docs = sorted(list(set(current_docs)))
    doc_list_str = f"[{', '.join(unique_sorted_docs)}]"
    print(f'{current_word}\t{doc_list_str}')