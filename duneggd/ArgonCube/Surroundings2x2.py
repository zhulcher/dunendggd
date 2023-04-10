""" TPC.py

Original Author: Z. Hulcher, SLAC

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class Surroundings2x2Builder(gegede.builder.Builder):
    """ Class to build 2x2 immediate surroundings geometry.

    """

    def configure(self,**kwargs):

        # # Read dimensions form config file
        # self.Drift_Length       = Drift_Length

        # Material definitons
        self.Material           = 'LAr'

        # Subbuilders
        self.ArgonCubeCryostat_builder = self.get_builder('ArgonCubeCryostat')
        self.Base_builder   = self.get_builder('Base')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.ArgonCubeCryostat_builder.halfDimension['dx']+self.Base_builder.halfDimension['dx'],
                                'dy':   self.ArgonCubeCryostat_builder.halfDimension['dy']+self.Base_builder.halfDimension['dy'],
                                'dz':   self.ArgonCubeCryostat_builder.halfDimension['dz']+self.Base_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build TPCPlane
        pos = [Q('0mm'),Q('0mm'),Q('0mm')]

        ArgonCubeCryostat_lv = self.ArgonCubeCryostat_builder.get_volume()

        ArgonCubeCryostat_pos = geom.structure.Position(self.ArgonCubeCryostat_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        ArgonCubeCryostat_pla = geom.structure.Placement(self.ArgonCubeCryostat_builder.name+'_pla',
                                                volume=ArgonCubeCryostat_lv,
                                                pos=ArgonCubeCryostat_pos)

        main_lv.placements.append(ArgonCubeCryostat_pla.name)

        # Build TPCPlane
        pos = [Q('0mm'),Q('-7000mm'),Q('0mm')]

        Base_lv = self.Base_builder.get_volume()

        Base_pos = geom.structure.Position(self.Base_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        Base_pla = geom.structure.Placement(self.Base_builder.name+'_pla',
                                                volume=Base_lv,
                                                pos=Base_pos)

        main_lv.placements.append(Base_pla.name)

        


class ExperimentHall2x2Builder(gegede.builder.Builder):
    """ Class to build 2x2 Experiment Hall geometry.

    """

    def configure(self,**kwargs):

        # # Read dimensions form config file

        # Material definitons
        self.Material           = 'LAr'

        # Subbuilders

        self.Surroundings2x2_builder = self.get_builder('Surroundings2x2')
        self.MinervaStand_builder   = self.get_builder('MinervaStand')
        

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Surroundings2x2_builder.halfDimension['dx']+2*self.MinervaStand_builder.halfDimension['dx'],
                                'dy':   self.Surroundings2x2_builder.halfDimension['dy']+2*self.MinervaStand_builder.halfDimension['dy'],
                                'dz':   self.Surroundings2x2_builder.halfDimension['dz']+2*self.MinervaStand_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build TPCPlane
        pos = [-self.Drift_Length,Q('0mm'),Q('0mm')]

        TPCPlane_lv = self.TPCPlane_builder.get_volume()

        TPCPlane_pos = geom.structure.Position(self.TPCPlane_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        TPCPlane_pla = geom.structure.Placement(self.TPCPlane_builder.name+'_pla',
                                                volume=TPCPlane_lv,
                                                pos=TPCPlane_pos)

        main_lv.placements.append(TPCPlane_pla.name)

        # Construct TPCActive
        TPCActive_shape = geom.shapes.Box('TPCActive_shape',
                                        dx =    self.Drift_Length,
                                        dy =    self.TPCPlane_builder.halfDimension['dy'],
                                        dz =    self.TPCPlane_builder.halfDimension['dz'])

        TPCActive_lv = geom.structure.Volume('volTPCActive',
                                        material=self.Material,
                                        shape=TPCActive_shape)

        TPCActive_lv.params.append(("SensDet","TPCActive_shape"))
        TPCActive_lv.params.append(("EField","(500.0 V/cm, 0.0 V/cm, 0.0 V/cm)"))

        # Place TPCActive
        pos = [self.TPCPlane_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

        TPCActive_pos = geom.structure.Position('TPCActive_pos',
                                                pos[0],pos[1],pos[2])

        TPCActive_pla = geom.structure.Placement('TPCActive_pla',
                                                volume=TPCActive_lv,
                                                pos=TPCActive_pos)

        main_lv.placements.append(TPCActive_pla.name)

        # Place E-Field
        #TPCActive_lv.params.append(("EField",self.EField))


