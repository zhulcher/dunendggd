#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class ModulePlateBuilder(gegede.builder.Builder):

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

        # subtract out feedthroughs
        boolean_shapes = [main_shape]
        boolean_lv = []
        assert(len(self.positions) == len(self.subtractions))
        for i, (sub, pos) in enumerate(zip(self.subtractions, self.positions)):
            # feedthrough shape
            ftsub_shape = geom.shapes.Tubs( self.name+'FTSubtractionTub'+str(i), rmin=Q('0m'), rmax=sub, dz=Q('1m') )
            relpos = geom.structure.Position(self.name+'FTSubtractionTub'+str(i)+'_pos', pos[0], pos[1], Q('0m'))
            # subtract
            boolean_shape = geom.shapes.Boolean( self.name+'FTSubtraction'+str(i), type='subtraction', first=boolean_shapes[i], second=ftsub_shape, pos=relpos)
            boolean_shapes.append(boolean_shape)
            boolean_lv = geom.structure.Volume('vol'+boolean_shape.name, material=self.Material, shape=boolean_shape)
        
        self.add_volume( boolean_lv )    

