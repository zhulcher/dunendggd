""" TPC.py

Original Author: Z. Hulcher, SLAC

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class Surroundings2x2Builder(gegede.builder.Builder):
    """ Class to build 2x2 immediate surroundings geometry.

    """

    def configure(self,Hall=None,OuterBeam=None,InnerBeam=None,**kwargs):

        # # Read dimensions form config file
        # self.Drift_Length       = Drift_Length

        # Material definitons
        self.Material           = 'LAr'
        self.Hall=Hall

        # Subbuilders
        self.ArgonCubeCryostat_builder = self.get_builder('ArgonCubeCryostat')
        self.MinervaStand_builder = self.get_builder('MinervaStand')
        self.Base_builder   = self.get_builder('Base')
        self.OuterBeam=OuterBeam
        self.InnerBeam=InnerBeam
        self.BeamMaterial="SSteel304"


    def construct(self,geom):

        def buildabeam(L,lipthick,middlethick,lipwidth,middlewidth,lipL,lipoffset=Q('0mm')):
            
            lipbox=geom.shapes.Box(None, lipwidth, lipL, lipthick)
            middlebox=geom.shapes.Box(None, middlethick, L, middlewidth)
            lip1_pos=geom.structure.Position( None,Q('0mm'), lipoffset, middlewidth+lipthick)
            lip2_pos=geom.structure.Position( None,Q('0mm'), lipoffset, -middlewidth-lipthick)
            beamtemp=geom.shapes.Boolean(None,'union',middlebox,lipbox,lip1_pos)
            return geom.shapes.Boolean(None,'union',beamtemp,lipbox,lip2_pos)


        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Hall['dx'],
                                'dy':   self.Hall['dy'],
                                'dz':   self.Hall['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)


        # Build TPCPlane
        pos = [Q('0mm'),Q('0mm'),Q('0mm')]
        pos1 = [Q('0mm'),-self.MinervaStand_builder.sbi1_pos.y + self.MinervaStand_builder.sbiheight - (self.ArgonCubeCryostat_builder.dz+2*self.Base_builder.block['dy']),Q('175in')]
        pos2 = [Q('0mm'),-self.MinervaStand_builder.sbi1_pos.y + self.MinervaStand_builder.sbiheight - (self.ArgonCubeCryostat_builder.dz+2*self.Base_builder.block['dy']),Q('-75in')]
        
        MinervaStand_lv = self.MinervaStand_builder.get_volume()

        MinervaStand1_pos = geom.structure.Position(None,
                                            pos1[0],pos1[1],pos1[2])
        MinervaStand2_pos = geom.structure.Position(None,
                                            pos2[0],pos2[1],pos2[2])

        MinervaStand1_pla = geom.structure.Placement(None,
                                                volume=MinervaStand_lv,
                                                pos=MinervaStand1_pos)
        
        rot= geom.structure.Rotation( None, y='0 deg')
        
        MinervaStand2_pla = geom.structure.Placement(None,
                                                volume=MinervaStand_lv,
                                                pos=MinervaStand2_pos,
                                                rot=rot)

        main_lv.placements.append(MinervaStand1_pla.name)
        main_lv.placements.append(MinervaStand2_pla.name)

        ArgonCubeCryostat_lv = self.ArgonCubeCryostat_builder.get_volume()

        ArgonCubeCryostat_pos = geom.structure.Position(self.ArgonCubeCryostat_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])
        
        rot= geom.structure.Rotation( None, x='90 deg')

        ArgonCubeCryostat_pla = geom.structure.Placement(self.ArgonCubeCryostat_builder.name+'_pla',
                                                volume=ArgonCubeCryostat_lv,
                                                pos=ArgonCubeCryostat_pos,
                                                rot=rot)
        

        main_lv.placements.append(ArgonCubeCryostat_pla.name)

        # Build TPCPlane
        pos = [Q('0mm'),-self.ArgonCubeCryostat_builder.dz-self.Base_builder.block['dy'],Q('0mm')]

        Base_lv = self.Base_builder.get_volume()

        Base_pos = geom.structure.Position(self.Base_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        Base_pla = geom.structure.Placement(self.Base_builder.name+'_pla',
                                                volume=Base_lv,
                                                pos=Base_pos)

        main_lv.placements.append(Base_pla.name)

                #top platform ------------
        platx=Q('5740.4mm')/2
        platy=Q('17mm')/2
        platz=Q('2712mm')/2
        cylcutrad=Q('2387.3mm')/2
        cylcut=geom.shapes.Tubs(None,Q('0mm'),cylcutrad,Q('1500mm'))
        top=geom.shapes.Box(None,platx,platy,platz)

        cylcutx=-(platx-cylcutrad-Q('2238mm'))

        cut_pos = geom.structure.Position(None, cylcutx, Q('0mm'), Q('0mm'))
        rot = geom.structure.Rotation(None,x='90 deg')
        U=geom.shapes.Boolean(None,'subtraction',top,cylcut,cut_pos,rot=rot)

# x=2238-rad=
        

        platbeamminiSS=buildabeam(Q('6096mm')/2,Q('7.1mm')/2,Q('5.8mm')/2,Q('101.6mm')/2,Q('129mm')/2,Q('6096mm')/2)
        platbeamminiS=buildabeam(Q('6096mm')/2,Q('7.1mm')/2,Q('5.8mm')/2,Q('101.6mm')/2,Q('129mm')/2,Q('6096mm')/2)
        platbeamminiL=buildabeam(Q('2845mm')/2,Q('7.1mm')/2,Q('5.8mm')/2,Q('101.6mm')/2,Q('129mm')/2,Q('2851mm')/2)



        platbeammaxS=buildabeam(Q('2845mm')/2,Q('8.4mm')/2,Q('5.8mm')/2,Q('133.3mm')/2,Q('190mm')/2,Q('2851mm')/2)
        platbeammaxL=buildabeam(Q('6096mm')/2,Q('8.4mm')/2,Q('5.8mm')/2,Q('133.3mm')/2,Q('190mm')/2,Q('6096mm')/2)

        flatoverbeams_pos = geom.structure.Position(None, Q('0mm'), Q('0mm'),Q('0mm'))
        beam1_pos= geom.structure.Position( None,platx-Q('609.5mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        beam2_pos= geom.structure.Position( None,platx-Q('609.5mm')-Q('433mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        beam3_pos= geom.structure.Position( None,-platx+3*Q('609.5mm')+Q('355.2mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        beam4_pos= geom.structure.Position( None,-platx+3*Q('609.5mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        beam5_pos= geom.structure.Position( None,-platx+2*Q('609.5mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        beam6_pos= geom.structure.Position( None,-platx+Q('609.5mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        

        

        

        beam7_pos= geom.structure.Position( None,Q('0mm'), -platy-Q('8.4mm')-Q('190mm')/2, Q('2845mm')/2)


        beam8_pos= geom.structure.Position( None,Q('0mm'), -platy-Q('8.4mm')-Q('190mm')/2, -Q('2845mm')/2)

        beam9_pos= geom.structure.Position( None,-platx, -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))
        beam10_pos= geom.structure.Position( None,platx, -platy-Q('8.4mm')-Q('190mm')/2, Q('0mm'))


        rot = geom.structure.Rotation(None,x='90 deg')
        # U=geom.shapes.Boolean(None,'union',U,platbeamminiL,flatoverbeams_pos,rot=rot)

        U=geom.shapes.Boolean(None,'union',U,platbeamminiL,beam1_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeamminiL,beam2_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeamminiL,beam3_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeamminiL,beam4_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeamminiL,beam5_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeamminiL,beam6_pos,rot=rot)

        U=geom.shapes.Boolean(None,'union',U,platbeammaxS,beam9_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeammaxS,beam10_pos,rot=rot)

        rot = geom.structure.Rotation(None,y='90 deg',z='90 deg')
        U=geom.shapes.Boolean(None,'union',U,platbeammaxL,beam7_pos,rot=rot)
        U=geom.shapes.Boolean(None,'union',U,platbeammaxL,beam8_pos,rot=rot)

        # U=geom.shapes.Boolean(None,'union',U,platbeam,beam7_pos)
        # rot = geom.structure.Rotation(None,x='90 deg')
        

        top_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=U)
        Bot_pos = geom.structure.Position(None, -cylcutx, Q('800mm'), Q('0mm'))
        # rot = geom.structure.Rotation(None,x='90 deg')

        Bot_pla = geom.structure.Placement(None, volume= top_lv, pos = Bot_pos)
        main_lv.placements.append(Bot_pla.name)
        






        #top platform ------------


        


# class ExperimentHall2x2Builder(gegede.builder.Builder):
#     """ Class to build 2x2 Experiment Hall geometry.

