# gngram-lookup

[![PyPI version](https://badge.fury.io/py/gngram-lookup.svg)](https://badge.fury.io/py/gngram-lookup)
[![Downloads](https://pepy.tech/badge/gngram-lookup)](https://pepy.tech/project/gngram-lookup)
[![Downloads/Month](https://pepy.tech/badge/gngram-lookup/month)](https://pepy.tech/project/gngram-lookup)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Word frequency from 500 years of books. O(1) lookup. 5 million words.**

Fast word existence checking and historical frequency data from Google Books Ngram. Know not just *if* a word exists, but *when* it peaked in usage across five centuries of published text.

## Quick Start

```bash
pip install gngram-lookup
```

After installing, download the data files (~110MB):

```bash
python -m gngram_lookup.download_data
```

```python
import gngram_lookup as ng

# Check if a word exists
ng.exists('computer')       # True
ng.exists('xyznotaword')    # False

# Get frequency data
freq = ng.frequency('computer')
# {'peak_tf': 2000, 'peak_df': 2000, 'sum_tf': 892451, 'sum_df': 312876}

# Batch lookup (efficient for large lists)
results = ng.batch_frequency(['the', 'algorithm', 'xyznotaword'])
# {'the': {...}, 'algorithm': {...}, 'xyznotaword': None}
```

## Features

- **O(1) Lookups** - Hash-bucketed parquet files for instant access
- **5 Million Words** - Comprehensive coverage from Google Books
- **Historical Data** - Peak usage decades from 1500s to 2000s
- **Term + Document Frequency** - Both TF and DF metrics
- **Case Insensitive** - Handles any capitalization
- **Batch Operations** - Efficient multi-word lookups

## The Problem This Solves

You need to know if a word exists *and* how frequently it appears in published text. Not a dictionary lookup (too prescriptive). Not a web scrape (too noisy). You need frequency data from real books across centuries.

```python
import gngram_lookup as ng

# Is this a real word?
ng.exists('computer')      # True
ng.exists('asdfgh')        # False

# When did it peak?
ng.frequency('computer')['peak_tf']   # 2000 - peaked in the 2000s
ng.frequency('telegram')['peak_tf']   # 1920 - peaked in the 1920s
```

## API Reference

### `exists(word: str) -> bool`

Check if a word exists in the corpus.

```python
ng.exists('THE')           # True (case-insensitive)
ng.exists('hello')         # True
ng.exists('asdfgh')        # False
```

### `frequency(word: str) -> FrequencyData | None`

Get frequency data for a word. Returns `None` if not found.

```python
freq = ng.frequency('algorithm')
if freq:
    print(f"Peak decade (TF): {freq['peak_tf']}")   # When it was used most
    print(f"Peak decade (DF): {freq['peak_df']}")   # When it appeared in most books
    print(f"Total TF: {freq['sum_tf']}")            # Total occurrences
    print(f"Total DF: {freq['sum_df']}")            # Total books containing it
```

### `batch_frequency(words: list[str]) -> dict[str, FrequencyData | None]`

Efficient batch lookup. Words are grouped by hash prefix to minimize file reads.

```python
results = ng.batch_frequency(['apple', 'banana', 'notaword'])
for word, freq in results.items():
    if freq:
        print(f"{word}: peaked in {freq['peak_tf']}")
    else:
        print(f"{word}: not found")
```

### `FrequencyData`

| Field | Type | Description |
|-------|------|-------------|
| `peak_tf` | `int` | Decade with highest term frequency (e.g., 1990) |
| `peak_df` | `int` | Decade with highest document frequency |
| `sum_tf` | `int` | Total term frequency across all decades |
| `sum_df` | `int` | Total document frequency across all decades |

### `is_data_installed() -> bool`

Check if data files have been downloaded.

```python
if not ng.is_data_installed():
    print("Run: python -m gngram_lookup.download_data")
```

## Data Structure

The corpus is split into **256 parquet files** (`00.parquet` to `ff.parquet`), bucketed by MD5 hash prefix. This enables O(1) lookups without loading the entire dataset.

```
~/.gngram-lookup/data/
├── 00.parquet
├── 01.parquet
├── ...
└── ff.parquet
```

Each file contains ~19,500 words with the following schema:

| Column | Type | Description |
|--------|------|-------------|
| `hash` | `str` | 30-char MD5 suffix (prefix is the filename) |
| `peak_tf` | `int` | Decade with highest term frequency |
| `peak_df` | `int` | Decade with highest document frequency |
| `sum_tf` | `int` | Total term frequency across all decades |
| `sum_df` | `int` | Total document frequency across all decades |

**Why hash-bucketed?** Words are distributed by MD5 hash to create uniformly-sized files (~430KB each). Looking up a word requires reading only one file, making lookups fast regardless of corpus size.

## Why Google Ngram?

Google Books Ngram represents **500 years of published text** - over 5 million books scanned and indexed. This gives you:

- **Historical depth**: Track word usage from 1500s to 2000s
- **Scale**: 5+ million unique words
- **Authority**: Published books, not web noise
- **Temporal precision**: Peak usage by decade

## When to Use This

- **Historical linguistics**: When did a word enter common usage?
- **NLP preprocessing**: Filter by frequency or existence
- **Data validation**: Is this token a real word?
- **Content analysis**: Compare word frequency across eras
- **Spelling validation**: Quick existence checks

## What This Doesn't Do

- No definitions or semantics (use a dictionary for that)
- No spell correction or suggestions
- No part-of-speech tagging
- No per-year granularity (decades only)

## Low-level API

For direct parquet file access:

```python
from gngram_lookup import get_hash_file
import polars as pl
import hashlib

word = "example"
h = hashlib.md5(word.lower().encode()).hexdigest()
df = pl.read_parquet(get_hash_file(h[:2]))
rows = df.filter(pl.col("hash") == h[2:])
```

## Development

```bash
git clone https://github.com/craigtrim/gngram-lookup.git
cd gngram-lookup
make install          # Install dependencies
make test             # Run tests
make lint             # Run linter
make build-hash       # Build hash files from source parquet
make package-release  # Create parquet-hash.tar.gz
make release VERSION=v1.1.0  # Create GitHub release
```

## License

MIT

## Attribution

This package uses data derived from the Google Books Ngram dataset:

> Google Books Ngram Viewer: https://books.google.com/ngrams
>
> Michel, Jean-Baptiste, et al. "Quantitative Analysis of Culture Using Millions of Digitized Books." Science 331.6014 (2011): 176-182.

**Note:** This is a processed snapshot of Google Ngram frequency data. The data is not automatically updated.

## See Also

- **[bnc-lookup](https://github.com/craigtrim/bnc-lookup)** - Similar O(1) lookup using the British National Corpus
- **[wordnet-lookup](https://github.com/craigtrim/wordnet-lookup)** - O(1) lookup using the WordNet lexicon

## Links

- **Repository**: [github.com/craigtrim/gngram-lookup](https://github.com/craigtrim/gngram-lookup)
- **PyPI**: [pypi.org/project/gngram-lookup](https://pypi.org/project/gngram-lookup)
- **Google Ngram**: [books.google.com/ngrams](https://books.google.com/ngrams)
- **Author**: Craig Trim ([craigtrim@gmail.com](mailto:craigtrim@gmail.com))
