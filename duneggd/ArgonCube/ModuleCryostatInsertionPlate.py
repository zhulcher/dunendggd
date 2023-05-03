""" ModuleCryostatInsertionPlate.py
Modified from Module.py
Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleCryostatInsertionPlateBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,**kwargs):

        # Material definitons

        self.Material   = 'Air'

        # Subbuilders
        self.Flange_builder         = self.get_builder('FlangeCryostatInsertionPlate')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_builder.halfDimension['dx'],
                                'dy':   self.Flange_builder.halfDimension['dy'],
                                'dz':   self.Flange_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build CryostatInsertionPlate
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Flange_lv = self.Flange_builder.get_volume()

        Flange_pos = geom.structure.Position(self.Flange_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement(self.Flange_builder.name+'_pla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        main_lv.placements.append(Flange_pla.name)


