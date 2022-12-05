import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class StrawTubeBuilder(gegede.builder.Builder):

    def configure(self, base_name, straw_half_length, gas,**kwds):
        self.StrawRadius            = Q('4mm')
        self.DistStrawStraw         = Q('1mm') # --> 2 mm to account for flange bearing
        self.DistStrawWall          = Q('1mm') 
        self.AngleStrawStraw        = Q('60deg')
        self.StrawRing              = Q('0.5mm')
        self.StrawWireWThickness    = Q('20um')
        self.StrawWireGThickness    = Q('20nm')
        self.CoatThickness          = Q("70nm")
        self.MylarThickness         = Q("12um")
        self.StrawGas               = {"CMod" : "stGas_Ar19", "C3H6Mod":"stGas_Xe19", "TrkMod":"stGas_Ar19"}  
        self.gas                    = gas
        self.base_name              = base_name
        self.straw_half_length      = straw_half_length

    def construct(self, geom):
        # straw 
        base_name = self.base_name
        straw_half_length = self.straw_half_length
        gas= self.gas
        straw_name          = base_name+"_straw"
        straw_shape         = geom.shapes.Tubs(straw_name+"_shape", rmin=Q("0m"), rmax=self.StrawRadius + self.StrawRing, dz=straw_half_length)
        straw_lv            = geom.structure.Volume(straw_name, material="Air35C", shape = straw_shape)

        self.add_volume(straw_lv)

        # straw ring
        ring_name           = straw_name+"_ring"
        ring_shape          = geom.shapes.Tubs(ring_name+"_shape", rmin = self.StrawRadius, rmax = self.StrawRadius + self.StrawRing, dz=straw_half_length)
        ring_lv             = geom.structure.Volume(ring_name, material="Air35C", shape = ring_shape)
        ring_pla            = geom.structure.Placement(ring_name+"_place", volume = ring_lv)

        # coat
        Alcoat_name         = straw_name+"_Alcoat"
        Alcoat_shape        = geom.shapes.Tubs(Alcoat_name+"_shape", rmin = self.StrawRadius - self.CoatThickness, rmax=self.StrawRadius, dz=straw_half_length)
        Alcoat_lv           = geom.structure.Volume(Alcoat_name, material="Aluminum", shape = Alcoat_shape)
        Alcoat_pla          = geom.structure.Placement(Alcoat_name+"_place", volume = Alcoat_lv)

        # mylar
        mylar_name          = straw_name+"_mylar"
        mylar_shape         = geom.shapes.Tubs(mylar_name+"_shape", rmin = self.StrawRadius - self.CoatThickness - self.MylarThickness, rmax = self.StrawRadius - self.CoatThickness, dz=straw_half_length)
        mylar_lv            = geom.structure.Volume(mylar_name, material="Mylar", shape = mylar_shape)
        mylar_pla           = geom.structure.Placement(mylar_name+"_place", volume = mylar_lv)

        # gas
        gas_name            = straw_name+"_"+gas
        gas_shape           = geom.shapes.Tubs(gas_name+"_shape", rmin = self.StrawWireWThickness + self.StrawWireGThickness, rmax = self.StrawRadius - self.CoatThickness - self.MylarThickness, dz=straw_half_length)
        gas_lv              = geom.structure.Volume(gas_name, material=gas, shape = gas_shape)
        gas_pla             = geom.structure.Placement(gas_name+"_place", volume = gas_lv)
        gas_lv.params.append(("SensDet","Straw"))

        # wire coating
        wireCoat_name       = straw_name+"_wireCoating"
        wireCoat_shape      = geom.shapes.Tubs(wireCoat_name+"_shape", rmin = self.StrawWireWThickness, rmax = self.StrawWireWThickness + self.StrawWireGThickness, dz=straw_half_length)
        wireCoat_lv         = geom.structure.Volume(wireCoat_name, material="Tungsten", shape=wireCoat_shape)
        wireCoat_pla        = geom.structure.Placement(wireCoat_name+"_place", volume = wireCoat_lv)

        # wire
        wire_name           = straw_name+"_wire"
        wire_shape          = geom.shapes.Tubs(wire_name+"_shape", rmin = Q("0mm"), rmax = self.StrawWireWThickness, dz=straw_half_length)
        wire_lv             = geom.structure.Volume(wire_name, material="Gold",shape=wire_shape)
        wire_pla            = geom.structure.Placement(wire_name+"_place", volume = wire_lv)

        straw_lv.placements.append(ring_pla.name)
        straw_lv.placements.append(Alcoat_pla.name)
        straw_lv.placements.append(mylar_pla.name)
        straw_lv.placements.append(gas_pla.name)
        straw_lv.placements.append(wireCoat_pla.name)
        straw_lv.placements.append(wire_pla.name)      