#!/usr/bin/env python
""" MINERVA.py

Original Author: Z. Hulcher, SLAC

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import math as m

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


        def buildabeam(L,lipthick,middlethick,lipwidth,middlewidth,lipL,lipoffset=Q('0mm')):
            
            lipbox=geom.shapes.Box(None, lipwidth, lipL, lipthick)
            middlebox=geom.shapes.Box(None, middlethick, L, middlewidth)
            lip1_pos=geom.structure.Position( None,Q('0mm'), lipoffset, middlewidth+lipthick)
            lip2_pos=geom.structure.Position( None,Q('0mm'), lipoffset, -middlewidth-lipthick)
            beamtemp=geom.shapes.Boolean(None,'union',middlebox,lipbox,lip1_pos)
            return geom.shapes.Boolean(None,'union',beamtemp,lipbox,lip2_pos)
            
            



       

        lipP_pos  = geom.structure.Position( 'botlipP_in_'+self.name,Q('0mm'), Q('0mm'), self.InnerBeam['dz']+self.OuterBeam['dz'])
        lipM_pos  = geom.structure.Position( 'botlipM_in_'+self.name,Q('0mm'), Q('0mm'), -self.InnerBeam['dz']-self.OuterBeam['dz'])
        # I_pos  = geom.structure.Position( 'IB_in_'+self.name,Q('0mm'), Q('0mm') ,  self.InnerBeam['dz']+self.OuterBeam['dz'])

        # Btemp=geom.shapes.Boolean('MINERVABtemp','union',IB,OB,OP_pos)
        # B=geom.shapes.Boolean('MINERVAB','union',Btemp,OB,OM_pos)

        B=buildabeam(self.InnerBeam['dyb'],self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],self.OuterBeam['dyb'],-self.InnerBeam['dyb']+self.OuterBeam['dyb'])
        T=buildabeam(self.InnerBeam['dyt'],self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],self.OuterBeam['dyt'])

        # Ttemp=geom.shapes.Boolean('MINERVATtemp','union',IT,OT,lipP_pos)
        # T=geom.shapes.Boolean('MINERVAT','union',Ttemp,OT,lipM_pos)

        L_pos=geom.structure.Position( 'L_in_'+self.name,-self.InnerBeam['dyt']*m.sqrt(3)/2,  self.InnerBeam['dyb']+1/2*self.InnerBeam['dyt'], Q('0mm'))

        rot = geom.structure.Rotation(None,z='60 deg')
        L=geom.shapes.Boolean(None,'union',B,T,L_pos,rot)

        rot=geom.structure.Rotation(None,y='180 deg')

        R_pos=geom.structure.Position( 'R_in_'+self.name,-4*self.InnerBeam['dyt']*m.sqrt(3)/2,Q('0mm'),  Q('0mm'))

        Msupp=geom.shapes.Boolean(None,'union',L,L,R_pos,rot)


        Msupp_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=Msupp)
        Msupp_pos=geom.structure.Position( 'Msupp_in_'+self.name,2*self.InnerBeam['dyt']*m.sqrt(3)/2, Q('0mm'),  Q('0mm'))
        Msupp_pla = geom.structure.Placement('pMsupp_in_'+self.name, volume= Msupp_lv, pos = Msupp_pos)
        main_lv.placements.append(Msupp_pla.name)



        botlen=self.OuterBeam['dyt']*m.sqrt(3)

        Obot = geom.shapes.Box(None, self.OuterBeam['dx'], botlen, self.OuterBeam['dz'])
        Ibot = geom.shapes.Box(None, self.InnerBeam['dx'], botlen, self.InnerBeam['dz'])


        Bottemp=geom.shapes.Boolean(None,'union',Ibot,Obot,lipP_pos)
        Bot=geom.shapes.Boolean(None,'union',Bottemp,Obot,lipM_pos)

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
        cylsup=geom.shapes.Boolean(None,'subtraction',cylsupO,cylsupI)
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
        supbox=geom.shapes.Boolean(None,'union',supboxB,supboxT,pos=BoverT)
        suppill=geom.shapes.Boolean(None,'union',supbox,supboxT,pos=BoverT)

        suppillh=Q('1500mm')

        sidelen = Q('1200mm')


        sbi=buildabeam(suppillh,self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],suppillh)
        self.sbiheight = suppillh + Q('19mm')/2
        sbibase_pos=geom.structure.Position('sbibase_in_sbi_in_'+self.name, Q('0mm'), -suppillh, Q('0mm'))

        sidebeam=geom.shapes.Boolean(None,'union',sbi,suppill,sbibase_pos)
        sbi_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=sidebeam)

        sbi1_pos = geom.structure.Position('sbi1_in_'+self.name, 2*self.InnerBeam['dyt']*m.sqrt(3)/2, botBpos[1],-4*self.OuterBeam['dz']-2*self.InnerBeam['dz'])
        self.sbi1_pos = sbi1_pos
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

        scOdx=Q('100mm')
        scIdx=Q('90mm')
        sidecrossO=geom.shapes.Box(None,suplen/2,scOdx,scOdx)
        sidecrossI=geom.shapes.Box(None,suplen/2,scIdx,scIdx)
        sidecross=geom.shapes.Boolean(None,'subtraction',sidecrossO,sidecrossI)

        #boolean subtract two blocks 
        cylsup_lv=geom.structure.Volume(None, material=self.BeamMaterial, shape=cylsup)




        
        # suppheight=



        # Oside = geom.shapes.Box(None, self.OuterBeam['dx'], sidelen, self.OuterBeam['dz'])
        # Iside = geom.shapes.Box(None, self.InnerBeam['dx'], sidelen, self.InnerBeam['dz'])

        # sidetemp=geom.shapes.Boolean(None,'union',Iside,Oside,OP_pos)
        # side=geom.shapes.Boolean('sidebeam','union',sidetemp,Oside,OM_pos)

        side=buildabeam(sidelen,self.OuterBeam['dz'],self.InnerBeam['dx'],self.OuterBeam['dx'],self.InnerBeam['dz'],sidelen)

        
        botbeamheight=Q('-1500mm')#?????????????????????????????/
        side_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=side)
        Bot_pos = geom.structure.Position('sidebeam1_in_'+self.name, -2*self.InnerBeam['dyt']*m.sqrt(3)/2, Q('1500mm')+botBpos[1]+self.OuterBeam['dz']+self.OuterBeam['dx'], -2*self.OuterBeam['dz']-self.InnerBeam['dz']-sidelen)
        rot = geom.structure.Rotation(None,x='90 deg')
        Bot_pla = geom.structure.Placement('psidebeam1_in_'+self.name, volume= side_lv, pos = Bot_pos,rot=rot)
        main_lv.placements.append(Bot_pla.name)

        botbeamheight=Q('-1500mm')#?????????????????????????????/
        side_lv = geom.structure.Volume(None, material=self.BeamMaterial, shape=side)
        Bot_pos = geom.structure.Position('sidebeam2_in_'+self.name, 2*self.InnerBeam['dyt']*m.sqrt(3)/2, Q('1500mm')+botBpos[1]+self.OuterBeam['dz']+self.OuterBeam['dx'], -2*self.OuterBeam['dz']-self.InnerBeam['dz']-sidelen)
        rot = geom.structure.Rotation(None,x='90 deg')
        Bot_pla = geom.structure.Placement('psidebeam2_in_'+self.name, volume= side_lv, pos = Bot_pos,rot=rot)
        main_lv.placements.append(Bot_pla.name)
