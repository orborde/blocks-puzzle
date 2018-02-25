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
    for line in lines[1:]:
        assert len(line) == 7
        occupancy.append([OCC_MAP[c] for c in line])
    return colordata, occupancy

def cube(**kwargs):
    return visual.box(size=(1,1,1), **kwargs)

PIECE_DIR = 'pieces'
def load_raw(piece):
    path = os.path.join(PIECE_DIR, piece)
    data = open(path, 'r').read()
    color, occ = parse(data)
    return color,occ

def spawn_from_raw(color, occ, **kwargs):
    f = visual.frame(**kwargs)
    for row in range(5):
        for col in range(7):
            if occ[row][col]:
                cube(frame=f, pos=(row,col,0), color=color)
    return f

def pieces():
    return [
        f for f in os.listdir(PIECE_DIR)
        if os.path.isfile(os.path.join(PIECE_DIR, f))]

AXES = [
    ( 1, 0, 0),
    (-1, 0, 0),
    ( 0, 1, 0),
    ( 0,-1, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]
AXES_set = set(AXES)

def neg(v):
    return tuple(-e for e in v)

def add(a,b):
    assert len(a) == len(b)
    return tuple(x+y for x,y in zip(a,b))

def compatible(axis, up):
    assert axis in AXES_set
    assert up in AXES_set

    return (
        axis != up and
        up != neg(axis))

def next_axis(axis, up):
    start_idx = AXES.index(axis)
    for adv in xrange(1, len(AXES)):
        idx = (start_idx + adv)%len(AXES)
        cand_axis = AXES[idx]
        if compatible(cand_axis, up):
            return cand_axis
    raise Exception("wtf")

def next_up(axis, up):
    start_idx = AXES.index(up)
    for adv in xrange(1, len(AXES)):
        idx = (start_idx + adv)%len(AXES)
        cand_up = AXES[idx]
        if compatible(axis, cand_up):
            return cand_up
    raise Exception("wtf")

class Piece(object):
    def __init__(self, name, pos):
        # TODO: make public fields properties
        self.name = name
        # Spawn the vobj first so that the property setters work
        # later.
        color, occ = load_raw(name)
        self._vobj = spawn_from_raw(color, occ)
        self._color = color
        self._occ = occ
        self.pos = pos
        self.axis = ( 1, 0, 0)
        self.up = ( 0, 1, 0)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._vobj.pos = pos
        self._pos = pos

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        assert axis in AXES_set
        self._vobj.axis = axis
        self._axis = axis

    @property
    def up(self):
        return self._up

    @up.setter
    def up(self, up):
        assert compatible(self.axis, up)
        self._vobj.up = up
        self._up = up

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, kolor):
        self._color = kolor
        for o in self._vobj.objects:
            o.color = self._color

def main():
    for idx,piece in enumerate(pieces()):
        q = Piece(piece, pos=(idx*6, 0, 0))

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

