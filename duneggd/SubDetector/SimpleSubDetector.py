#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class SimpleSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, dx=None, dy=None, dz=None, rmax=None, rmin=None,
                  material=None, NElements=None, BeginGap=None,
                  InsideGap=None, Rotation=None, auxParams=None,
                  TranspV=None, SubBPos=None, shape=None, **kwds):
        if halfDimension == None and shape == "Tubs":
            halfDimension = {}
            halfDimension['rmin'] = rmin
            halfDimension['rmax'] = rmax
            halfDimension['dz'] = dz
        else:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.Material = (halfDimension, material)
        self.NElements, self.BeginGap = (NElements, BeginGap)
        self.InsideGap, self.Rotation = (InsideGap, Rotation)
        self.TranspV, self.SubBPos = (TranspV, SubBPos)
        self.auxParams = auxParams
        self.shape = shape

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv = None
        main_hDim = None

        if self.shape == "Tubs":
            main_lv, main_hDim = ltools.main_lv(self, geom, "Tubs")
        else:
            self.shape = "Box"
            main_lv, main_hDim = ltools.main_lv(self, geom, "Box")

        if self.auxParams != None:
            ltools.addAuxParams(self, main_lv)

        self.add_volume(main_lv)

        if self.NElements != None:
            TranspV = [0, 0, 1]
            if self.TranspV != None:
                TranspV = self.TranspV
            ltools.placeBuilders(self, geom, main_lv, TranspV)
        else:
            print("**Warning, no Elements to place inside " + self.name)
