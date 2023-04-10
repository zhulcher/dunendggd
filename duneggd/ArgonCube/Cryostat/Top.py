#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import numpy as np

class TopBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmax=None, rmin=None, material=None, 
                    shifts=None, positions=None, **kwds ):
        self.rmin, self.rmax, self.dz = (rmin, rmax, dz)
        self.Material = material
        self.shifts = shifts
        self.positions = positions

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_shape = geom.shapes.Tubs( self.name, rmin=self.rmin, rmax=self.rmax, dz=self.dz )
        main_lv = geom.structure.Volume('vol'+main_shape.name, material=self.Material, shape=main_shape)
        self.add_volume( main_lv )   

        # get the builders
        sbs = self.get_builders()
        longcon_lv  = sbs[0].get_volume()
        innercon_lv = sbs[1].get_volume()
        ft100_lv    = sbs[2].get_volume()
        ft160_lv    = sbs[3].get_volume()
        modcont_lv  = sbs[4].get_volume()

        # place long connectors
        midZ = -1*main_shape.dz + self.shifts[2]
        longR = self.shifts[0]
        rot1 = geom.structure.Rotation(self.name+longcon_lv.name+ '_rot', '0.0deg', '0.0deg', '0.0deg')  

        sb_pos1 = geom.structure.Position(self.name+longcon_lv.name+ '_pos1', -1*longR, Q('0m'), midZ)                               
        sb_pla1 = geom.structure.Placement(self.name+longcon_lv.name+'_pla1', volume=longcon_lv, pos=sb_pos1, rot=rot1)
        main_lv.placements.append(sb_pla1.name)

        sb_pos2 = geom.structure.Position(self.name+longcon_lv.name+ '_pos2', Q('0m'), Q('0m'), midZ)                                 
        sb_pla2 = geom.structure.Placement(self.name+longcon_lv.name+'_pla2', volume=longcon_lv, pos=sb_pos2, rot=rot1)
        main_lv.placements.append(sb_pla2.name)

        sb_pos3 = geom.structure.Position(self.name+longcon_lv.name+ '_pos3', longR, Q('0m'), midZ)                           
        sb_pla3 = geom.structure.Placement(self.name+longcon_lv.name+'_pla3', volume=longcon_lv, pos=sb_pos3, rot=rot1)
        main_lv.placements.append(sb_pla3.name)

        # place inner connectors
        innerR = self.shifts[1]
        steps = [-1*longR, Q('0m'), longR]
        rot2 = geom.structure.Rotation(self.name+innercon_lv.name+ '_rot1', '0.0deg', '0.0deg', '0.0deg')  
        rot3 = geom.structure.Rotation(self.name+innercon_lv.name+ '_rot2', '0.0deg', '0.0deg', '90.0deg')  

        i = 0
        for step in steps:
            i = i + 1
            sb_pos = geom.structure.Position(self.name+innercon_lv.name+ '_pos'+str(i), -1*innerR, step, midZ)
            sb_pla = geom.structure.Placement(self.name+innercon_lv.name+'_pla'+str(i), volume=innercon_lv, pos=sb_pos, rot=rot1)
            main_lv.placements.append(sb_pla.name)
        for step in steps:
            i = i + 1
            sb_pos = geom.structure.Position(self.name+innercon_lv.name+ '_pos'+str(i), innerR, step, midZ)
            sb_pla = geom.structure.Placement(self.name+innercon_lv.name+'_pla'+str(i), volume=innercon_lv, pos=sb_pos, rot=rot1)
            main_lv.placements.append(sb_pla.name) 

        # place feedthroughs
        for i in range(0,4):
            # rotate
            theta = (np.pi/2.)*i
            pos1 = [self.positions[0][0]*np.cos(theta) + self.positions[0][1]*np.sin(theta), -1*self.positions[0][0]*np.sin(theta) + self.positions[0][1]*np.cos(theta) ]
            pos2 = [self.positions[1][0]*np.cos(theta) + self.positions[1][1]*np.sin(theta), -1*self.positions[1][0]*np.sin(theta) + self.positions[1][1]*np.cos(theta) ]

            trelpos1 = geom.structure.Position(self.name+'100FT'+str(i)+'_pos', pos1[0], pos1[1], self.positions[0][2])
            trelpos2 = geom.structure.Position(self.name+'160FT'+str(i)+'_pos', pos2[0], pos2[1], self.positions[1][2])  

            ft100_pla = geom.structure.Placement(self.name+ft100_lv.name+'_pla'+str(i), volume=ft100_lv, pos=trelpos1)
            ft160_pla = geom.structure.Placement(self.name+ft160_lv.name+'_pla'+str(i), volume=ft160_lv, pos=trelpos2)
            main_lv.placements.append(ft100_pla.name) 
            main_lv.placements.append(ft160_pla.name)         

        # place the module top containers
        modcontpos = self.positions[2]

        relpos1 = geom.structure.Position(self.name+'ModuleTopContainer1_pos', modcontpos[0], modcontpos[1], modcontpos[2])  
        modcont1_pla = geom.structure.Placement(self.name+modcont_lv.name+'1_pla', volume=modcont_lv, pos=relpos1)
        main_lv.placements.append(modcont1_pla.name)  

        relpos2 = geom.structure.Position(self.name+'ModuleTopContainer2_pos', -1*modcontpos[0], modcontpos[1], modcontpos[2])  
        modcont2_pla = geom.structure.Placement(self.name+modcont_lv.name+'2_pla', volume=modcont_lv, pos=relpos2)
        main_lv.placements.append(modcont2_pla.name)  

        relpos3 = geom.structure.Position(self.name+'ModuleTopContainer3_pos', -1*modcontpos[0], -1*modcontpos[1], modcontpos[2])  
        modcont3_pla = geom.structure.Placement(self.name+modcont_lv.name+'3_pla', volume=modcont_lv, pos=relpos3)
        main_lv.placements.append(modcont3_pla.name)  

        relpos4 = geom.structure.Position(self.name+'ModuleTopContainer4_pos', modcontpos[0], -1*modcontpos[1], modcontpos[2])  
        modcont4_pla = geom.structure.Placement(self.name+modcont_lv.name+'4_pla', volume=modcont_lv, pos=relpos4)
        main_lv.placements.append(modcont4_pla.name)  

       
