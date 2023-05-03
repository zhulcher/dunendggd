#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class BodyBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, material=None, tubrmin=None, tubrmax=None, tubdz=None,
                    caprmin=None, caprmax=None, caprtor=None,
                    startphi=None, deltaphi=None, Rotation=None, SubBPos=None, **kwds ):
        self.Material = material 
        self.tubrmin, self.tubrmax, self.tubdz = ( tubrmin, tubrmax, tubdz )
        self.caprmin, self.caprmax, self.caprtor = ( caprmin, caprmax, caprtor )
        self.startphi, self.deltaphi = ( startphi, deltaphi )
        self.Rotation = Rotation
        self.SubBPos = SubBPos

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the tub and end cap
        outertub_shape = geom.shapes.Tubs( self.name+'OuterTub', rmin=self.tubrmin, rmax=self.tubrmax, dz=self.tubdz )
        torus_shape = geom.shapes.Torus( self.name+'Torus', rmin=self.caprmin, rmax=self.caprmax, rtor=self.caprtor,
                                        startphi=self.startphi, deltaphi=self.deltaphi )
        innertub_shape = geom.shapes.Tubs( self.name+'InnerTub', rmin=Q('0m'), rmax=self.caprtor, dz=self.caprmax )

        shiftFor2 = Q(-1*outertub_shape.dz)
        relpos1 = geom.structure.Position(self.name+'Torus_pos', Q('0m'), Q('0m'), -1*outertub_shape.dz)
        relpos2 = geom.structure.Position(self.name+'InnerTub_pos', Q('0m'), Q('0m'), shiftFor2 )

        # make union of outer tub and torus 
        boolean_shape_1 = geom.shapes.Boolean( self.name+'_OuterTubTorus', type='union',
                                               first=outertub_shape, second=torus_shape, pos=relpos1)

        boolean_lv = geom.structure.Volume('vol'+boolean_shape_1.name, material=self.Material,
                                            shape=boolean_shape_1)

        # make union of boolean 1 and inner tub
        boolean_shape_2 = geom.shapes.Boolean( self.name+'_OuterTubTorusInnerTub', type='union',
                                              first=boolean_shape_1, second=innertub_shape, pos=relpos2)

        boolean_lv = geom.structure.Volume('vol'+boolean_shape_2.name, material=self.Material,
                                            shape=boolean_shape_2)
        
        self.add_volume( boolean_lv )      

        # place sub-builder
        if len(self.get_builders()) != 1: return

        sb = self.get_builder()
        sb_lv = sb.get_volume()

        sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                         self.SubBPos[0], self.SubBPos[1], self.SubBPos[2])
        sb_rot = []                                         
        if self.Rotation != None:                                         
            sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot', self.Rotation[0], self.Rotation[1], self.Rotation[2])
        else:            
            sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot',
                                             '0.0deg', '0.0deg', '0.0deg')  
                                             
        sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                            volume=sb_lv, pos=sb_pos, rot=sb_rot)
        boolean_lv.placements.append(sb_pla.name)                                           
