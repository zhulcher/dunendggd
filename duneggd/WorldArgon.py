#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


#Changed DetEnc to Rock
class WorldBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, **kwds):
        self.halfDimension = halfDimension
        self.Material = Material
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ########################### Above is math, below is GGD ###########################

        materials.define_materials(geom)


        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume(main_lv)
        main_lv.params.append(("SensDet","ActiveArgonSea_shape"))
        main_lv.params.append(("EField","(500.0 V/cm, 0.0 V/cm, 0.0 V/cm)"))




