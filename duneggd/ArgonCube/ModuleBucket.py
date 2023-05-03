""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBucketBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,**kwargs):

        # Material definitons

        self.Material   = 'Air'

        # Subbuilders
        self.Bucket_builder         = self.get_builder('Bucket')
        self.Flange_builder         = self.get_builder('Flange')
        self.HVFeedThrough_builder  = self.get_builder('HVFeedThrough')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Bucket_builder.halfDimension['dx'],
                                'dy':   self.Bucket_builder.halfDimension['dy'],
                                'dz':   self.Bucket_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build Bucket
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Bucket_builder.halfDimension['dy'],Q('0cm')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_pla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos)

        main_lv.placements.append(Bucket_pla.name)
