#!/usr/bin/env python3
import argparse
import sys
import tomllib
from pathlib import Path

from src.audacity import AudacityConnector
from src.slot import Slot

cfg = {}


def process_loops():
    from_dir = Path(cfg['loops']['path_raw'])
    to_dir = Path(cfg['loops']['path_processed'])
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    audacity = AudacityConnector(cfg['loops']['gain'], cfg['loops']['bit_depth'])
    for loop in from_dir.glob("*"):
        print(loop)
        audacity.convert(from_dir / loop, to_dir / loop)


def copy_loops():
    from_dir = Path(cfg['loops']['path_processed'])
    storage_dir = Path(cfg['device']['volume']) / Path((cfg['device']['directory']))
    if not storage_dir.exists():
        storage_dir.mkdir()

    for i, loop in enumerate(from_dir.glob("*")):
        print(loop)
        s = Slot(storage_dir, i)
        s.store(loop)


if __name__ == '__main__':
    with open("config.toml", "rb") as f:
        cfg = tomllib.load(f)
    try:
        pass
        # process_loops()
    except RuntimeError as ex:
        print(ex)
        sys.exit(1)
    copy_loops()
