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

def fill_via_func(fill, occ):
    for row in range(5):
        for col in range(7):
            if occ[row][col]:
                x,y,z = row,col,0
                fill(x,y,z)

def spawn_from_raw(color, occ, **kwargs):
    f = visual.frame(**kwargs)

    def fill(x,y,z):
        cube(frame=f, pos=(x,y,z), color=color)

    fill_via_func(fill, occ)
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

def sub(a,b):
    return add(a, neg(b))

def mul(k, v):
    return tuple(k*e for e in v)

def max_pairwise(a,b):
    return tuple(max(x,y) for x,y in zip(a,b))

def min_pairwise(a,b):
    return tuple(min(x,y) for x,y in zip(a,b))

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
        self.occ = occ
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

RADIUS=20
SIDELENGTH=RADIUS*2+1
class Assembly:
    def __init__(self):
        self._array = []
        self._bbox_low  = (0, 0, 0)
        self._bbox_high = (0, 0, 0)
        for x in range(SIDELENGTH):
            plane = []
            for y in range(SIDELENGTH):
                row = [set() for _ in xrange(SIDELENGTH)]
                plane.append(row)
            assert len(plane) == SIDELENGTH
            self._array.append(plane)

        self._lowcorner = (-RADIUS,-RADIUS,-RADIUS)
        self.conflicts = set()

    def pos2index(self, pos):
        index = sub(pos, self._lowcorner)
        assert all(r>=0 for r in index)
        return index

    def index2pos(self, index):
        pos = add(index, self._lowcorner)
        assert all(l <= p for l,p in zip(self._lowcorner,pos))
        return pos

    def addtopos(self, pos, val):
        index = self.pos2index(pos)
        i,j,k = index
        self._array[i][j][k].add(val)

    def getpos(self, pos):
        index = self.pos2index(pos)
        i,j,k = index
        return self._array[i][j][k]

    def all_positions(self):
        for i in xrange(len(self._array)):
            for j in xrange(len(self._array[i])):
                for k in xrange(len(self._array[j])):
                    yield self.index2pos( (i,j,k) )

    def place(self, name, pos, axis, up, occ):
        def fill(x,y,z):
            assert z == 0
            spotpos = add(pos, add(mul(x, axis), mul(y, up)))

            if len(self.getpos(spotpos)) > 0:
                self.conflicts.add(spotpos)

            self._bbox_low = min_pairwise(spotpos, self._bbox_low)
            self._bbox_high = max_pairwise(spotpos, self._bbox_high)
            self.addtopos(spotpos, name)
        fill_via_func(fill, occ)

    def bbox_center(self):
        sm = add(self._bbox_low, self._bbox_high)
        center = mul(0.5, sm)
        center = tuple(map(int, center))
        return center

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

