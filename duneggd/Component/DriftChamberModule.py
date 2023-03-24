#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q

class DriftChamberModuleBuilder(gegede.builder.Builder):
    
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, moduleDx=None, moduleHeight=None,
                        targetThickness=None, targetMaterial=None,
                        DriftChamberThickness=None, DriftChamberGas=None, NofDriftModules=None,
                        WireRadius=None, WireMaterial=None, WireAngle=None, WireWireDistance=None,
                        **kwds):
        
        self.moduleDx               = moduleDx
        self.moduleHeight           = moduleHeight
        self.moduleThickness        = targetThickness + DriftChamberThickness

        self.targetThickness        = targetThickness
        self.targetMaterial         = targetMaterial
        
        self.DriftChamberThickness  = DriftChamberThickness
        self.DriftChamberGas        = DriftChamberGas
        self.NofDriftModules        = NofDriftModules

        self.WireRadius             = WireRadius
        self.WireMaterial           = WireMaterial
        self.WireAngle              = WireAngle
        self.WireWireDistance       = WireWireDistance

    def construct(self, geom):
        print("DriftChamberModuleBuilder::construct()")

        main_lv = self.constructModule(geom)
        self.add_volume(main_lv)
    
    def constructModule(self,geom):

        module_name = "prototype_"
        main_shape  = geom.shapes.Box(module_name+"_shape", dx=(self.targetThickness+self.DriftChamberThickness)/2, dy=self.moduleHeight/2, dz=self.moduleDx/2)
        main_lv     = geom.structure.Volume(module_name, material="Air35C",shape=main_shape)

        target_lv               = self.constructTarget(geom, module_name)
        drift_chamber_lv        = self.constructDriftChamber(geom, module_name)
        
        target_position         = geom.structure.Position(target_lv.name+"_pos", -self.moduleThickness/2+self.targetThickness/2, Q("0m"), Q("0m"))
        drift_chamber_position  = geom.structure.Position(drift_chamber_lv.name+"_pos", -self.moduleThickness/2+self.targetThickness+self.DriftChamberThickness/2, Q("0m"), Q("0m"))

        target_place            = geom.structure.Placement(target_lv.name+"_place",volume=target_lv.name, pos=target_position.name)
        drift_chamber_place     = geom.structure.Placement(drift_chamber_lv.name+"_place",volume=drift_chamber_lv.name, pos=drift_chamber_position.name)  

        main_lv.placements.append(target_place.name)
        main_lv.placements.append(drift_chamber_place.name)

        return main_lv
    
    def constructTarget(self,geom, base_name):

        target_name = base_name + "target"
        target_shape = geom.shapes.Box(target_name+"_shape",dx=self.targetThickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        target_lv = geom.structure.Volume(target_name, material=self.targetMaterial, shape=target_shape)

        return target_lv

    def constructDriftChamber(self,geom, base_name):

        driftChamber_name   = base_name + "drift_chamber"
        driftChamber_shape  = geom.shapes.Box(driftChamber_name+"_shape",dx=self.DriftChamberThickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        driftChamber_lv     = geom.structure.Volume(driftChamber_name, material=self.DriftChamberGas, shape=driftChamber_shape)

        chamber0_lv = self.constructChamberModule(geom, driftChamber_name)
        chamber1_lv = self.constructChamberModule(geom, driftChamber_name, self.WireAngle)
        chamber2_lv = self.constructChamberModule(geom, driftChamber_name, -self.WireAngle)

        chamber_thickness = self.DriftChamberThickness/self.NofDriftModules

        chamber0_pos = geom.structure.Position(chamber0_lv.name+"_pos", -self.DriftChamberThickness/2+chamber_thickness*0.5, Q("0mm"), Q("0mm"))
        chamber1_pos = geom.structure.Position(chamber1_lv.name+"_pos", -self.DriftChamberThickness/2+chamber_thickness*1.5, Q("0mm"), Q("0mm"))
        chamber2_pos = geom.structure.Position(chamber2_lv.name+"_pos", -self.DriftChamberThickness/2+chamber_thickness*2.5, Q("0mm"), Q("0mm"))

        chamber0_pla = geom.structure.Placement(chamber0_lv.name+"_pla",volume=chamber0_lv.name,pos=chamber0_pos.name)
        chamber1_pla = geom.structure.Placement(chamber1_lv.name+"_pla",volume=chamber1_lv.name,pos=chamber1_pos.name)
        chamber2_pla = geom.structure.Placement(chamber2_lv.name+"_pla",volume=chamber2_lv.name,pos=chamber2_pos.name)

        driftChamber_lv.placements.append(chamber0_pla.name)
        driftChamber_lv.placements.append(chamber1_pla.name)
        driftChamber_lv.placements.append(chamber2_pla.name)

        return driftChamber_lv
    
    def constructChamberModule(self, geom, base_name, wire_angle=Q("0deg")):
        orientation=""
        if wire_angle < 0:
            orientation="dw"
        elif wire_angle > 0:
            orientation="up"
        else:
            orientation="h"

        chamber_name    = base_name+orientation
        thickness       = self.DriftChamberThickness/self.NofDriftModules
        chamber_shape   = geom.shapes.Box(chamber_name+"_shape",dx=thickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        chamber_lv      = geom.structure.Volume(chamber_name, material="Air35C",shape=chamber_shape)

        nof_wires = int(self.moduleHeight/self.WireWireDistance - 1)

        wire_lv = self.constructWire(geom, chamber_name, wire_angle)

        running_y = self.moduleHeight/2 
        
        for i in range(nof_wires):
            running_y -= self.WireWireDistance
            wire_name  = wire_lv.name+"_"+str(i).zfill(3)
            wire_pos   = geom.structure.Position(wire_name+"_pos", Q("0m"), running_y, Q('0m'))
            wire_rot   = geom.structure.Rotation(wire_name+"_rot",wire_angle,"0deg","0deg")
            wire_place = geom.structure.Placement(wire_name+"_place", volume = wire_lv.name, pos = wire_pos.name, rot=wire_rot.name)
            
            chamber_lv.placements.append(wire_place.name)

        return chamber_lv
    
    def constructWire(self,geom,base_name,wire_angle):

        wire_name           = base_name+"_wire"
        wire_shape          = geom.shapes.Tubs(wire_name+"_shape", rmin = Q("0mm"), rmax = self.WireRadius, dz=self.moduleDx/2)
        wire_lv             = geom.structure.Volume(wire_name, material=self.WireMaterial,shape=wire_shape)
        wire_pla            = geom.structure.Placement(wire_name+"_place", volume = wire_lv)
        
        return wire_lv