#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class ModuleTopBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dx=None, dy=None, dz=None, positions=None, subtractions=None, material=None, **kwds ):
        self.dx, self.dy, self.dz = ( dx, dy, dz)
        self.positions = positions
        self.subtractions = subtractions
        self.Material = material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct box shape
        main_shape = geom.shapes.Box( self.name, dx=self.dx, dy=self.dy, dz=self.dz )
        main_lv = geom.structure.Volume('vol'+main_shape.name, material=self.Material, shape=main_shape)
        self.add_volume( main_lv )  

        # place feedthroughs
        sbs = self.get_builders()
        modft63_lv  = sbs[0].get_volume()
        modft100_lv = sbs[1].get_volume()

        modft100pos = self.positions[0]
        modft63pos1 = self.positions[1]
        modft63pos2 = self.positions[2]

        relpos100 = geom.structure.Position(self.name+'100ModuleFT_pos', modft100pos[0], modft100pos[1], modft100pos[2])
        relpos63_1 = geom.structure.Position(self.name+'63ModuleFT1_pos', modft63pos1[0], modft63pos1[1], modft63pos1[2])  
        relpos63_2 = geom.structure.Position(self.name+'63ModuleFT2_pos', modft63pos2[0], modft63pos2[1], modft63pos2[2])

        modft100_pla = geom.structure.Placement(self.name+modft100_lv.name+'_pla', volume=modft100_lv, pos=relpos100)
        modft160_1_pla = geom.structure.Placement(self.name+modft63_lv.name+'1_pla', volume=modft63_lv, pos=relpos63_1)
        modft160_2_pla = geom.structure.Placement(self.name+modft63_lv.name+'2_pla', volume=modft63_lv, pos=relpos63_2)

        main_lv.placements.append(modft100_pla.name) 
        main_lv.placements.append(modft160_1_pla.name)
        main_lv.placements.append(modft160_2_pla.name)    

