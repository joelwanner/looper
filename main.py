#!/usr/bin/env python3
import tomllib

cfg = {}


def convert():
    pass


def copy():
    pass


if __name__ == '__main__':
    with open("config.toml", "rb") as f:
        cfg = tomllib.load(f)
    print(cfg)
