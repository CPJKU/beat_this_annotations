#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
import re

import numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit


def read_artist(fn):
    # read artist name from a metadata file
    with open(fn) as f:
        for line in f:
            if line.startswith("Artist:"):
                return line.rstrip().split(":", 1)[1]
    return None


def main():
    # read metadata as mapping artist -> tracklist
    metadata_dir = Path(__file__).parent / "annotations" / "metadata"
    collection = defaultdict(list)
    for fn in sorted(metadata_dir.glob("*.txt")):
        collection[read_artist(fn).lower()].append(fn.stem)

    # merge artists that collaborated
    while True:
        # find an artist name that is contained in other artist names
        for artist in collection:
            if artist:
                regexp = re.compile(r"\b" + re.escape(artist) + r"\b")
                mergable = [
                    candidate
                    for candidate in collection
                    if len(artist) < len(candidate) and regexp.search(candidate)
                ]
                if mergable:
                    break
        # merge all those artists together
        if mergable:
            artist_group = "|".join(sorted(set(mergable)))
            collection[artist_group] = sum(
                (collection.pop(name) for name in [artist] + mergable), []
            )
        # stop if there are no possible mergers
        if not mergable:
            break

    # bring into (item, class) form
    items = sorted(
        (fn, artist_group) for artist_group, fns in collection.items() for fn in fns
    )
    fns, artist_groups = zip(*items)

    # create the 15% validation split
    sf = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=42)
    train, valid = next(sf.split(fns, [0] * len(items), artist_groups))
    train_valid = [(fns[idx], "train") for idx in train] + [
        (fns[idx], "val") for idx in valid
    ]
    with open(Path(__file__).parent / "single.split", "w") as f:
        f.writelines(f"{fn}\t{group}\n" for fn, group in sorted(train_valid))

    # create the 8-fold split (with a random seed resulting in good balance)
    best_entropy = 0
    best_splits = None
    for seed in range(300):
        kf = GroupKFold(n_splits=8, shuffle=True, random_state=seed)
        splits = [val for _, val in kf.split(fns, [0] * len(items), artist_groups)]
        counts = np.asarray([len(val) for val in splits])
        entropy = sum(-p * np.log2(p) for p in counts / counts.sum())
        if entropy > best_entropy:
            best_entropy = entropy
            best_splits = splits
    splits = best_splits
    splits = sorted((fns[idx], k) for k, val in enumerate(splits) for idx in val)
    with open(Path(__file__).parent / "8-folds.split", "w") as f:
        f.writelines(f"{fn}\t{idx}\n" for fn, idx in splits)


if __name__ == "__main__":
    main()
