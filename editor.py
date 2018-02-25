#!/usr/bin/env python

import ast
import itertools
import os
import pdb
import sys
import traceback
import visual

from pieces import *

VALID_ADV = set([-1,1])
class Editor(object):
    def __init__(self, objects):
        self._objects = objects
        # Prime the pump
        self._index = 0
        self._old_color = self.selected().color
        self.index = 0

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, idx):
        self.selected().color = self._old_color
        self._index = idx
        self._old_color = self.selected().color
        self.selected().color = (1, 1, 1)

    def selected(self):
        return self._objects[self._index]

    def obj_sel(self, adv):
        assert adv in VALID_ADV
        self.index = (self.index + adv)%len(self._objects)

    def axis_sel(self):
        obj = self.selected()
        obj.axis = next_axis(obj.axis, obj.up)

    def up_sel(self):
        obj = self.selected()
        obj.up = next_up(obj.axis, obj.up)

    def displace(self, offset):
        obj = self.selected()
        obj.pos = add(obj.pos, offset)

def load_objects(path):
    # TODO: is this ast parsing actually safe?
    f = open(path, 'r')
    objects = []
    for spec in f:
        spec = spec.strip()
        name,pos,axis,up = spec.split(';')
        pos,axis,up = [
            ast.literal_eval(e) for e in
            [pos,axis,up]]
        obj = Piece(name, pos=pos)
        obj.axis = axis
        obj.up = up
        objects.append(obj)
    return objects

def vec2str(vec):
    return '('+','.join('%d'%v for v in vec)+')'

def save_objects(path, objects):
    newpath = path+'.new'
    f = open(newpath, 'w')
    for obj in objects:
        f.write(';'.join(
            [obj.name] + map(vec2str, [obj.pos, obj.axis, obj.up])))
        f.write('\n')
    f.close()
    os.rename(newpath, path)

def main():
    visual.scene.width = 800
    visual.scene.height = 800

    _, target = sys.argv

    if not os.path.exists(target):
        objects = [Piece(name, pos=(-18 + idx*6, 0, 0))
                   for idx,name in enumerate(pieces())]
    else:
        objects = load_objects(target)

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
        elif key == 'l':
            e.axis_sel()
        elif key == 'p':
            e.up_sel()
        else:
            print(repr(key))

        assembly = Assembly()
        for obj in objects:
            assembly.place(
                obj.name, obj.pos, obj.axis, obj.up, obj.occ)

        conflicts = assembly.conflicts
        if len(conflicts) == 0:
            save_objects(target, objects)
        else:
            print len(conflicts),
            print ','.join(
                reduce(lambda x,y: x.union(y), conflicts.values())),
            print 'conflicts; didn\'t save'

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

