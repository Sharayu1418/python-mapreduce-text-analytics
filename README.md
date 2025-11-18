## Playing with MapReduce (Inverted Index + Top‑10 Words)

This repo consits of me **experimenting with how Hadoop Streaming mappers and reducers work** on a small text‑processing task.

The main idea I played with is:

- **Build an inverted index**: for each word, list which files it appears in.
- **Compute the “top 10” most frequent words (by document count)**.

All of this is done with **plain Python scripts** wired together in a typical **Unix / Hadoop Streaming style pipeline**.
---

## Repo layout

- **`mapper.py`**: real mapper for the inverted index.  
  - Reads text, normalizes and cleans it, and emits `word<TAB>docID`.  
  - Uses the Hadoop env var `mapreduce_map_input_file` so each word is tagged with its source file.
- **`reducer.py`**: reducer that builds the inverted index.  
  - Groups `word<TAB>docID` pairs, deduplicates doc IDs, sorts them, and prints  
    `word<TAB>[doc1, doc2, ...]`.
- **`reducer1.py`**: second‑stage reducer.  
  - Takes the inverted index and turns it into `docCount<TAB>word<TAB>[doc list]` so it’s easy to sort.
- **`reducer2.py`**: final reducer for the **top‑10** words.  
  - Reads sorted data and prints only the 10 most frequent words plus their document lists.
- **`mapper1.py`, `mapper2.py`**: tiny “pass‑through” mappers I used while getting comfortable with the streaming flow and testing stages.
- **Result samples**:  
  - `inverted_index_results*.txt` – example inverted index output.  
  - `top10_results.txt` – example “top 10 words” output.

---

## How the pipeline works (conceptually)

1. **Mapper – build word/doc pairs**
   - Input: raw text files.
   - Output: `word<TAB>docID`.
2. **Reducer – build inverted index**
   - Input: mapper output, sorted by word (Hadoop does this sort step).
   - Output: `word<TAB>[doc1, doc2, ...]`.
3. **Reducer1 – count how many documents each word appears in**
   - Input: inverted index.
   - Output: `docCount<TAB>word<TAB>[doc list]`.
4. **Sort by count (descending)**
   - Done with standard Unix `sort` in the shell (or by Hadoop’s sorting, depending on setup).
5. **Reducer2 – keep only the top 10**
   - Input: sorted by docCount.
   - Output: `word | docCount | [doc list]`.

---

## Running things locally (no real cluster required)

You can fake the Hadoop Streaming behavior with standard pipes:

```bash
# From inside the project directory:

# 1) Simulate mapper + reducer to build the inverted index
cat *.txt \
  | MAPREDUCE_MAP_INPUT_FILE=dummy.txt ./mapper.py \
  | sort \
  | ./reducer.py > inverted_index_results.txt

# 2) Turn the inverted index into counts and pick the top‑10
cat inverted_index_results.txt \
  | ./reducer1.py \
  | sort -r \
  | ./reducer2.py > top10_results.txt
```

Note: on Windows you may need to adapt the shebangs or run with `python mapper.py` instead of `./mapper.py`.

---

## What I was trying to learn

- **How a mapper is supposed to behave**: stateless, line‑oriented, emitting simple key/value pairs.
- **How a reducer typically looks**: assumes sorted input, keeps some state for the “current key”, and flushes when the key changes.
- **How multiple MapReduce stages can be chained**: using intermediate formats so each stage is simple but composable.
- **How to prototype Hadoop Streaming jobs locally** using just `python`, `cat`, and `sort` before touching a real cluster.

If you’re also curious about MapReduce, feel free to clone this and tweak the scripts, add new stages, or change the output format.


