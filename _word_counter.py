# ============================================================
# Level 1 - Task 3: Word Counter
# Codveda Python Development Internship
# ============================================================

import os
import re
from collections import Counter

def count_words(filepath):
    """
    Read a text file and return word statistics.
    Raises FileNotFoundError if the file does not exist,
    and IOError for other read problems.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on any whitespace — covers spaces, newlines, tabs
    words = content.split()
    total_words = len(words)

    # Cleaned words (lowercase, letters only) for frequency count
    clean_words = [re.sub(r"[^a-zA-Z]", "", w).lower() for w in words]
    clean_words = [w for w in clean_words if w]  # drop empty strings

    lines = content.splitlines()
    chars_with_spaces    = len(content)
    chars_without_spaces = len(content.replace(" ", "").replace("\n", "").replace("\t", ""))

    frequency = Counter(clean_words)

    return {
        "total_words":           total_words,
        "unique_words":          len(set(clean_words)),
        "total_lines":           len(lines),
        "chars_with_spaces":     chars_with_spaces,
        "chars_without_spaces":  chars_without_spaces,
        "top_10":                frequency.most_common(10),
    }

def display_stats(filepath, stats):
    print("\n" + "=" * 50)
    print(f" Word Count Statistics")
    print(f" File: {filepath}")
    print("=" * 50)
    print(f"  Total words       : {stats['total_words']}")
    print(f"  Unique words      : {stats['unique_words']}")
    print(f"  Total lines       : {stats['total_lines']}")
    print(f"  Characters (w/ sp): {stats['chars_with_spaces']}")
    print(f"  Characters (no sp): {stats['chars_without_spaces']}")

    if stats["top_10"]:
        print("\n  Top 10 most frequent words:")
        for rank, (word, count) in enumerate(stats["top_10"], start=1):
            print(f"    {rank:>2}. '{word}' — {count} time(s)")
    print("=" * 50)

def main():
    print("=" * 50)
    print("         Word Counter")
    print("=" * 50)

    filepath = input("\nEnter the path to the text file: ").strip()

    try:
        stats = count_words(filepath)
        display_stats(filepath, stats)
    except FileNotFoundError as e:
        print(f"\n[Error] {e}")
    except UnicodeDecodeError:
        print("\n[Error] Could not decode the file. Make sure it is a plain text (UTF-8) file.")
    except IOError as e:
        print(f"\n[Error] Could not read the file: {e}")

if __name__ == "__main__":
    main()
