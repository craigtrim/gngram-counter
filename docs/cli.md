# CLI Reference

## Commands

### `gngram-exists`

Check if a word exists in the corpus.

```bash
gngram-exists computer
# Output: True
# Exit code: 0

gngram-exists xyznotaword
# Output: False
# Exit code: 1
```

Use in shell scripts:

```bash
if gngram-exists "$word"; then
    echo "$word is a real word"
fi
```

### `gngram-freq`

Get frequency data for a word.

```bash
gngram-freq computer
# Output:
# peak_tf_decade: 2000
# peak_df_decade: 2000
# sum_tf: 892451
# sum_df: 312876
```

Exit code is 1 if word not found:

```bash
gngram-freq xyznotaword
# Output: None
# Exit code: 1
```

### `python -m gngram_lookup.download_data`

Download the data files (~110MB). Required before first use.

```bash
python -m gngram_lookup.download_data
```

Data is stored in `~/.gngram-lookup/data/`.
