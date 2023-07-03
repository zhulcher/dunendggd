#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import numpy as np

class BodyBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, Material=None, tubrmin=None, tubrmax=None, tubdz=None,
                    startphi=None, deltaphi=None, Rotation=None, SubBPos=None,
                    dishradius=None, knuckleradius=None, headradius=None, **kwds ):
        self.Material = Material 
        self.tubrmin, self.tubrmax, self.tubdz = ( tubrmin, tubrmax, tubdz )
        self.startphi, self.deltaphi = ( startphi, deltaphi )
        self.Rotation = Rotation
        self.SubBPos = SubBPos
        self.dishradius, self.knuckleradius, self.headradius = (dishradius, knuckleradius, headradius)

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # construct the tub and end cap

        # This constructs the cylindrical portion of the body.
        tube_shape = geom.shapes.Tubs( self.name+'CylindricalTube', rmin=self.tubrmin, rmax=self.tubrmax, dz=self.tubdz )

        # For the end cap, we create a Torispherical head
        # I use the parameters as defined in: https://mathworld.wolfram.com/TorisphericalDome.html
        R = self.dishradius
        a = self.knuckleradius
        c = self.headradius - a
        h = R - np.sqrt( (a + c - R)*(a - c - R) )

        # Make the sphere that will be the dish portion of the head.
        sphere_shape = geom.shapes.Sphere( self.name+'Sphere', rmin=self.tubrmin, rmax=R)

        # The head transitions from the sphere to the torus at the critical radius.
        # We cut out the portion of the sphere that lies outside of the critical radius.
        criticalradius = c * ( 1 + (R/a - 1)**-1 )

        tub_shape = geom.shapes.Tubs(self.name+'Tubs1', rmin = Q('0.m'), rmax = criticalradius, dz = h/2)

        relpos1 = geom.structure.Position(self.name + "Sphere_pos", Q('0m'), Q('0m'), R-h+h/2)

        sphere_cap = geom.shapes.Boolean(self.name + "_SphericalCap", type='intersection', first = tub_shape,
                                         second=sphere_shape, pos = relpos1)

        # Make the toroidal part of the head.
        torus_shape = geom.shapes.Torus(self.name+'Torus', rmin = Q('0m'), rmax = a, rtor = c)

        relpos2 = geom.structure.Position(self.name + "Torus_pos", Q('0m'), Q('0m'), h/2)

        head_shape = geom.shapes.Boolean(self.name + "SphericalCapTorus", type='union', first = sphere_cap,
                                        second = torus_shape, pos = relpos2)

        # Cut out the upper half of the torus.
        tub2_shape = geom.shapes.Tubs(self.name +'Tubs2', rmin = Q('0m'), rmax = self.headradius, dz = h/2)

        final_head_shape = geom.shapes.Boolean(self.name + "Head", type ='intersection', first = tub2_shape,
                                               second = head_shape)

        #Place the head directly under the cylinder.
        headpos = geom.structure.Position(self.name + "head_pos", Q('0m'), Q('0m'), -self.tubdz-h/2)

        boolean_shape = geom.shapes.Boolean(self.name + "_CylindricalTubeHead", type='union', first=tube_shape,
                                            second=final_head_shape, pos = headpos)

        boolean_lv = geom.structure.Volume('vol'+boolean_shape.name, material=self.Material,
                                            shape=boolean_shape)
        
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
