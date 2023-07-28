#!/usr/bin/env python3
import tomllib
from pathlib import Path

from src.audacity import AudacityConnector
from src.pipeclient import PipeClient

cfg = {}


def process_loops():
    audacity = AudacityConnector(cfg['loops']['gain'], cfg['loops']['bit_depth'])
    from_dir = Path(cfg['loops']['path_raw'])
    to_dir = Path(cfg['loops']['path_processed'])
    for loop in from_dir.glob("*"):
        print(loop)
        audacity.convert(from_dir / loop, to_dir / loop)
        return


def copy_loops():
    pass


if __name__ == '__main__':
    with open("config.toml", "rb") as f:
        cfg = tomllib.load(f)
    process_loops()
