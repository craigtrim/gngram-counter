# Data Format

## Overview

The corpus is split into 256 parquet files (`00.parquet` to `ff.parquet`), bucketed by MD5 hash prefix. This enables O(1) lookups without loading the entire dataset.

## File Structure

```
~/.gngram-lookup/data/
├── 00.parquet
├── 01.parquet
├── ...
└── ff.parquet
```

Each file contains ~19,500 words (~430KB per file).

## Schema

| Column | Type | Description |
|--------|------|-------------|
| `hash` | `str` | 30-char MD5 suffix (prefix is the filename) |
| `peak_tf` | `int` | Decade with highest term frequency |
| `peak_df` | `int` | Decade with highest document frequency |
| `sum_tf` | `int` | Total term frequency across all decades |
| `sum_df` | `int` | Total document frequency across all decades |

## Why Hash-Bucketed?

Words are distributed by MD5 hash to create uniformly-sized files. Looking up a word requires reading only one file, making lookups fast regardless of corpus size.

The lookup process:

1. Compute MD5 hash of lowercase word
2. Use first 2 hex chars as bucket (filename)
3. Search for remaining 30 chars in that file

```python
import hashlib

word = "computer"
h = hashlib.md5(word.lower().encode()).hexdigest()
# h = "df53ca268240ca76670c8566ee54568a"
# bucket = "df" -> df.parquet
# search for hash = "53ca268240ca76670c8566ee54568a"
```

## Data Source

Data is derived from the Google Books Ngram dataset:

- 500 years of published text (1500s to 2000s)
- Over 5 million books scanned and indexed
- 5+ million unique words

The data represents a processed snapshot and is not automatically updated.