#     """

#     def configure(self,**kwargs):

#         # # Read dimensions form config file

#         # Material definitons
#         self.Material           = 'LAr'

#         # Subbuilders

#         self.Surroundings2x2_builder = self.get_builder('Surroundings2x2')
#         self.MinervaStand_builder   = self.get_builder('MinervaStand')
        

#     def construct(self,geom):
#         """ Construct the geometry.

#         """

#         self.halfDimension  = { 'dx':   self.Surroundings2x2_builder.halfDimension['dx']+2*self.MinervaStand_builder.halfDimension['dx'],
#                                 'dy':   self.Surroundings2x2_builder.halfDimension['dy']+2*self.MinervaStand_builder.halfDimension['dy'],
#                                 'dz':   self.Surroundings2x2_builder.halfDimension['dz']+2*self.MinervaStand_builder.halfDimension['dz']}

#         main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
#         print('TPCBuilder::construct()')
#         print(('main_lv = '+main_lv.name))
#         self.add_volume(main_lv)

#         # Build TPCPlane
#         pos = [-self.Drift_Length,Q('0mm'),Q('0mm')]

#         TPCPlane_lv = self.TPCPlane_builder.get_volume()

#         TPCPlane_pos = geom.structure.Position(self.TPCPlane_builder.name+'_pos',
#                                             pos[0],pos[1],pos[2])

