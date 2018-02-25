#!/usr/bin/env python

import os
import pdb
import sys
import traceback
import visual

OCCUPIED = '#'
SPACE = ' '

OCC_MAP = {
    OCCUPIED: True,
    SPACE:    False,
}

def parse(filedata):
    lines = filedata.strip().splitlines()
    assert len(lines) == 6
    colordata = map(float, lines[0].split())
    assert len(colordata) == 3

    occupancy = []
    for line in lines:
        assert len(line) == 7
        occupancy.append([OCC_MAP[c] for c in line])
    return colordata, occupancy

def cube(**kwargs):
    return visual.box(size=(1,1,1), **kwargs)

PIECE_DIR = 'pieces'
def spawn(piece, **kwargs):
    path = os.path.join(PIECE_DIR, piece)
    data = open(path, 'r').read()
    color, occ = parse(data)

    f = visual.frame(**kwargs)
    for row in range(5):
        for col in range(7):
            cube(frame=f, pos=(row,col,0), color=color)
    return f

def pieces():
    return [
        f for f in os.listdir(PIECE_DIR)
        if os.path.isfile(os.path.join(PIECE_DIR, f))]

def main():
    for idx,piece in enumerate(pieces()):
        spawn(piece, pos=(idx*6, 0, 0))


if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

