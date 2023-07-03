#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import numpy as np

# The feedthrough positions seem to be correct,
# however visualization is not showing all the holes

class FlangeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz1=None, dz2=None, rmax=None, rmin1=None, rmin2=None,
                    Material=None, positions=None, centersubt=None, ftsubtr=None, **kwds ):
        self.rmin1, self.rmin2, self.rmax, self.dz1, self.dz2 = (rmin1, rmin2, rmax, dz1, dz2)
        self.Material = Material
        self.centersubt = centersubt
        self.positions = positions
        self.ftsubtr = ftsubtr

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the plate, subtract out insertion plate
        fl1_shape = geom.shapes.Tubs( self.name+'FlangeComponent1', rmin=self.rmin1, rmax=self.rmax, dz=self.dz1 )
        fl2_shape = geom.shapes.Tubs( self.name+'FlangeComponent2', rmin=self.rmin2, rmax=self.rmax, dz=self.dz2 )
        flsub_shape = geom.shapes.Box( self.name+'FlangeComponent3', dx=self.centersubt[0], dy=self.centersubt[1], dz=self.centersubt[2])
        
        relpos1 = geom.structure.Position(self.name+'FlangeSubtractionRel_pos', Q('0m'), Q('0m'), Q('0m'))
        relpos2 = geom.structure.Position(self.name+'FlangeComponent2Rel_pos', Q('0m'), Q('0m'), -1*fl1_shape.dz-fl2_shape.dz)

        # subtract insertion plate
        boolean_shape1 = geom.shapes.Boolean( self.name+'FlangeSubtraction', type='subtraction', first=fl1_shape, second=flsub_shape, pos=relpos1)

        # subtract out feedthroughs
        ft1_shape = geom.shapes.Tubs( self.name+'FTComponent1', rmin=Q('0m'), rmax=self.ftsubtr[0], dz=2*self.centersubt[2] )
        ft2_shape = geom.shapes.Tubs( self.name+'FTComponent2', rmin=Q('0m'), rmax=self.ftsubtr[1], dz=2*self.centersubt[2] )
        theBoolean = boolean_shape1
        for i in range(0,4):
            # rotate
            theta = (np.pi/2.)*i
            pos1 = [self.positions[0][0]*np.cos(theta) + self.positions[0][1]*np.sin(theta), -1*self.positions[0][0]*np.sin(theta) + self.positions[0][1]*np.cos(theta) ]
            pos2 = [self.positions[1][0]*np.cos(theta) + self.positions[1][1]*np.sin(theta), -1*self.positions[1][0]*np.sin(theta) + self.positions[1][1]*np.cos(theta) ]

            trelpos1 = geom.structure.Position(self.name+'FTSubtraction1Rel'+str(i)+'_pos', pos1[0], pos1[1], Q('0m'))
            trelpos2 = geom.structure.Position(self.name+'FTSubtraction2Rel'+str(i)+'_pos', pos2[0], pos2[1], Q('0m'))

            # subtract
            tboolean_shape = geom.shapes.Boolean( self.name+'FTSubtraction1'+str(i), type='subtraction', first=theBoolean, second=ft1_shape, pos=trelpos1)
            theBoolean = tboolean_shape
            boolean_shape = geom.shapes.Boolean( self.name+'FTSubtraction2'+str(i), type='subtraction', first=theBoolean, second=ft2_shape, pos=trelpos2)
            theBoolean = boolean_shape

        # make union of the two components
        boolean_shape2 = geom.shapes.Boolean( self.name, type='union', first=theBoolean, second=fl2_shape, pos=relpos2)
        boolean_lv = geom.structure.Volume('vol'+boolean_shape2.name, material=self.Material, shape=boolean_shape2)
        self.add_volume( boolean_lv )      