#         TPCPlane_pla = geom.structure.Placement(self.TPCPlane_builder.name+'_pla',
#                                                 volume=TPCPlane_lv,
#                                                 pos=TPCPlane_pos)

#         main_lv.placements.append(TPCPlane_pla.name)

#         # Construct TPCActive
#         TPCActive_shape = geom.shapes.Box('TPCActive_shape',
#                                         dx =    self.Drift_Length,
#                                         dy =    self.TPCPlane_builder.halfDimension['dy'],
#                                         dz =    self.TPCPlane_builder.halfDimension['dz'])

#         TPCActive_lv = geom.structure.Volume('volTPCActive',
#                                         material=self.Material,
#                                         shape=TPCActive_shape)

#         TPCActive_lv.params.append(("SensDet","TPCActive_shape"))
#         TPCActive_lv.params.append(("EField","(500.0 V/cm, 0.0 V/cm, 0.0 V/cm)"))

#         # Place TPCActive
#         pos = [self.TPCPlane_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

#         TPCActive_pos = geom.structure.Position('TPCActive_pos',
#                                                 pos[0],pos[1],pos[2])

#         TPCActive_pla = geom.structure.Placement('TPCActive_pla',
#                                                 volume=TPCActive_lv,
#                                                 pos=TPCActive_pos)

#         main_lv.placements.append(TPCActive_pla.name)

#         # Place E-Field
#         #TPCActive_lv.params.append(("EField",self.EField))


