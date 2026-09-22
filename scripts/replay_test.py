"""Demonstrate duplicate and old sequence rejection."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cloud.verification.replay_checker import accepts_sequence


if __name__ == "__main__":
    last_sequence = 7
    print(f"new sequence accepted: {accepts_sequence(8, last_sequence)}")
    print(f"duplicate sequence accepted: {accepts_sequence(7, last_sequence)} (expected False)")
    print(f"old sequence accepted: {accepts_sequence(6, last_sequence)} (expected False)")
