#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class InletBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, rmax1=None, rmax2=None, rmin1=None, rmin2=None, 
                    dz1=None, dz2=None, Material=None, shift=None, **kwds ):
        self.rmin1, self.rmax1, self.dz1 = (rmin1, rmax1, dz1)
        self.rmin2, self.rmax2, self.dz2 = (rmin2, rmax2, dz2)
        self.Material = Material
        self.shift = shift

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        neck_shape = geom.shapes.Tubs( self.name+'Component2', rmin=self.rmin2, rmax=self.rmax2, dz=self.dz2 )
        foot_shape = geom.shapes.Tubs( self.name+'Component1', rmin=self.rmin1, rmax=self.rmax1, dz=self.dz1 )
        
        relpos1 = geom.structure.Position(self.name+'Component1Rel_pos', Q('0m'), Q('0m'), neck_shape.dz+foot_shape.dz)
        relpos2 = geom.structure.Position(self.name+'Component2Rel_pos', Q('0m'), Q('0m'), neck_shape.dz-self.shift-foot_shape.dz)

        # union
        boolean_shape1 = geom.shapes.Boolean( self.name+'Union1', type='union', first=neck_shape, second=foot_shape, pos=relpos1)
        boolean_shape2 = geom.shapes.Boolean( self.name, type='union', first=boolean_shape1, second=foot_shape, pos=relpos2)
        boolean_lv = geom.structure.Volume('vol'+boolean_shape2.name, material=self.Material, shape=boolean_shape2)
        self.add_volume( boolean_lv )   




       
