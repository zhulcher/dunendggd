#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
import math
from gegede import Quantity as Q

class DriftChamberModuleBuilder(gegede.builder.Builder):
    
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, moduleDx=None, moduleHeight=None,
                        targetThickness=None, targetMaterial=None,
                        DriftModuleThickness=None, DriftChamberGas=None, NofDriftModules=None,MylarThickness=None,
                        FieldWireRadius=None, SignalWireRadius=None, WireMaterial=None, WireAngle=None, WireWireDistance=None,
                        **kwds):
        
        self.moduleDx               = moduleDx
        self.moduleHeight           = moduleHeight

        self.targetThickness        = targetThickness
        self.targetMaterial         = targetMaterial
        
        self.DriftModuleThickness   = DriftModuleThickness
        self.DriftChamberGas        = DriftChamberGas
        self.NofDriftModules        = NofDriftModules
        self.MylarThickness         = MylarThickness
        self.DriftChamberThickness  = self.DriftModuleThickness * self.NofDriftModules + self.MylarThickness*(self.NofDriftModules + 1)
        self.moduleThickness        = targetThickness + self.DriftChamberThickness

        self.FieldWireRadius        = FieldWireRadius
        self.SignalWireRadius       = SignalWireRadius
        self.WireMaterial           = WireMaterial
        self.WireAngle              = WireAngle
        self.WireWireDistance       = WireWireDistance

    def construct(self, geom):
        print("DriftChamberModuleBuilder::construct()")
        materials.define_materials(geom)

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

        target_name         = base_name + "target"
        target_shape        = geom.shapes.Box(target_name+"_shape",dx=self.targetThickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        target_lv           = geom.structure.Volume(target_name, material=self.targetMaterial, shape=target_shape)

        return target_lv

    def constructDriftChamber(self,geom, base_name):

        driftChamber_name   = base_name + "drift_chamber"
        driftChamber_shape  = geom.shapes.Box(driftChamber_name+"_shape",dx=self.DriftChamberThickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        driftChamber_lv     = geom.structure.Volume(driftChamber_name, material=self.DriftChamberGas, shape=driftChamber_shape)

        # construct mylar planes
        MylarPlane_lv       = self.constructMylarPlane(geom, driftChamber_name)
        # construct module with no wire inclination
        DriftModuleX_lv     = self.constructDriftModule(geom, driftChamber_name)
        # construct module with inclination
        DriftModuleXY_lv    = self.constructDriftModule(geom, driftChamber_name, self.WireAngle)

        running_x           = -self.DriftChamberThickness/2
        running_drift_vol   = DriftModuleX_lv
        running_rotationY   = Q("0deg")

        for i in range(self.NofDriftModules):
            # place mylar plane
            running_x           += self.MylarThickness/2

            Mylar_name           = MylarPlane_lv.name+"_"+str(i)
            MylarPlane_position  = geom.structure.Position(Mylar_name+"_pos", running_x, Q("0mm"), Q("0mm"))
            MylarPlane_place     = geom.structure.Placement(Mylar_name+"_place", volume = MylarPlane_lv, pos = MylarPlane_position)
 
            # place driftModule 
            running_x           += self.MylarThickness/2 + self.DriftModuleThickness/2

            DriftModule_name     = running_drift_vol.name+"_"+str(i)
            DriftModule_position = geom.structure.Position(DriftModule_name+"_pos", running_x, Q("0mm"), Q("0mm"))
            DriftModule_rotation = geom.structure.Rotation(DriftModule_name+"_rot", Q("0deg"), running_rotationY, Q("0deg"))
            DriftModule_place    = geom.structure.Placement(DriftModule_name+"_place", volume = running_drift_vol, pos = DriftModule_position, rot = DriftModule_rotation)

            running_x           += self.DriftModuleThickness/2
            running_drift_vol    = DriftModuleXY_lv
            running_rotationY   +=Q("180deg")

            driftChamber_lv.placements.append(MylarPlane_place.name)
            driftChamber_lv.placements.append(DriftModule_place.name)

        #place last mylar plane
        running_x           += self.MylarThickness/2
        Mylar_name           = MylarPlane_lv.name+"_"+str(self.NofDriftModules+1)
        MylarPlane_position  = geom.structure.Position(Mylar_name+"_pos", running_x, Q("0mm"), Q("0mm"))
        MylarPlane_place     = geom.structure.Placement(Mylar_name+"_place", volume = MylarPlane_lv, pos = MylarPlane_position)

        driftChamber_lv.placements.append(MylarPlane_place.name)

        return driftChamber_lv
    
    def constructDriftModule(self, geom, base_name, wire_angle=Q("0deg")):
        orientation=""
        if wire_angle == 0:
            orientation = "X"
        else:
            orientation = "XY"

        chamber_name    = base_name+"_module"+orientation
        thickness       = self.DriftModuleThickness
        chamber_shape   = geom.shapes.Box(chamber_name+"_shape",dx=thickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        chamber_lv      = geom.structure.Volume(chamber_name, material=self.DriftChamberGas, shape=chamber_shape)

        AvailableSpaceY = self.moduleHeight - self.moduleDx * math.sin(self.WireAngle)

        nof_wires       = int(AvailableSpaceY/(self.WireWireDistance + max(self.FieldWireRadius, self.SignalWireRadius)*2))

        LeftSpaceY      = AvailableSpaceY - (self.WireWireDistance + max(self.FieldWireRadius, self.SignalWireRadius)*2) * nof_wires

        running_y       = (self.moduleHeight - LeftSpaceY)/2 - self.moduleDx/2*math.sin(self.WireAngle) - self.FieldWireRadius # where to start building

        SignalWire_lv   = self.constructWire(geom, chamber_name, wire_angle, "S")
        FieldWire_lv    = self.constructWire(geom, chamber_name, wire_angle, "F")


        for i in range(nof_wires):

            volume     = SignalWire_lv if i%2 else FieldWire_lv 
            wire_name  = volume.name+"_"+str(i).zfill(3)
            wire_pos   = geom.structure.Position(wire_name+"_pos", Q("0m"), running_y, Q('0m'))
            wire_rot   = geom.structure.Rotation(wire_name+"_rot", wire_angle, Q("0deg"), Q("0deg"))
            wire_place = geom.structure.Placement(wire_name+"_place", volume = volume.name, pos = wire_pos.name, rot = wire_rot)

            running_y -= (self.WireWireDistance + self.FieldWireRadius + self.SignalWireRadius)
            
            chamber_lv.placements.append(wire_place.name)
        
        print("chamber : "+chamber_lv.name+" , nof_wires build "+str(nof_wires))

        return chamber_lv
    
    def constructMylarPlane(self, geom, base_name):

        mylar_name    = base_name+"_mylar"
        mylar_shape   = geom.shapes.Box(mylar_name+"_shape",dx=self.MylarThickness/2,dy=self.moduleHeight/2,dz=self.moduleDx/2)
        mylar_lv      = geom.structure.Volume(mylar_name, material="Mylar", shape=mylar_shape)
        
        return mylar_lv
    
    def constructWire(self, geom, base_name, wire_angle, wire_type):

        wire_name           = base_name+"_"+wire_type+"wire"
        r                   = self.SignalWireRadius if wire_type=="S" else self.FieldWireRadius
        wire_shape          = geom.shapes.Tubs(wire_name+"_shape", rmin = Q("0mm"), rmax = r, dz=self.moduleDx/2)
        wire_lv             = geom.structure.Volume(wire_name, material = self.WireMaterial, shape = wire_shape)

        return wire_lv