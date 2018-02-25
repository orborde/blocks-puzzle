#!/usr/bin/env python

import itertools
import pdb
import sys
import traceback
import visual

from pieces import *

VALID_ADV = set([-1,1])
class Editor(object):
    def __init__(self, objects):
        self._objects = objects
        self._index = 0

    def selected(self):
        return self._objects[self._index]

    def obj_sel(self, adv):
        assert adv in VALID_ADV
        self._index = (self._index + adv)%len(self._objects)

    def axis_sel(self):
        obj = self.selected()
        obj.axis = next_axis(obj.axis, obj.up)

    def up_sel(self):
        obj = self.selected()
        obj.up = next_up(obj.axis, obj.up)

    def displace(self, offset):
        obj = self.selected()
        obj.pos = add(obj.pos, offset)

def main():
    objects = [Piece(name, pos=(-18 + idx*6, 0, 0))
               for idx,name in enumerate(pieces())]
    e = Editor(objects)

    while True:
        print 'now controlling', e.selected().name

        key = visual.scene.kb.getkey()

        if key == 'e':
            e.displace( ( 0, 0,-1) )
        elif key == 'q':
            e.displace( ( 0, 0, 1) )
        elif key == 'a':
            e.displace( (-1, 0, 0) )
        elif key == 'd':
            e.displace( ( 1, 0, 0) )
        elif key == 'w':
            e.displace( ( 0, 1, 0) )
        elif key == 's':
            e.displace( ( 0,-1, 0) )
        elif key == '\t':
            e.obj_sel(1)
        elif key == '`':
            e.obj_sel(-1)
        else:
            print(repr(key))

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

