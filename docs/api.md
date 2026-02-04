# API Reference

## Functions

### `exists(word: str) -> bool`

Check if a word exists in the corpus.

```python
import gngram_lookup as ng

ng.exists('THE')           # True (case-insensitive)
ng.exists('hello')         # True
ng.exists('asdfgh')        # False
```

### `frequency(word: str) -> FrequencyData | None`

Get frequency data for a word. Returns `None` if not found.

```python
import gngram_lookup as ng

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
import gngram_lookup as ng

results = ng.batch_frequency(['apple', 'banana', 'notaword'])
for word, freq in results.items():
    if freq:
        print(f"{word}: peaked in {freq['peak_tf']}")
    else:
        print(f"{word}: not found")
```

### `is_data_installed() -> bool`

Check if data files have been downloaded.

```python
import gngram_lookup as ng

if not ng.is_data_installed():
    print("Run: python -m gngram_lookup.download_data")
```

### `get_hash_file(prefix: str) -> Path`

Return path to a specific hash bucket parquet file. For direct file access.

```python
from gngram_lookup import get_hash_file
import polars as pl
import hashlib

word = "example"
h = hashlib.md5(word.lower().encode()).hexdigest()
df = pl.read_parquet(get_hash_file(h[:2]))
rows = df.filter(pl.col("hash") == h[2:])
```

### `get_data_dir() -> Path`

Return the data directory path (`~/.gngram-lookup/data/`).

## Types

### `FrequencyData`

A TypedDict with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `peak_tf` | `int` | Decade with highest term frequency (e.g., 1990) |
| `peak_df` | `int` | Decade with highest document frequency |
| `sum_tf` | `int` | Total term frequency across all decades |
| `sum_df` | `int` | Total document frequency across all decades |
