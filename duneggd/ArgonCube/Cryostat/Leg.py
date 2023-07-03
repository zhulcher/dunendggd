#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class LegBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, rmax1=None, rmax2=None, rmin=None, dz1=None, dz2=None, 
                    Material=None, **kwds ):
        self.rmin, self.rmax1, self.rmax2 = (rmin, rmax1, rmax2)
        self.dz1, self.dz2 = (dz1, dz2)
        self.Material = Material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the plate, subtract out insertion plate
        leg_shape = geom.shapes.Tubs( self.name+'Component1', rmin=self.rmin, rmax=self.rmax1, dz=self.dz1 )
        foot_shape = geom.shapes.Tubs( self.name+'Component2', rmin=self.rmin, rmax=self.rmax2, dz=self.dz2 )
        
        relpos = geom.structure.Position(self.name+'Component2Rel_pos', Q('0m'), Q('0m'), -1*leg_shape.dz-foot_shape.dz)

        # union
        boolean_shape = geom.shapes.Boolean( self.name, type='union', first=leg_shape, second=foot_shape, pos=relpos)
        boolean_lv = geom.structure.Volume('vol'+boolean_shape.name, material=self.Material, shape=boolean_shape)
        self.add_volume( boolean_lv )   




       
