# gngram-counter

Google Ngram frequency lookup using hash-bucketed parquet files.

## Installation

```bash
pip install gngram-counter
```

After installing, download the data files:

```bash
python -m gngram_counter.download_data
```

This downloads ~110MB of parquet files to `~/.gngram-counter/data/`.

## Usage

```python
from gngram_counter import exists, frequency, batch_frequency

# Check if a word exists
exists("example")  # True
exists("xyznotaword")  # False

# Get frequency data for a word
freq = frequency("example")
# {'peak_tf': 1990, 'peak_df': 1990, 'sum_tf': 12345, 'sum_df': 9876}

# Batch lookup for multiple words
results = batch_frequency(["the", "example", "xyznotaword"])
# {'the': {...}, 'example': {...}, 'xyznotaword': None}
```

### Low-level API

For direct parquet access:

```python
from gngram_counter import get_hash_file, is_data_installed
import polars as pl
import hashlib

word = "example"
h = hashlib.md5(word.encode()).hexdigest()
df = pl.read_parquet(get_hash_file(h[:2]))
row = df.filter(pl.col("hash") == h[2:])
```

## Data Schema

Each parquet file contains:
- `hash`: 30-char MD5 suffix (prefix is the filename)
- `peak_tf`: decade with highest term frequency
- `peak_df`: decade with highest document frequency
- `sum_tf`: total term frequency across all decades
- `sum_df`: total document frequency across all decades

## Development

```bash
# Install dependencies
make install

# Run tests
make test

# Build hash files from source parquet
make build-hash

# Package for GitHub release
make package-release
```

## Release Workflow

1. Build hash files: `make build-hash`
2. Package: `make package-release` (creates `parquet-hash.tar.gz`)
3. Create GitHub release, upload `parquet-hash.tar.gz`
4. Update `DATA_VERSION` in `gngram_counter/download_data.py` if needed
