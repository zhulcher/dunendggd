#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class FeedthroughBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz1=None, rmax1=None, rmin1=None,
                         dz2=None, rmax2=None, rmin2=None,
                         Material=None, **kwds ):
        self.rmin1, self.rmax1, self.dz1 = (rmin1, rmax1, dz1)
        self.rmin2, self.rmax2, self.dz2 = (rmin2, rmax2, dz2)
        self.Material = Material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # container
        head_shape = geom.shapes.Tubs( self.name+'Head', rmin=self.rmin1, rmax=self.rmax1, dz=self.dz1 )
        neck_shape = geom.shapes.Tubs( self.name+'Neck', rmin=self.rmin2, rmax=self.rmax2, dz=self.dz2 )

        relpos = geom.structure.Position(self.name+'FTRel_pos', Q('0m'), Q('0m'), neck_shape.dz+head_shape.dz)

        # union
        boolean_shape = geom.shapes.Boolean( self.name, type='union', first=neck_shape, second=head_shape, pos=relpos)
        boolean_lv = geom.structure.Volume('vol'+boolean_shape.name, material=self.Material, shape=boolean_shape)
        self.add_volume( boolean_lv ) 

