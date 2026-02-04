# Use Cases

## When to Use gngram-lookup

### Historical Linguistics

Track when words entered common usage:

```python
import gngram_lookup as ng

# "computer" peaked in the 2000s
ng.frequency('computer')['peak_tf']   # 2000

# "telegram" peaked in the 1920s
ng.frequency('telegram')['peak_tf']   # 1920
```

### NLP Preprocessing

Filter tokens by frequency or existence:

```python
import gngram_lookup as ng

tokens = ['the', 'algorithm', 'xyzabc', 'neural']
real_words = [t for t in tokens if ng.exists(t)]
# ['the', 'algorithm', 'neural']
```

### Data Validation

Check if tokens are real words:

```python
import gngram_lookup as ng

def is_valid_word(word: str) -> bool:
    return ng.exists(word)
```

### Content Analysis

Compare word frequency across eras:

```python
import gngram_lookup as ng

words = ['telegraph', 'telephone', 'internet', 'smartphone']
for word in words:
    freq = ng.frequency(word)
    if freq:
        print(f"{word}: peaked {freq['peak_tf']}, total uses: {freq['sum_tf']}")
```

### Spelling Validation

Quick existence checks without spell correction:

```python
import gngram_lookup as ng

# Simple existence check
ng.exists('receive')    # True
ng.exists('recieve')    # False (misspelling)
```

## What This Package Does Not Do

- No definitions or semantics (use a dictionary)
- No spell correction or suggestions
- No part-of-speech tagging
- No per-year granularity (decades only)
