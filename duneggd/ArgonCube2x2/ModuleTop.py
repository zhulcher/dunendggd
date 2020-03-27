""" ModuleTop.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleTopBuilder(gegede.builder.Builder):
    """ Class to build ModuleTop geometry.

    """

    def configure(self,ModuleTop_dimension,Flange_dimension,PillowTop_dimension,PillowSide_dimension,PillowBottom_dy,AngleBarTop_dimension,Angle_length,Angle_dd,N_Angle,**kwargs):

        # Read dimensions form config file
        self.ModuleTop_dx       = ModuleTop_dimension['dx']
        self.ModuleTop_dy       = ModuleTop_dimension['dy']
        self.ModuleTop_dz       = ModuleTop_dimension['dz']

        self.Flange_dx          = Flange_dimension['dx']
        self.Flange_dy          = Flange_dimension['dy']
        self.Flange_dz          = Flange_dimension['dz']

        self.PillowTop_dx       = PillowTop_dimension['dx']
        self.PillowTop_dy       = PillowTop_dimension['dy']
        self.PillowTop_dz       = PillowTop_dimension['dz']

        self.PillowSide_dx      = PillowSide_dimension['dx']
        self.PillowSide_dy      = PillowSide_dimension['dy']
        self.PillowSide_dz      = PillowSide_dimension['dz']
        self.PillowSide_dd      = PillowSide_dimension['dd']

        self.PillowBottom_dy    = PillowBottom_dy

        self.AngleBarTop_dx     = AngleBarTop_dimension['dx']
        self.AngleBarTop_dy     = AngleBarTop_dimension['dy']
        self.AngleBarTop_dz     = AngleBarTop_dimension['dz']
        self.AngleBarTop_gap    = AngleBarTop_dimension['gap']

        self.Angle_length       = Angle_length
        self.Angle_dd           = Angle_dd
        self.N_Angle             = N_Angle
        self.Angle_gap          = (self.AngleBarTop_dz-self.Angle_length*self.N_Angle)/(self.N_Angle-1)

        # Material definitons
        self.ModuleTop_Material = 'Steel'

        self.Material           = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        #innerDetector_builder   = self.get_builder('InnerDetector')

        self.halfDimension  = { 'dx':   self.ModuleTop_dx,
                                'dy':   self.ModuleTop_dy,
                                'dz':   self.ModuleTop_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleTopBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Flange Volume
        flange_shape = geom.shapes.Box('Flange',
                                        dx = self.Flange_dx,
                                        dy = self.Flange_dy,
                                        dz = self.Flange_dz)

        flange_lv = geom.structure.Volume('volFlange',
                                        material=self.ModuleTop_Material,
                                        shape=flange_shape)

        # Place Flange Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-self.Flange_dy,Q('0cm')]

        flange_pos = geom.structure.Position('flange_pos',
                                                pos[0],pos[1],pos[2])

        flange_pla = geom.structure.Placement('flange_pla',
                                                volume=flange_lv,
                                                pos=flange_pos)

        main_lv.placements.append(flange_pla.name)

        # Construct Pillow Top Volume
        pillowTop_shape = geom.shapes.Box('PillowTop',
                                        dx = self.PillowTop_dx,
                                        dy = self.PillowTop_dy,
                                        dz = self.PillowTop_dz)

        pillowTop_lv = geom.structure.Volume('volPillowTop',
                                        material=self.ModuleTop_Material,
                                        shape=pillowTop_shape)

        # Place Pillow Top Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-2*self.Flange_dy-self.PillowTop_dy,Q('0cm')]

        pillowTop_pos = geom.structure.Position('pillowTop_pos',
                                                pos[0],pos[1],pos[2])

        pillowTop_pla = geom.structure.Placement('pillowTop_pla',
                                                volume=pillowTop_lv,
                                                pos=pillowTop_pos)

        main_lv.placements.append(pillowTop_pla.name)

        # Construct Pillow Side Volume
        pillowSide_shape = geom.shapes.Box('PillowSide',
                                        dx = self.PillowSide_dx,
                                        dy = self.PillowSide_dy,
                                        dz = self.PillowSide_dz)

        pillowSide_lv = geom.structure.Volume('volPillowSide',
                                        material=self.ModuleTop_Material,
                                        shape=pillowSide_shape)

        # Place Pillow Side Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-self.PillowSide_dy,Q('0cm')]

        pillowSide_pos = geom.structure.Position('pillowSide_pos',
                                                pos[0],pos[1],pos[2])

        pillowSide_pla = geom.structure.Placement('pillowSide_pla',
                                                volume=pillowSide_lv,
                                                pos=pillowSide_pos)

        main_lv.placements.append(pillowSide_pla.name)

        # Construct Pillow Cavity Volume
        pillowCavity_shape = geom.shapes.Box('PillowCavity',
                                        dx = self.PillowSide_dx-2*self.PillowSide_dd,
                                        dy = self.PillowSide_dy-self.PillowBottom_dy,
                                        dz = self.PillowSide_dz-2*self.PillowSide_dd)

        pillowCavity_lv = geom.structure.Volume('volPillowCavity',
                                        material=self.Material,
                                        shape=pillowCavity_shape)

        # Place Pillow Cavity Volume inside Module Top volume
        pos = [Q('0cm'),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-self.PillowSide_dy+self.PillowBottom_dy,Q('0cm')]

        pillowCavity_pos = geom.structure.Position('pillowCavity_pos',
                                                pos[0],pos[1],pos[2])

        pillowCavity_pla = geom.structure.Placement('pillowCavity_pla',
                                                volume=pillowCavity_lv,
                                                pos=pillowCavity_pos)

        main_lv.placements.append(pillowCavity_pla.name)

        # Construct Angle Bar Top Volume
        angleBarTop_shape = geom.shapes.Box('AngleBarTop',
                                        dx = self.AngleBarTop_dx,
                                        dy = self.AngleBarTop_dy,
                                        dz = self.AngleBarTop_dz)

        angleBarTop_lv = geom.structure.Volume('volAngleBarTop',
                                        material=self.ModuleTop_Material,
                                        shape=angleBarTop_shape)

        # Place Angle Bar Top L Volume inside Module Top volume
        pos = [-self.AngleBarTop_gap-self.AngleBarTop_dx,self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-self.AngleBarTop_dy,Q('0cm')]

        angleBarTop_L_pos = geom.structure.Position('angleBarTop_L_pos',
                                                pos[0],pos[1],pos[2])

        angleBarTop_L_pla = geom.structure.Placement('angleBarTop_L_pla',
                                                volume=angleBarTop_lv,
                                                pos=angleBarTop_L_pos)

        main_lv.placements.append(angleBarTop_L_pla.name)

        # Place Angle Bar Top R Volume inside Module Top volume
        pos = [self.AngleBarTop_gap+self.AngleBarTop_dx,self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-self.AngleBarTop_dy,Q('0cm')]

        rot_y = Q('180.0deg')

        angleBarTop_R_rot = geom.structure.Rotation('angleBarTop_R_rot',
                                                y=rot_y)

        angleBarTop_R_pos = geom.structure.Position('angleBarTop_R_pos',
                                                pos[0],pos[1],pos[2])

        angleBarTop_R_pla = geom.structure.Placement('angleBarTop_R_pla',
                                                volume=angleBarTop_lv,
                                                pos=angleBarTop_R_pos,
                                                rot=angleBarTop_R_rot)

        main_lv.placements.append(angleBarTop_R_pla.name)

        # Construct Angle Base Volume
        angleBase_shape = geom.shapes.Box('AngleBase',
                                        dx = self.AngleBarTop_dx,
                                        dy = self.Angle_dd,
                                        dz = self.Angle_length)

        angleBase_lv = geom.structure.Volume('volAngleBase',
                                        material=self.ModuleTop_Material,
                                        shape=angleBase_shape)

        # Place Angle Base Volume inside  volume
        for i in range(2):
            for j in range(self.N_Angle):
                pos = [(-1)**i*(self.AngleBarTop_gap+angleBase_shape[1]),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-self.Angle_dd,-(self.N_Angle-1-2*j)*self.Angle_length-(self.N_Angle-1-2*j)*self.Angle_gap]

                angleBase_pos = geom.structure.Position('angleBase_pos'+str(i*self.N_Angle+j),
                                                        pos[0],pos[1],pos[2])

                angleBase_pla = geom.structure.Placement('angleBase_pla'+str(i*self.N_Angle+j),
                                                        volume=angleBase_lv,
                                                        pos=angleBase_pos)

                main_lv.placements.append(angleBase_pla.name)

        # Construct Angle Side Volume
        angleSide_shape = geom.shapes.Box('AngleSide',
                                        dx = self.Angle_dd,
                                        dy = self.AngleBarTop_dx-self.Angle_dd,
                                        dz = self.Angle_length)

        angleSide_lv = geom.structure.Volume('volAngleSide',
                                        material=self.ModuleTop_Material,
                                        shape=angleSide_shape)

        # Place Angle Side Volume inside  volume
        for i in range(2):
            for j in range(self.N_Angle):
                pos = [(-1)**i*(self.AngleBarTop_gap+2*self.AngleBarTop_dx-angleSide_shape[1]),self.ModuleTop_dy-2*self.Flange_dy-2*self.PillowTop_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-2*self.Angle_dd-angleSide_shape[2],-(self.N_Angle-1-2*j)*self.Angle_length-(self.N_Angle-1-2*j)*self.Angle_gap]

                angleSide_pos = geom.structure.Position('angleSide_pos'+str(i*self.N_Angle+j),
                                                        pos[0],pos[1],pos[2])

                angleSide_pla = geom.structure.Placement('angleSide_pla'+str(i*self.N_Angle+j),
                                                        volume=angleSide_lv,
                                                        pos=angleSide_pos)

                main_lv.placements.append(angleSide_pla.name)

