#!/usr/bin/env python
""" Base.py

Original Author: Z. Hulcher, SLAC

"""
#All your base are belong to us

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BaseBuilder(gegede.builder.Builder):
    '''
    Assemble 2x2 Base blocks
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                    block  = [Q('0cm'),Q('0cm'),Q('0cm')], 
                    base = 0,
                #   modSteelPlateDim = None, 
                #   modNTraysPerPlane = None, 
                #   modNPlanes = None,
                #   modMuidRot = None,
                #   modMuidMat = 'Steel',
                   **kwds):

        self.Material="Air"
        self.blockmaterial="Concrete"
        self.block=block
        self.base=base






        # self.muidAbsPos     = modMuidPos
        # self.muidMat        = modMuidMat 
        # self.muidDim        = modMuidDim 
        # self.steelPlateDim  = modSteelPlateDim 
        # self.nTraysPerPlane = modNTraysPerPlane 
        # self.nPlanes        = modNPlanes 
        # self.muidRot        = modMuidRot 
        
        #print( self.builders)
        # self.RPCTrayBldr = self.get_builder('RPCTray_End')
        return

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        self.halfDimension = {'dx':  self.block['dx'],
                              'dy':  self.block['dy'],
                              'dz':  self.base}


        



        # main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        # print('DetectorBuilder::construct()')
        # print(('main_lv = '+main_lv.name))
        # self.add_volume(main_lv)
        # toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
        # botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
        # midpos = [Q('0cm'),Q('0cm'), Q('0cm')]

        # lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
        # midshape=geom.shapes.Box(None, self.midheight/2, self.length/2,self.midthick/2)

        # toplip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
        # botlip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
        # mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)

        # toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
        # botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
        # mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])

        # toplip_pla = geom.structure.Placement(None,volume=toplip_lv, pos=toplip_pos)
        # botlip_pla = geom.structure.Placement(None,volume=botlip_lv, pos=botlip_pos)
        # mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)

        # main_lv.placements.append(toplip_pla.name)
        # main_lv.placements.append(botlip_pla.name)
        # main_lv.placements.append(mid_pla.name)

        # Get the RPC tray volume and position
        # rpcTray_lv = self.RPCTrayBldr.get_volume('volRPCTray_End')
        # rpcTrayDim = self.RPCTrayBldr.rpcTrayDim
        
        # Calculate the muidDim[2] (z dim) with other configured parameters: 
        #   number of planes, thicknesses...
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        self.add_volume(main_lv)
        print("block",self.block)

        # Make volume to be retrieved by DetectorBuilder
        # baseshape = geom.shapes.Box( self.name,
        #                            dx=0.5*self.block['dx'],
        #                            dy=0.5*self.block['dy'],
        #                            dz=0.5*self.base)
        # base_lv = geom.structure.Volume('vol'+self.name, material=self.hallmaterial, shape=baseshape)
        # self.add_volume(base_lv)

        # Place the RPC trays and steel sheets between in the configured way
        # Steel Sheets: just leave the default material of volMuID* steel 
        #   and leave spaces instead of placing explicit volumes
	
        # print(( 'Abs pos for '+ str(self.name) +' along Z: '+ str(self.muidAbsPos[2])))


        
        
        # for i in range(self.nPlanes):
        #     zpos = -0.5*self.muidDim[2]+(i+0.5)*rpcTrayDim[2]+i*self.steelPlateDim[2]+self.muidAbsPos[2]
        #     for j in range(self.nTraysPerPlane):

        #         xpos = Q('0cm')+self.muidAbsPos[0]
        #         ypos = -0.5*self.muidDim[1]+(j+0.5)*rpcTrayDim[1]+self.muidAbsPos[1]
        
        #         rpct_in_muid  = geom.structure.Position( 'rpct-'+str(self.nTraysPerPlane*i+j)+'_in_'+self.name,
        #                                                  xpos,  ypos,  zpos)
        #         prpct_in_muid = geom.structure.Placement( 'prpct-'+str(self.nTraysPerPlane*i+j)+'_in_'+self.name,
        #                                                   volume = rpcTray_lv, pos = rpct_in_muid, rot=self.muidRot )

        #         muid_lv.placements.append( prpct_in_muid.name )

        block_shape= geom.shapes.Box(None, self.block['dx'], self.block['dy'],self.block['dz'])

        block_lv = geom.structure.Volume(
            None, material='ReifConcrete', shape=block_shape)

        block1_pos  = geom.structure.Position( 'block1_in_'+self.name,Q('0cm'),  Q('0cm'),  self.base-self.block['dz'])
        pblock1_pla = geom.structure.Placement( 'pblock1_in_'+self.name,volume = block_lv, pos = block1_pos)

        block2_pos  = geom.structure.Position( 'block2_in_'+self.name,Q('0cm'),  Q('0cm'),  -self.base+self.block['dz'])
        pblock2_pla = geom.structure.Placement( 'pblock2_in_'+self.name,volume = block_lv, pos = block2_pos)

        main_lv.placements.append( pblock1_pla.name )
        main_lv.placements.append( pblock2_pla.name )

        print("got here4")
