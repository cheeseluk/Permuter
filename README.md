# Permuter Engine

A highly optimized, trie-based word unscrambler. Give it a scrambled string (a "rack") and it returns every valid dictionary word that can be formed from a subset of those letters — i.e. the full power set of unscrambles, not just full-length anagrams.

This was mainly a for-fun project born out of wanting scrabble/anagram-solving to be *fast*.

## How fast?

All benchmarks below were run on a **Ryzen 9 7900X**.

| Rack | Letters | Valid words found | Execution time |
|---|---|---|---|
| `PERMEATIONS` | 11 | 1,906 | **0.006559s** |
| `PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS` | 45 | 25,636 | **0.223440s** |

Sample output:

```
┌─────────────────── Permuter Scooter Engine ───────────────────┐
│ Rack Submitted: PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS │
│ Search Execution Time: 0.223440 seconds                       │
│ Total Valid Words Found: 25636                                │
└───────────────────────────────────────────────────────────────┘
```

Note that timing excludes dictionary loading and trie construction — it measures only the search/permutation step, since that's the part actually being optimized.

## Why it's fast

A naive anagram solver generates every permutation of a string and then checks each one against a dictionary — this blows up factorially (11 letters = ~40 million permutations) and wastes enormous effort building strings that don't correspond to any real word.

This project avoids that by walking a **trie (prefix tree)** of the dictionary *while* generating permutations, so the two processes prune each other:

- **Dictionary as a trie**: every valid word is loaded once into a nested-dictionary trie (`trie.py`), where each node represents a shared prefix. This lets prefix lookups happen in O(1) per character instead of scanning the whole dictionary.
- **Prefix-pruned permutation generation**: `permuter.py` recursively builds permutations of the scrambled string, but at every step it checks whether the prefix built so far exists in the trie. If a prefix isn't a path in the trie, there is no word in the dictionary that starts with it — so that entire branch of the permutation tree is abandoned immediately, rather than being fully generated and then discarded.
- **Duplicate letter handling**: a `seen_characters` set at each recursion level skips repeated letters at that position, avoiding redundant identical branches when the input has repeated letters (e.g. the many `O`s and `C`s in `PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS`).
- **Wildcard support**: the permuter also supports a `?` wildcard character, which expands to every child key at that trie node — useful for "unscramble with one blank tile" style queries.

In short: instead of generate-then-filter, this is filter-*while*-generating, so the search space collapses to roughly the shape of the dictionary trie itself rather than the full factorial permutation space of the input.

## Project structure

```
.
├── main.py       # Entry point: loads the dictionary, builds the trie, runs a search, prints results
├── trie.py       # Builds a trie (nested dict) out of a set of dictionary words
├── permuter.py   # Trie-pruned recursive permutation generator (the core algorithm)
├── display.py    # Groups/sorts results by word length and renders a Rich-based terminal UI
└── README.md
```

## How it works, file by file

### `trie.py`
Builds the dictionary trie. Each node is a plain `dict`; a special `'_is_word'` key marks that the path traversed so far spells a complete valid word. This is what lets the permuter check "is this prefix even worth continuing?" in constant time per character.

### `permuter.py`
The core algorithm. `trie_permuter(string, current_trie_node)` is a generator that:
1. Tries each unique character remaining in the string at the current position.
2. Checks if that character exists as a child of the current trie node — if not, skips it (this is the pruning step).
3. If the resulting node is marked `_is_word`, yields the current prefix as a found word.
4. Recurses into the remaining letters and the deeper trie node, yielding every valid continuation.
5. Optionally handles a `?` wildcard by expanding to all children of the current node.

### `display.py`
Post-processing and presentation only — no part of the timed search. `format_results` groups the found words by length (longest first). `display_rich_ui` renders a summary panel and a results table using [`rich`](https://github.com/Textualize/rich).

### `main.py`
Wires it all together: loads the NLTK `words` corpus, builds the trie once, times the `permuter.py` search over a given scrambled string, and hands the results to `display.py` for pretty-printing.

## Requirements

- Python 3.8+
- [`nltk`](https://www.nltk.org/) (with the `words` corpus — run `nltk.download('words')` once)
- [`rich`](https://pypi.org/project/rich/)

```bash
pip install nltk rich
python -c "import nltk; nltk.download('words')"
```

## Usage

Edit the `scrambled_string` variable in `main.py`, then run:

```bash
python main.py
```

```python
scrambled_string = "permeations"
```

Use `?` in the string as a wildcard tile:

```python
scrambled_string = "perm?tions"
```

## Notes / caveats

- This finds every valid word that's a subset of the input letters (any length ≥ 2), not just full-length anagrams — the "power set of unscrambles."
- Dictionary quality is entirely dependent on NLTK's `words` corpus, which includes some obscure/archaic entries and is missing some modern words — swap in a different word list if you want different coverage.
- Timing numbers above are search-only (post trie-construction) and were measured on a Ryzen 9 7900X; expect variance on other hardware.
