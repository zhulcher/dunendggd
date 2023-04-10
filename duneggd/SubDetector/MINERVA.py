#!/usr/bin/env python
""" MINERVA.py

Original Author: Z. Hulcher, SLAC

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import math as m


# class MINERVABuilder(gegede.builder.Builder):
#     '''
#     Assemble Minerva Support Structure
#     '''

#     #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
#     def configure(self,
#                 #   modMuidPos = [Q('0cm'),Q('0cm'),Q('0cm')], 
#                 #   modMuidDim = None,
#                 #   modSteelPlateDim = None, 
#                 #   modNTraysPerPlane = None, 
#                 #   modNPlanes = None,
#                 #   modMuidRot = None,
#                 #   modMuidMat = 'Steel',
#                    **kwds):

#         self.Beammaterial="steel"



#         # self.muidAbsPos     = modMuidPos
#         # self.muidMat        = modMuidMat 
#         # self.muidDim        = modMuidDim 
#         # self.steelPlateDim  = modSteelPlateDim 
#         # self.nTraysPerPlane = modNTraysPerPlane 
#         # self.nPlanes        = modNPlanes 
#         # self.muidRot        = modMuidRot 
        
#         #print( self.builders)
#         # self.RPCTrayBldr = self.get_builder('RPCTray_End')
#         return

#     #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
#     def construct(self, geom):

#         # Get the RPC tray volume and position
#         # rpcTray_lv = self.RPCTrayBldr.get_volume('volRPCTray_End')
#         # rpcTrayDim = self.RPCTrayBldr.rpcTrayDim
        
#         # Calculate the muidDim[2] (z dim) with other configured parameters: 
#         #   number of planes, thicknesses...


#         # Make volume to be retrieved by DetectorBuilder
#         muidBox = geom.shapes.Box( self.name,
#                                    dx=0.5*self.muidDim[0],
#                                    dy=0.5*self.muidDim[1],
#                                    dz=0.5*self.muidDim[2])
#         muid_lv = geom.structure.Volume('vol'+self.name, material=self.muidMat, shape=muidBox)
#         self.add_volume(muid_lv)

#         # Place the RPC trays and steel sheets between in the configured way
#         # Steel Sheets: just leave the default material of volMuID* steel 
#         #   and leave spaces instead of placing explicit volumes
	
#         print(( 'Abs pos for '+ str(self.name) +' along Z: '+ str(self.muidAbsPos[2])))
        
#         for i in range(self.nPlanes):
#             zpos = -0.5*self.muidDim[2]+(i+0.5)*rpcTrayDim[2]+i*self.steelPlateDim[2]+self.muidAbsPos[2]
#             for j in range(self.nTraysPerPlane):

#                 xpos = Q('0cm')+self.muidAbsPos[0]
#                 ypos = -0.5*self.muidDim[1]+(j+0.5)*rpcTrayDim[1]+self.muidAbsPos[1]
        
#                 rpct_in_muid  = geom.structure.Position( 'rpct-'+str(self.nTraysPerPlane*i+j)+'_in_'+self.name,
#                                                          xpos,  ypos,  zpos)
#                 prpct_in_muid = geom.structure.Placement( 'prpct-'+str(self.nTraysPerPlane*i+j)+'_in_'+self.name,
#                                                           volume = rpcTray_lv, pos = rpct_in_muid, rot=self.muidRot )

#                 muid_lv.placements.append( prpct_in_muid.name )
        
        
#         return


class MINERVAStandBuilder(gegede.builder.Builder):
    '''
    Assemble Minerva Support Structure
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                    OuterBeam  = {'dx':Q('0mm')/2,'dyb':Q('0mm')/2,'dyt':Q('0mm')/2,'dz':Q('0mm')/2},
                    InnerBeam  = {'dx':Q('0mm')/2,'dyb':Q('0mm')/2,'dyt':Q('0mm')/2 ,'dz':Q('0mm')/2},
                    # block  = [Q('0cm'),Q('0cm'),Q('0cm')], 
                    # base = 0,
                #   modSteelPlateDim = None, 
                #   modNTraysPerPlane = None, 
                #   modNPlanes = None,
                #   modMuidRot = None,
                #   modMuidMat = 'Steel',
                   **kwds):

        self.Material="Air"
        self.BeamMaterial="SSteel304"
        self.OuterBeam=OuterBeam
        self.InnerBeam=InnerBeam
        # self.blockmaterial="Concrete"
        # self.block=block
        # self.base=base






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

        self.halfDimension = {'dx':  Q('5100mm'),
                              'dy':  Q('4356.1mm'),
                              'dz':  Q('2011.2mm')}
        
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        self.add_volume(main_lv)


        def buildabeam(self,L,lipthick,middlethick,lipwidth,middlewidth,lipL,lipoffset=Q('0mm')):
            
            lipbox=geom.shapes.Box(None, lipwidth, lipL, lipthick)
            middlebox=geom.shapes.Box(None, middlethick, L, middlewidth)
            lip1_pos=geom.structure.Position( None,Q('0mm'), lipoffset, middlewidth+lipthick)
            lip2_pos=geom.structure.Position( None,Q('0mm'), lipoffset, -middlewidth-lipthick)
            beamtemp=geom.shapes.Boolean(None,'union',middlebox,lipbox,lip1_pos)
            return geom.shapes.Boolean(None,'union',beamtemp,lipbox,lip2_pos)
            
            



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

        #arc--------------------
        
        # print("block",self.block)
        # OB = geom.shapes.Box(None, self.OuterBeam['dx'], self.OuterBeam['dyb'], self.OuterBeam['dz'])
        # OT = geom.shapes.Box(None, self.OuterBeam['dx'], self.OuterBeam['dyt'], self.OuterBeam['dz'])
        # IB = geom.shapes.Box(None, self.InnerBeam['dx'], self.InnerBeam['dyb'], self.InnerBeam['dz'])
        # IT = geom.shapes.Box(None, self.InnerBeam['dx'], self.InnerBeam['dyt'], self.InnerBeam['dz'])

        # OP_pos  = geom.structure.Position( 'OB_in_'+self.name,Q('0mm'), self.OuterBeam['dyb']-self.InnerBeam['dyb'], self.InnerBeam['dz']+self.OuterBeam['dz'])
        # OM_pos  = geom.structure.Position( 'OM_in_'+self.name,Q('0mm'), self.OuterBeam['dyb']-self.InnerBeam['dyb'], -self.InnerBeam['dz']-self.OuterBeam['dz'])

        lipP_pos  = geom.structure.Position( 'botlipP_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        lipM_pos  = geom.structure.Position( 'botlipM_in_'+self.name,Q('0mm'), Q('0mm'), -self.InnerBeam['dz']-self.OuterBeam['dz'])
        # I_pos  = geom.structure.Position( 'IB_in_'+self.name,Q('0mm'), Q('0mm') ,  self.InnerBeam['dz']+self.OuterBeam['dz'])

        # Btemp=geom.shapes.Boolean('MINERVABtemp','union',IB,OB,OP_pos)
        # B=geom.shapes.Boolean('MINERVAB','union',Btemp,OB,OM_pos)

        B=buildabeam(self,self.InnerBeam['dyb'],self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],self.OuterBeam['dyb'],-self.InnerBeam['dyb']+self.OuterBeam['dyb'])
        T=buildabeam(self,self.InnerBeam['dyt'],self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],self.OuterBeam['dyt'])

        # Ttemp=geom.shapes.Boolean('MINERVATtemp','union',IT,OT,lipP_pos)
        # T=geom.shapes.Boolean('MINERVAT','union',Ttemp,OT,lipM_pos)

        L_pos=geom.structure.Position( 'L_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3)/2,  self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'], Q('0mm'))

        rot = geom.structure.Rotation(None,z='60 deg')
        L=geom.shapes.Boolean('MINERVAL','union',B,T,L_pos,rot)

        rot=geom.structure.Rotation(None,y='180 deg')

        R_pos=geom.structure.Position( 'R_in_'+self.name,-4*self.InnerBeam['dyt']*m.sqrt(3)/2,Q('0mm'),  Q('0mm'))

        Msupp=geom.shapes.Boolean('Msupp','union',L,L,R_pos,rot)




        # OB_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=OB)
        # OT_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=OT)
        # IB_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=IB)
        # IT_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=IT)

        Msupp_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=Msupp)
        Msupp_pos=geom.structure.Position( 'Msupp_in_'+self.name,2*self.InnerBeam['dyt']*m.sqrt(3)/2, Q('0mm'),  Q('0mm'))
        Msupp_pla = geom.structure.Placement('pMsupp_in_'+self.name, volume= Msupp_lv, pos = Msupp_pos)
        main_lv.placements.append(Msupp_pla.name)



        botlen=self.OuterBeam['dyt']*m.sqrt(3)

        Obot = geom.shapes.Box(None, self.OuterBeam['dx'], botlen, self.OuterBeam['dz'])
        Ibot = geom.shapes.Box(None, self.InnerBeam['dx'], botlen, self.InnerBeam['dz'])


        Bottemp=geom.shapes.Boolean(None,'union',Ibot,Obot,lipP_pos)
        Bot=geom.shapes.Boolean('botbeam','union',Bottemp,Obot,lipM_pos)

        botbeamheight=Q('-1500mm')#?????????????????????????????/


        Bot_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=Bot)
        Bot_pos = geom.structure.Position('Bot_in_'+self.name,  Q('0mm'), botbeamheight, Q('0mm'))
        rot = geom.structure.Rotation(None,z='90 deg')
        Bot_pla = geom.structure.Placement('pBot_in_'+self.name, volume= Bot_lv, pos = Bot_pos,rot=rot)
        main_lv.placements.append(Bot_pla.name)
        #arc--------------------




        #cylinders--------------
        supOdx=Q('44.4mm')
        supIdx=Q('38.1mm')
        suplen=Q('2070.1mm')
        botBpos=[Q('44.4mm'),Q('-1000mm'),Q('44.4mm')]

        cylsuploc=[-Q('1000mm'),Q('2000mm'),Q('0mm')]

        cylsupO=geom.shapes.Box(None,suplen/2,supOdx,supOdx)
        cylsupI=geom.shapes.Box(None,suplen/2,supIdx,supIdx)
        cylsup=geom.shapes.Boolean('cylsup','subtraction',cylsupO,cylsupI)
        cylsup_lv=geom.structure.Volume(None, material=self.BeamMaterial, shape=cylsup)

        rot=geom.structure.Rotation(None,z='-30 deg')
        cylsupL_pos = geom.structure.Position('cylsupL_in_'+self.name, cylsuploc[0], cylsuploc[1], cylsuploc[2])
        cylsupL_pla = geom.structure.Placement('pcylsupL_in_'+self.name, volume= cylsup_lv, pos = cylsupL_pos,rot=rot)
        main_lv.placements.append(cylsupL_pla.name)

        rot=geom.structure.Rotation(None,z='30 deg')
        cylsupR_pos = geom.structure.Position('cylsupR_in_'+self.name, -cylsuploc[0], cylsuploc[1], cylsuploc[2])
        cylsupR_pla = geom.structure.Placement('pcylsupR_in_'+self.name, volume= cylsup_lv, pos = cylsupR_pos,rot=rot)
        main_lv.placements.append(cylsupR_pla.name)

        cyldiam=Q('152.4mm')
        cyllen=Q('305mm')

        cyldiff=Q('1912.2mm')/9
        

        topcyl=geom.shapes.Tubs(None,Q('0mm'),cyldiam/2,cyllen/2)
        # store=geom.shapes.Box(None, self.OuterBeam['dx'], botlen, self.OuterBeam['dz'])

        topcyl_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=topcyl)

        poslist=[]




        plalist=[]
        rot = geom.structure.Rotation(None,'90 deg','30 deg','0 deg')
        for i in range(-4,6):
            poslist+=[geom.structure.Position( 'cylR_'+str(i)+'L_in_'+self.name,cyldiff*i*m.sin(60*m.pi/180)+cylsuploc[0]-(cyllen/2+supOdx)*m.cos(60*m.pi/180), cyldiff*i*m.cos(60*m.pi/180)+cylsuploc[1]+(cyllen/2+supOdx)*m.sin(60*m.pi/180), cylsuploc[2])]
            plalist+=[geom.structure.Placement('pcylR_'+str(i)+'L_in_'+self.name, volume= topcyl_lv, pos = poslist[-1],rot=rot)]
            main_lv.placements.append(plalist[-1].name)
        rot = geom.structure.Rotation(None,'90 deg','-30 deg','0 deg')
        for i in range(-4,6):
            if i!=3:
                poslist+=[geom.structure.Position( 'cylL_'+str(i)+'L_in_'+self.name,-cyldiff*i*m.sin(60*m.pi/180)-cylsuploc[0]+(cyllen/2+supOdx)*m.cos(60*m.pi/180), cyldiff*i*m.cos(60*m.pi/180)+cylsuploc[1]+(cyllen/2+supOdx)*m.sin(60*m.pi/180), cylsuploc[2])]
                plalist+=[geom.structure.Placement('pcylL_'+str(i)+'L_in_'+self.name, volume= topcyl_lv, pos = poslist[-1],rot=rot)]
                main_lv.placements.append(plalist[-1].name)

        #cylinders--------------

        #side-------------------

        # suppill

        supboxB = geom.shapes.Box(None, Q('393.7mm')/2, Q('19mm')/2, Q('393.7mm')/2)
        supboxT = geom.shapes.Box(None, Q('355.6mm')/2, Q('28.6mm')/2, Q('355.6mm')/2)
        BoverT= geom.structure.Position('BoverT_in_'+self.name, Q('0mm'),Q('19mm')/2+Q('28.6mm')/2, Q('0mm'))
        supbox=geom.shapes.Boolean('subbox','union',supboxB,supboxT,pos=BoverT)
        suppill=geom.shapes.Boolean('suppill','union',supbox,supboxT,pos=BoverT)

        suppillh=Q('1500mm')

        sidelen = Q('1200mm')


        sbi=buildabeam(self,suppillh,self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],suppillh)
        sbibase_pos=geom.structure.Position('sbibase_in_sbi_in_'+self.name, Q('0mm'), -suppillh, Q('0mm'))

        sidebeam=geom.shapes.Boolean(None,'union',sbi,suppill,sbibase_pos)
        sbi_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=sidebeam)

        sbi1_pos = geom.structure.Position('sbi1_in_'+self.name, 2*self.InnerBeam['dyt']*m.sqrt(3)/2, botBpos[1],-4*self.OuterBeam['dz']-2*self.InnerBeam['dz'])
        sbi1_pla = geom.structure.Placement('psbi1_in_'+self.name, volume= sbi_lv, pos = sbi1_pos)
        main_lv.placements.append(sbi1_pla.name)

        sbi1_pos = geom.structure.Position('sbi2_in_'+self.name, -2*self.InnerBeam['dyt']*m.sqrt(3)/2, botBpos[1],-4*self.OuterBeam['dz']-2*self.InnerBeam['dz'])
        sbi1_pla = geom.structure.Placement('psbi2_in_'+self.name, volume= sbi_lv, pos = sbi1_pos)
        main_lv.placements.append(sbi1_pla.name)

        sbi1_pos = geom.structure.Position('sbi3_in_'+self.name, 2*self.InnerBeam['dyt']*m.sqrt(3)/2, botBpos[1],-2*sidelen)
        sbi1_pla = geom.structure.Placement('psbi3_in_'+self.name, volume= sbi_lv, pos = sbi1_pos)
        main_lv.placements.append(sbi1_pla.name)

        sbi1_pos = geom.structure.Position('sbi4_in_'+self.name, -2*self.InnerBeam['dyt']*m.sqrt(3)/2, botBpos[1],-2*sidelen)
        sbi1_pla = geom.structure.Placement('psbi4_in_'+self.name, volume= sbi_lv, pos = sbi1_pos)
        main_lv.placements.append(sbi1_pla.name)

        # suppill_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=suppill)
        # suppill_pos = geom.structure.Position('BotB_in_'+self.name, botBpos[0], botBpos[1], botBpos[2])
        # suppill_pla = geom.structure.Placement('pBotB_in_'+self.name, volume= suppill_lv, pos = suppill_pos)
        # main_lv.placements.append(suppill_pla.name)

       
        # supboxT_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=supboxT)
        # supboxT_pos = geom.structure.Position('BotT_in_'+self.name, botBpos[0], botBpos[1]+Q('19mm')/2+Q('28.6mm')/2, botBpos[2])
        # supboxT_pla = geom.structure.Placement('pBotT_in_'+self.name, volume= supboxT_lv, pos = supboxT_pos)
        # main_lv.placements.append(supboxT_pla.name)

        scOdx=Q('100mm')
        scIdx=Q('90mm')
        sidecrossO=geom.shapes.Box(None,suplen/2,scOdx,scOdx)
        sidecrossI=geom.shapes.Box(None,suplen/2,scIdx,scIdx)
        sidecross=geom.shapes.Boolean('sidecross','subtraction',sidecrossO,sidecrossI)

        #boolean subtract two blocks 
        cylsup_lv=geom.structure.Volume(None, material=self.BeamMaterial, shape=cylsup)




        
        # suppheight=



        # Oside = geom.shapes.Box(None, self.OuterBeam['dx'], sidelen, self.OuterBeam['dz'])
        # Iside = geom.shapes.Box(None, self.InnerBeam['dx'], sidelen, self.InnerBeam['dz'])

        # sidetemp=geom.shapes.Boolean(None,'union',Iside,Oside,OP_pos)
        # side=geom.shapes.Boolean('sidebeam','union',sidetemp,Oside,OM_pos)

        side=buildabeam(self,sidelen,self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],sidelen)

        
        botbeamheight=Q('-1500mm')#?????????????????????????????/
        side_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=side)
        Bot_pos = geom.structure.Position('sidebeam1_in_'+self.name, -2*self.InnerBeam['dyt']*m.sqrt(3)/2, self.InnerBeam['dyt']/2, -sidelen-self.InnerBeam['dz']/2-self.OuterBeam['dz'])
        rot = geom.structure.Rotation(None,x='90 deg')
        Bot_pla = geom.structure.Placement('psidebeam1_in_'+self.name, volume= side_lv, pos = Bot_pos,rot=rot)
        main_lv.placements.append(Bot_pla.name)

        botbeamheight=Q('-1500mm')#?????????????????????????????/
        side_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=side)
        Bot_pos = geom.structure.Position('sidebeam2_in_'+self.name, 2*self.InnerBeam['dyt']*m.sqrt(3)/2, self.InnerBeam['dyt']/2, -sidelen-self.InnerBeam['dz']/2-self.OuterBeam['dz'])
        rot = geom.structure.Rotation(None,x='90 deg')
        Bot_pla = geom.structure.Placement('psidebeam2_in_'+self.name, volume= side_lv, pos = Bot_pos,rot=rot)
        main_lv.placements.append(Bot_pla.name)






        #side-------------------












        #top platform ------------
        platx=Q('1500mm')
        platy=Q('15mm')
        platz=Q('1500mm')
        cylcutrad=Q('400mm')
        cylcut=geom.shapes.Tubs(None,Q('0mm'),cylcutrad,Q('1500mm'))
        top=geom.shapes.Box(None,platx,platy,platz)
        cut_pos= geom.structure.Position( None,Q('700mm'), Q('0mm'), Q('0mm'))
        rot = geom.structure.Rotation(None,x='90 deg')
        flatplat=geom.shapes.Boolean(None,'subtraction',top,cylcut,cut_pos,rot=rot)

        

        flatoverbeams_pos = geom.structure.Position(None, platx/2, Q('0mm'), Q('60mm'))

        platbeam=buildabeam(self,platz,self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],platz)
        beam1_pos= geom.structure.Position( None,Q('-600mm'), Q('0mm'), Q('0mm'))
        beam2_pos= geom.structure.Position( None,Q('-300mm'), Q('0mm'), Q('0mm'))
        beam3_pos= geom.structure.Position( None,Q('100mm'), Q('0mm'), Q('0mm'))
        beam4_pos= geom.structure.Position( None,Q('500mm'), Q('0mm'), Q('0mm'))
        beam5_pos= geom.structure.Position( None,Q('900mm'), Q('0mm'), Q('0mm'))
        beam6_pos= geom.structure.Position( None,Q('2000mm'), Q('0mm'), Q('0mm'))
        beam7_pos= geom.structure.Position( None,Q('2200mm'), Q('0mm'), Q('0mm'))
        U=geom.shapes.Boolean(None,'union',platbeam,platbeam,beam1_pos)
        U=geom.shapes.Boolean(None,'union',U,platbeam,beam2_pos)
        U=geom.shapes.Boolean(None,'union',U,platbeam,beam3_pos)
        U=geom.shapes.Boolean(None,'union',U,platbeam,beam4_pos)
        U=geom.shapes.Boolean(None,'union',U,platbeam,beam5_pos)
        U=geom.shapes.Boolean(None,'union',U,platbeam,beam6_pos)
        U=geom.shapes.Boolean(None,'union',U,platbeam,beam7_pos)
        U=geom.shapes.Boolean(None,'union',U,flatplat,flatoverbeams_pos,rot)

        top_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=U)
        Bot_pos = geom.structure.Position(None, Q('300mm'), Q('300mm'), Q('3000mm'))
        rot = geom.structure.Rotation(None,x='0 deg')

        Bot_pla = geom.structure.Placement(None, volume= top_lv, pos = Bot_pos,rot=rot)
        main_lv.placements.append(Bot_pla.name)




        #top platform ------------







        # cyl_1L_pos  = geom.structure.Position( 'cyl_1L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_1L_pla = geom.structure.Placement('pcyl_1L_in_'+self.name, volume= topcyl_lv, pos = cyl_1L_pos,rot=rot)
        # main_lv.placements.append(cyl_1L_pla.name)
        # cyl_2L_pos  = geom.structure.Position( 'cyl_2L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_2L_pla = geom.structure.Placement('pcyl_2L_in_'+self.name, volume= topcyl_lv, pos = cyl_2L_pos,rot=rot)
        # main_lv.placements.append(cyl_2L_pla.name)
        # cyl_3L_pos  = geom.structure.Position( 'cyl_3L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_3L_pla = geom.structure.Placement('pcyl_3L_in_'+self.name, volume= topcyl_lv, pos = cyl_3L_pos,rot=rot)
        # main_lv.placements.append(cyl_3L_pla.name)
        # cyl_4L_pos  = geom.structure.Position( 'cyl_4L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_4L_pla = geom.structure.Placement('pcyl_4L_in_'+self.name, volume= topcyl_lv, pos = cyl_4L_pos,rot=rot)
        # main_lv.placements.append(cyl_4L_pla.name)
        # cyl_5L_pos  = geom.structure.Position( 'cyl_5L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_5L_pla = geom.structure.Placement('pcyl_5L_in_'+self.name, volume= topcyl_lv, pos = cyl_5L_pos,rot=rot)
        # main_lv.placements.append(cyl_5L_pla.name)
        # cyl_6L_pos  = geom.structure.Position( 'cyl_6L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_6L_pla = geom.structure.Placement('pcyl_6L_in_'+self.name, volume= topcyl_lv, pos = cyl_6L_pos,rot=rot)
        # main_lv.placements.append(cyl_6L_pla.name)
        # cyl_7L_pos  = geom.structure.Position( 'cyl_7L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_7L_pla = geom.structure.Placement('pcyl_7L_in_'+self.name, volume= topcyl_lv, pos = cyl_7L_pos,rot=rot)
        # main_lv.placements.append(cyl_7L_pla.name)
        # cyl_8L_pos  = geom.structure.Position( 'cyl_8L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_8L_pla = geom.structure.Placement('pcyl_8L_in_'+self.name, volume= topcyl_lv, pos = cyl_8L_pos,rot=rot)
        # main_lv.placements.append(cyl_8L_pla.name)
        # cyl_9L_pos  = geom.structure.Position( 'cyl_9L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_9L_pla = geom.structure.Placement('pcyl_9L_in_'+self.name, volume= topcyl_lv, pos = cyl_9L_pos,rot=rot)
        # main_lv.placements.append(cyl_9L_pla.name)
        # cyl_10L_pos  = geom.structure.Position( 'cyl_10L_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        # cyl_10L_pla = geom.structure.Placement('pcyl_10L_in_'+self.name, volume= topcyl_lv, pos = cyl_10L_pos,rot=rot)
        # main_lv.placements.append(cyl_10L_pla.name)


        #??????? do again for the rhs 

        


        # rot = geom.structure.Rotation(None,z='90 deg')





        #cylinders--------------

        #support----------------


        #support----------------


        # T_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=T)

        # FC={'dx':Q('0mm')/2,'dy':Q('0mm')/2,'dz':Q('0mm')/2}

        # BL_pos=geom.structure.Position( 'BL_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.OuterBeam['dyb'],  FC['dz']+self.InnerBeam['dz']+self.OuterBeam['dz'])
        # BR_Pos
        # TL_pos
        # TR_pos

        # OTPL_pos  = geom.structure.Position( 'OTPL_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3)/2,self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'],  Q('0mm')) #outer, top (y), plus (z), left(x)


        # OBPL_pos  = geom.structure.Position( 'OBPL_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.OuterBeam['dyb'],  FC['dz']+self.InnerBeam['dz']+self.OuterBeam['dz'])
        # OBML_pos  = geom.structure.Position( 'OBML_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.OuterBeam['dyb'] ,  FC['dz']-self.InnerBeam['dz']-self.OuterBeam['dz'])
        # OBPR_pos  = geom.structure.Position( 'OBPR_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.OuterBeam['dyb'] ,  FC['dz']+self.InnerBeam['dz']+self.OuterBeam['dz'])
        # OBMR_pos  = geom.structure.Position( 'OBMR_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.OuterBeam['dyb'] ,  FC['dz']-self.InnerBeam['dz']-self.OuterBeam['dz'])
        # IBL_pos  = geom.structure.Position( 'IBL_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.InnerBeam['dyb'] ,  FC['dz'])
        # IBR_pos  = geom.structure.Position( 'IBR_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3), FC['dy']+self.InnerBeam['dyb'] ,  FC['dz'])

        # OTPL_pos  = geom.structure.Position( 'OTPL_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3)/2,FC['dy']+2*self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'],  FC['dz']+self.InnerBeam['dz']+self.OuterBeam['dz']) #outer, top (y), plus (z), left(x)
        # OTML_pos  = geom.structure.Position( 'OTML_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3)/2,FC['dy']+2*self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt']  ,  FC['dz']-self.InnerBeam['dz']-self.OuterBeam['dz'])
        # OTPR_pos  = geom.structure.Position( 'OTPR_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3)/2,FC['dy']+2*self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'] ,  FC['dz']+self.InnerBeam['dz']+self.OuterBeam['dz'])
        # OTMR_pos  = geom.structure.Position( 'OTMR_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3)/2,FC['dy']+2*self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'] ,  FC['dz']-self.InnerBeam['dz']-self.OuterBeam['dz'])
        # ITL_pos  = geom.structure.Position( 'ITL_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3)/2, FC['dy']+2*self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'] ,  FC['dz'])
        # ITR_pos  = geom.structure.Position( 'ITR_in_'+self.name,self.InnerBeam['dyt']*m.sqrt(3)/2,FC['dy']+2*self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt']  ,  FC['dz'])

        # print("inner beam", self.InnerBeam)

        # OBPL_pla = geom.structure.Placement('pOBPL_in_'+self.name, volume= OB_lv, pos = OBPL_pos)
        # OBML_pla = geom.structure.Placement('pOBML_in_'+self.name, volume= OB_lv, pos = OBML_pos)
        # OBPR_pla = geom.structure.Placement('pOBPR_in_'+self.name, volume= OB_lv, pos = OBPR_pos)
        # OBMR_pla = geom.structure.Placement('pOBMR_in_'+self.name, volume= OB_lv, pos = OBMR_pos)
        # IBL_pla = geom.structure.Placement('pIBL_in_'+self.name, volume= IB_lv, pos = IBL_pos)
        # IBR_pla = geom.structure.Placement('pIBR_in_'+self.name, volume= IB_lv, pos = IBR_pos)

        # rot = geom.structure.Rotation(None,z='60 deg')

        # OTPL_pla = geom.structure.Placement('pOTPL_in_'+self.name, volume= OT_lv, pos = OTPL_pos,rot=rot)
        # OTML_pla = geom.structure.Placement('pOTML_in_'+self.name, volume= OT_lv, pos = OTML_pos,rot=rot)
        # ITL_pla = geom.structure.Placement('pITL_in_'+self.name, volume= IT_lv, pos = ITL_pos,rot=rot)

        # rot = geom.structure.Rotation(None,z='-60 deg')

        # OTPR_pla = geom.structure.Placement('pOTPR_in_'+self.name, volume= OT_lv, pos = OTPR_pos,rot=rot)
        # OTMR_pla = geom.structure.Placement('pOTMR_in_'+self.name, volume= OT_lv, pos = OTMR_pos,rot=rot)
        # ITR_pla = geom.structure.Placement('pITR_in_'+self.name, volume= IT_lv, pos = ITR_pos,rot=rot)

        # main_lv.placements.append(OBPL_pla.name)
        # main_lv.placements.append(OBML_pla.name)
        # main_lv.placements.append(OBPR_pla.name)
        # main_lv.placements.append(OBMR_pla.name)
        # main_lv.placements.append(IBL_pla.name)
        # main_lv.placements.append(IBR_pla.name)

        # main_lv.placements.append(OTPL_pla.name)
        # main_lv.placements.append(OTML_pla.name)
        # main_lv.placements.append(OTPR_pla.name)
        # main_lv.placements.append(OTMR_pla.name)
        # main_lv.placements.append(ITL_pla.name)
        # main_lv.placements.append(ITR_pla.name)




        
        # pblock1_pla = geom.structure.Placement( 'pblock1_in_'+self.name,volume = block_lv, pos = block1_pos,rot=rot)



        # FBL= geom.shapes.Box(None, self.block['dx'], self.block['dy'],self.block['dz']) #Forward_Bottom_Left
        




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

        # block_shape= geom.shapes.Box(None, self.block['dx'], self.block['dy'],self.block['dz'])

        # block_lv = geom.structure.Volume(None, material='ReifConcrete', shape=block_shape)

        # block1_pos  = geom.structure.Position( 'block1_in_'+self.name,Q('0cm'),  Q('0cm'),  self.base-self.block['dz'])
        # pblock1_pla = geom.structure.Placement( 'pblock1_in_'+self.name,volume = block_lv, pos = block1_pos)

        # block2_pos  = geom.structure.Position( 'block2_in_'+self.name,Q('0cm'),  Q('0cm'),  -self.base+self.block['dz'])
        # pblock2_pla = geom.structure.Placement( 'pblock2_in_'+self.name,volume = block_lv, pos = block2_pos)

        # main_lv.placements.append( pblock1_pla.name )
        # main_lv.placements.append( pblock2_pla.name )

        # print("got here4")


# class BeamBuilder(gegede.builder.Builder):
#     def configure(self, midheight, midthick, lipsize, length,lipthick, **kwargs):
#         self.midheight=midheight
#         self.midthick=midthick
#         self.lipsize=lipsize
#         self.length=length
#         self.lipthick=lipthick
#         self.Material='Air'
#     def construct(self, geom):
#         self.halfDimension = {'dx':   self.lipthick*2/2+self.midheight/2,
#                               'dy':   self.length/2,
#                               'dz':   self.lipsize/2}
#         main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
#         print('DetectorBuilder::construct()')
#         print(('main_lv = '+main_lv.name))
#         self.add_volume(main_lv)
#         toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
#         botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
#         midpos = [Q('0cm'),Q('0cm'), Q('0cm')]

#         lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
#         midshape=geom.shapes.Box(None, self.midheight/2, self.length/2,self.midthick/2)

#         toplip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         botlip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)

#         toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
#         botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
#         mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])

#         toplip_pla = geom.structure.Placement(None,volume=toplip_lv, pos=toplip_pos)
#         botlip_pla = geom.structure.Placement(None,volume=botlip_lv, pos=botlip_pos)
#         mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)

#         main_lv.placements.append(toplip_pla.name)
#         main_lv.placements.append(botlip_pla.name)
#         main_lv.placements.append(mid_pla.name)


# class CrossBeamBuilder(gegede.builder.Builder):
#     def configure(self, midheight, midthick, lipsize, length,lipthick, **kwargs):
#         self.midheight=midheight
#         self.midthick=midthick
#         self.lipsize=lipsize
#         self.length=length
#         self.lipthick=lipthick
#         self.Material='Air'
#     def construct(self, geom):
#         self.halfDimension = {'dx':   self.lipthick*2/2+self.midheight/2,
#                               'dy':   self.length/2,
#                               'dz':   self.lipsize/2}
#         main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
#         print('DetectorBuilder::construct()')
#         print(('main_lv = '+main_lv.name))
#         self.add_volume(main_lv)
#         toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
#         botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
#         midpos = [Q('0cm'),Q('0cm'), Q('0cm')]
#         end1pos = [Q('0cm'), self.length/2-self.lipsize/2+self.midthick/2, Q('0cm')]
#         end2pos = [Q('0cm'), -self.length/2+self.lipsize/2-self.midthick/2, Q('0cm')]

#         lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
#         midshape=geom.shapes.Box(None, self.midheight/2, self.length/2-self.lipsize/2,self.midthick/2)
#         endshape=geom.shapes.Box(None, self.midheight/2, self.midthick/2,self.lipsize/2)

#         lip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)
#         end_lv = geom.structure.Volume(None, material='CarbonSteel', shape=endshape)

#         toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
#         botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
#         mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])
#         end1_pos=geom.structure.Position(None, x=end1pos[0], y=end1pos[1], z=end1pos[2])
#         end2_pos=geom.structure.Position(None, x=end2pos[0], y=end2pos[1], z=end2pos[2])

#         toplip_pla = geom.structure.Placement(None,volume=lip_lv, pos=toplip_pos)
#         botlip_pla = geom.structure.Placement(None,volume=lip_lv, pos=botlip_pos)
#         mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)
#         end1_pla = geom.structure.Placement(None, volume=end_lv, pos=end1_pos)
#         end2_pla = geom.structure.Placement(None, volume=end_lv, pos=end2_pos)

#         main_lv.placements.append(toplip_pla.name)
#         main_lv.placements.append(botlip_pla.name)
#         main_lv.placements.append(mid_pla.name)
#         main_lv.placements.append(end1_pla.name)
#         main_lv.placements.append(end2_pla.name)


# class SupportBuilder(gegede.builder.Builder):
#     def configure(self, midheight, midthick, lipsize, length,lipthick, **kwargs):
#         self.midheight=midheight
#         self.midthick=midthick
#         self.lipsize=lipsize
#         self.length=length
#         self.lipthick=lipthick
#         self.Material='Air'
#     def construct(self, geom):
#         self.halfDimension = {'dx':   self.lipthick*2/2+self.midheight/2,
#                               'dy':   self.length/2,
#                               'dz':   self.lipsize/2}
#         main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
#         print('DetectorBuilder::construct()')
#         print(('main_lv = '+main_lv.name))
#         self.add_volume(main_lv)
#         toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
#         botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
#         midpos = [Q('0cm'),Q('0cm'), Q('0cm')]

#         lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
#         midshape=geom.shapes.Box(None, self.midheight/2, self.length/2,self.midthick/2)

#         toplip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         botlip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)

#         toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
#         botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
#         mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])

#         toplip_pla = geom.structure.Placement(None,volume=toplip_lv, pos=toplip_pos)
#         botlip_pla = geom.structure.Placement(None,volume=botlip_lv, pos=botlip_pos)
#         mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)

#         main_lv.placements.append(toplip_pla.name)
#         main_lv.placements.append(botlip_pla.name)
#         main_lv.placements.append(mid_pla.name)

# class PLatformBuilder(gegede.builder.Builder):
#     def configure(self, midheight, midthick, lipsize, length,lipthick, **kwargs):
#         self.midheight=midheight
#         self.midthick=midthick
#         self.lipsize=lipsize
#         self.length=length
#         self.lipthick=lipthick
#         self.Material='Air'
#     def construct(self, geom):
#         self.halfDimension = {'dx':   self.lipthick*2/2+self.midheight/2,
#                               'dy':   self.length/2,
#                               'dz':   self.lipsize/2}
#         main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
#         print('DetectorBuilder::construct()')
#         print(('main_lv = '+main_lv.name))
#         self.add_volume(main_lv)
#         toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
#         botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
#         midpos = [Q('0cm'),Q('0cm'), Q('0cm')]

#         lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
#         midshape=geom.shapes.Box(None, self.midheight/2, self.length/2,self.midthick/2)

#         toplip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         botlip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
#         mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)

#         toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
#         botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
#         mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])

#         toplip_pla = geom.structure.Placement(None,volume=toplip_lv, pos=toplip_pos)
#         botlip_pla = geom.structure.Placement(None,volume=botlip_lv, pos=botlip_pos)
#         mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)

#         main_lv.placements.append(toplip_pla.name)
#         main_lv.placements.append(botlip_pla.name)
#         main_lv.placements.append(mid_pla.name)