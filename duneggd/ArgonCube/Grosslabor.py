""" Grosslabor.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class GrosslaborBuilder(gegede.builder.Builder):
    """ Class to build Grosslabor geometry.

    """

    def configure(self,halfDimension,cryoDimension,roofDimension,pitDimension,Material,**kwargs):

        # Read dimensions form config file
        self.halfDimension      = halfDimension

        self.cryo_rmax          = cryoDimension['r_max']
        self.cryo_rmin          = cryoDimension['r_min']
        self.cryo_dy            = cryoDimension['dy']

        self.roof_dy            = roofDimension['dy']

        self.pit_dx             = pitDimension['dx']
        self.pit_dy             = pitDimension['dy']
        self.pit_dz             = pitDimension['dz']

        self.Material           = Material

        self.Tube_Material      = 'Steel'
        self.Pit_Material       = 'Air'
        self.Concrete_Material  = 'ReifConcrete'
        self.Roof_Material      = 'ReifConcrete'


        # Subbuilders
        self.Module_builder     = self.get_builder('Module')
        self.Bucket_builder     = self.get_builder('Module').get_builder('Bucket')
        self.Flange_builder     = self.get_builder('Module').get_builder('Flange')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.halfDimension['dx'],
                                'dy':   2*self.halfDimension['dy']+self.Module_builder.halfDimension['dy']+2*self.roof_dy,
                                'dz':   self.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('GrosslaborBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Roof Volume
        Roof_shape = geom.shapes.Box('Roof_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.roof_dy,
                                        dz = self.halfDimension['dz'])

        Roof_lv = geom.structure.Volume('volRoof',
                                        material=self.Roof_Material,
                                        shape=Roof_shape)

        # Place Roof Volume inside Grosslabor volume
        pos = [Q('0cm'),self.halfDimension['dy']-Roof_shape.dy,Q('0cm')]

        Roof_pos = geom.structure.Position('Roof_pos',
                                                pos[0],pos[1],pos[2])

        Roof_pla = geom.structure.Placement('Roof_pla',
                                                volume=Roof_lv,
                                                pos=Roof_pos)

        main_lv.placements.append(Roof_pla.name)

        # Construct Concrete Volume
        Concrete_shape = geom.shapes.Box('Concrete_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.halfDimension['dy']/2.+self.Module_builder.halfDimension['dy']/2.,
                                        dz = self.halfDimension['dz'])

        Concrete_lv = geom.structure.Volume('volConcrete',
                                        material=self.Concrete_Material,
                                        shape=Concrete_shape)

        # Place Concrete Volume inside Grosslabor volume
        pos = [Q('0cm'),-self.halfDimension['dy']+Concrete_shape.dy,Q('0cm')]

        Concrete_pos = geom.structure.Position('Concrete_pos',
                                                pos[0],pos[1],pos[2])

        Concrete_pla = geom.structure.Placement('Concrete_pla',
                                                volume=Concrete_lv,
                                                pos=Concrete_pos)

        main_lv.placements.append(Concrete_pla.name)

        # Construct Pit Volume
        Pit_shape = geom.shapes.Box('Pit_shape',
                                        dx = self.pit_dx,
                                        dy = self.pit_dy,
                                        dz = self.pit_dz)

        Pit_lv = geom.structure.Volume('volPit',
                                        material=self.Pit_Material,
                                        shape=Pit_shape)

        # Place Pit Volume inside Concrete volume
        pos = [Q('0cm'),Concrete_shape.dy-self.pit_dy,Q('0cm')]

        Pit_pos = geom.structure.Position('Pit_pos',
                                                pos[0],pos[1],pos[2])

        Pit_pla = geom.structure.Placement('Pit_pla',
                                                volume=Pit_lv,
                                                pos=Pit_pos)

        Concrete_lv.placements.append(Pit_pla.name)


        # Construct CryoTube Volume
        CryoTube_shape = geom.shapes.Tubs('CryoTube_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.cryo_rmax,
                                        dz = self.cryo_dy)

        CryoTube_lv = geom.structure.Volume('volCryoTube',
                                        material=self.Tube_Material,
                                        shape=CryoTube_shape)

        # Place CryoTube Volume inside Pit volume
        pos = [Q('0cm'),Pit_shape.dy-self.cryo_dy-2*self.Module_builder.get_builder('Flange').halfDimension['dy'],Q('0cm')]

        rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

        CryoTube_rot = geom.structure.Rotation('CryoTube_rot',
                                                rot[0],rot[1],rot[2])

        CryoTube_pos = geom.structure.Position('CryoTube_pos_A',
                                                pos[0],pos[1],pos[2])

        CryoTube_pla = geom.structure.Placement('CryoTube_pla_A',
                                                volume=CryoTube_lv,
                                                pos=CryoTube_pos,
                                                rot=CryoTube_rot)

        Pit_lv.placements.append(CryoTube_pla.name)


        # Construct LArFill Volume
        LArFill_shape = geom.shapes.Tubs('LArFill_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.cryo_rmin,
                                        dz = self.cryo_dy)

        LArFill_lv = geom.structure.Volume('volLArFill',
                                        material='LAr',
                                        shape=LArFill_shape)

        # Place LArFill Volume inside Cryotube volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        rot = [Q('0.0deg'),Q('0.0deg'),Q('0.0deg')]

        LArFill_rot = geom.structure.Rotation('LArFill_rot',
                                                rot[0],rot[1],rot[2])

        LArFill_pos = geom.structure.Position('LArFill_pos_A',
                                                pos[0],pos[1],pos[2])

        LArFill_pla = geom.structure.Placement('LArFill_pla_A',
                                                volume=LArFill_lv,
                                                pos=LArFill_pos,
                                                rot=LArFill_rot)

        CryoTube_lv.placements.append(LArFill_pla.name)


        # Build Bucket
        pos = [Q('0cm'),Q('0cm'),CryoTube_shape.dz-self.Bucket_builder.halfDimension['dy']]

        rot = [Q('-90.0deg'),Q('0.0deg'),Q('0.0deg')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_ppos',
                                            pos[0],pos[1],pos[2])

        Bucket_rot = geom.structure.Rotation('Bucket_rot',
                                                rot[0],rot[1],rot[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_ppla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos,
                                                rot=Bucket_rot)

        LArFill_lv.placements.append(Bucket_pla.name)

        # Build Flange
        pos = [Q('0cm'),Pit_shape.dy-self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Flange_lv = self.Flange_builder.get_volume()

        Flange_pos = geom.structure.Position(self.Flange_builder.name+'_ppos',
                                            pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement(self.Flange_builder.name+'_ppla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        Pit_lv.placements.append(Flange_pla.name)

