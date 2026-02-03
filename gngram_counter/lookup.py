"""
High-level lookup API for gngram-counter.

Provides simple functions for word frequency lookups similar to bnc-lookup.
"""

import hashlib
from functools import lru_cache
from typing import TypedDict

import polars as pl

from gngram_counter.data import get_hash_file, is_data_installed


class FrequencyData(TypedDict):
    """Frequency data for a word."""

    peak_tf: int  # Decade with highest term frequency
    peak_df: int  # Decade with highest document frequency
    sum_tf: int  # Total term frequency across all decades
    sum_df: int  # Total document frequency across all decades


@lru_cache(maxsize=256)
def _load_bucket(prefix: str) -> pl.DataFrame:
    """Load and cache a parquet bucket file."""
    return pl.read_parquet(get_hash_file(prefix))


def _hash_word(word: str) -> tuple[str, str]:
    """Hash a word and return (prefix, suffix)."""
    h = hashlib.md5(word.lower().encode("utf-8")).hexdigest()
    return h[:2], h[2:]


def exists(word: str) -> bool:
    """Check if a word exists in the ngram data.

    Args:
        word: The word to check (case-insensitive)

    Returns:
        True if the word exists, False otherwise

    Raises:
        FileNotFoundError: If data files are not installed
    """
    if not is_data_installed():
        raise FileNotFoundError(
            "Data files not installed. Run: python -m gngram_counter.download_data"
        )

    prefix, suffix = _hash_word(word)
    df = _load_bucket(prefix)
    return len(df.filter(pl.col("hash") == suffix)) > 0


def frequency(word: str) -> FrequencyData | None:
    """Get frequency data for a word.

    Args:
        word: The word to look up (case-insensitive)

    Returns:
        FrequencyData dict with peak_tf, peak_df, sum_tf, sum_df, or None if not found

    Raises:
        FileNotFoundError: If data files are not installed
    """
    if not is_data_installed():
        raise FileNotFoundError(
            "Data files not installed. Run: python -m gngram_counter.download_data"
        )

    prefix, suffix = _hash_word(word)
    df = _load_bucket(prefix)
    row = df.filter(pl.col("hash") == suffix)

    if len(row) == 0:
        return None

    return FrequencyData(
        peak_tf=row["peak_tf"][0],
        peak_df=row["peak_df"][0],
        sum_tf=row["sum_tf"][0],
        sum_df=row["sum_df"][0],
    )


def batch_frequency(words: list[str]) -> dict[str, FrequencyData | None]:
    """Get frequency data for multiple words.

    Args:
        words: List of words to look up (case-insensitive)

    Returns:
        Dict mapping each word to its FrequencyData or None if not found

    Raises:
        FileNotFoundError: If data files are not installed
    """
    if not is_data_installed():
        raise FileNotFoundError(
            "Data files not installed. Run: python -m gngram_counter.download_data"
        )

    # Group words by bucket prefix for efficient batch lookups
    by_prefix: dict[str, list[tuple[str, str]]] = {}
    for word in words:
        prefix, suffix = _hash_word(word)
        if prefix not in by_prefix:
            by_prefix[prefix] = []
        by_prefix[prefix].append((word, suffix))

    results: dict[str, FrequencyData | None] = {}

    for prefix, word_suffix_pairs in by_prefix.items():
        df = _load_bucket(prefix)
        suffixes = [s for _, s in word_suffix_pairs]

        # Filter to all matching suffixes at once
        matches = df.filter(pl.col("hash").is_in(suffixes))
        match_dict = {row["hash"]: row for row in matches.iter_rows(named=True)}

        for word, suffix in word_suffix_pairs:
            if suffix in match_dict:
                row = match_dict[suffix]
                results[word] = FrequencyData(
                    peak_tf=row["peak_tf"],
                    peak_df=row["peak_df"],
                    sum_tf=row["sum_tf"],
                    sum_df=row["sum_df"],
                )
            else:
                results[word] = None

    return results
