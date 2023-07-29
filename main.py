#!/usr/bin/env python3
import argparse
import sys
import tomllib
import shutil
from pathlib import Path

from src.audacity import AudacityConnector
from src.slot import Slot

cfg = {}


def process_loops():
    from_dir = Path(cfg['loops']['path_raw'])
    to_dir = Path(cfg['loops']['path_processed'])
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    # Filename pre-processing
    for loop in from_dir.glob("*"):
        shutil.move(loop, loop.parent / loop.name.replace(' ', '_'))

    audacity = AudacityConnector(cfg['loops']['gain'], cfg['loops']['bit_depth'])
    files = list(from_dir.glob("*.aiff")) + list(from_dir.glob("*.wav"))
    for loop in files:
        print(loop)
        audacity.convert(from_dir / loop, to_dir / loop)


def copy_loops():
    from_dir = Path(cfg['loops']['path_processed'])
    storage_dir = Path(cfg['device']['volume']) / Path((cfg['device']['directory']))
    if not storage_dir.exists():
        storage_dir.mkdir()

    for i, loop in enumerate(from_dir.glob("*")):
        print(loop)
        slot = Slot(storage_dir, i+1)  # Start at 01
        slot.store(loop)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--process', action='store_true')
    parser.add_argument('--copy', action='store_true')
    args = parser.parse_args()

    with open("config.toml", "rb") as f:
        cfg = tomllib.load(f)

    if not args.process and not args.copy:
        parser.print_help()
        sys.exit(1)

    if args.process:
        try:
            process_loops()
        except RuntimeError as ex:
            print(ex)
            sys.exit(1)

    if args.copy:
        copy_loops()
