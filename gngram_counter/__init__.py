"""gngram-counter: Google Ngram frequency counter."""

from gngram_counter.data import get_data_dir, get_hash_file, is_data_installed
from gngram_counter.lookup import FrequencyData, batch_frequency, exists, frequency

__all__ = [
    "get_data_dir",
    "get_hash_file",
    "is_data_installed",
    "exists",
    "frequency",
    "batch_frequency",
    "FrequencyData",
]
