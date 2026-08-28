from display import format_results, display_rich_ui
from permuter import trie_permuter
from trie import build_trie

import time

# getting words
import nltk
# nltk.download('words')  # run once to download the corpus
from nltk.corpus import words

valid_words = set(w.lower() for w in words.words())

trie_root = build_trie(valid_words)

scrambled_string = "permeations"

# start time
start_time = time.perf_counter()

# run workload
matches = []
for perm in trie_permuter(scrambled_string, trie_root):
    if perm in valid_words and len(perm) != 1:
        matches.append(perm)

# stop time
end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"found matches: {matches}")
print(f"execution time: {execution_time} seconds")
display_rich_ui(format_results(matches), scrambled_string, execution_time)
