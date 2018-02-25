#!/usr/bin/env python

import itertools
import pdb
import pieces
import sys
import traceback

AXES = [
    ( 1, 0, 0),
    (-1, 0, 0),
    ( 0, 1, 0),
    ( 0,-1, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]
def main():
    for row,(axis,up) in enumerate(
            itertools.permutations(AXES,r=2)):
        for col,piece in enumerate(pieces.pieces()):
            pieces.spawn(
                piece,
                pos=(col*14, row*14, 0),
                axis=axis, up=up)


if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

