#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import math as m

""" Hall_2x2_Air_Volume.py

Original Author: Z. Hulcher, SLAC

"""

class Hall2x2AirVolumeBuilder(gegede.builder.Builder):

    def configure(self, Hall=None, Entrance1=None, Entrance2=None, Entrance3=None,Position=None, Surroundings2x2_pos=None, **kwds):

        self.Position = Position
        self.Hall = Hall
        self.Entrance1=Entrance1
        self.Entrance2=Entrance2
        self.Entrance3=Entrance3
        self.Material='Rock'
        self.halfDimension={'dx':Q('60m')/2+Q('438in')/2,'dy':Q('60m')/2+Q('367in')/2,'dz':Q('165m')/2}
        # self.halfDimension={'dx':self.Hall['dx'],'dy':self.Hall['dy'],'dz':self.Hall['dz']}
        self.Surroundings2x2_Builder= self.get_builder('Surroundings2x2')
        self.Surroundings2x2_pos = Surroundings2x2_pos

    def construct(self, geom):

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        
        phi=self.Hall['phi']
       
        # main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        VolHall = geom.shapes.Box( 'HallVol',
                dx = self.Hall['dx'],
                dy = self.Hall['dy'],
                dz = self.Hall['dz'])
        
        
        
        roofdy=2*self.Hall['dy']-Q('98in')-Q('84in')

        Volextrawall=geom.shapes.Arb8( 'ExtraWallvol',
                v4x=Q("0in"),v4y=Q("0in"),
                v3x=Q("-5ft")/2,v3y=Q("0in"),
                v2x=Q("-5ft")/2,v2y=-roofdy/2,
                v1x=Q("0in"),v1y=(-roofdy-Q('84in'))/2,
                
                
                v8x=Q("0in"),v8y=Q("0in"),
                v7x=Q("-5ft")/2,v7y=Q("0in"),
                v6x=Q("-5ft")/2,v6y=-roofdy/2,
                v5x=Q("0in"),v5y=(-roofdy-Q('84in'))/2,
                dz = self.Hall['dz']/2)

        # VolSpace1 = geom.shapes.Trapezoid( 'Entrance1Vol',
        #         dx1 = self.Entrance1['dx1'],
        #         dx2 = self.Entrance1['dx2'],
        #         dy1 = self.Entrance1['dy1'],
        #         dy2 = self.Entrance1['dy2'],
        #         dz = self.Entrance1['dz'])
        # VolSpace1 = geom.shapes.Arb8( 'Entrance1Vol')
        VolSpace1 = geom.shapes.Arb8( 'Entrance1Vol',
        v4x=Q("0in"),v4y=Q("-1571in")/2,
        v3x=Q("0in"),v3y=Q("-1571in")/2,
        v2x=Q("346in")/2,v2y=Q("177in")/2,
        v1x=Q("0in"),v1y=Q("246in")/2,

        v8x=Q("0in"),v8y=Q("-1571in")/2,
        v7x=Q("0in"),v7y=Q("-1571in")/2,
        v6x=Q("346in")/2,v6y=Q("177in")/2,
        v5x=Q("0in"),v5y=Q("246in")/2,
        dz = self.Entrance1['dz'])
        
        VolSpace2 = geom.shapes.Box( 'Entrance2Vol',
                dx = self.Entrance2['dx'],
                dy = self.Entrance2['dy'],
                dz = self.Entrance2['dz'])
        
        vol3y=Q('237in')/2  # edited to match drawing from 115 to 237
        VolSpace3U = geom.shapes.Box( 'Entrance3Vol',
                dx = Q("353in"),
                dy=vol3y,
                dz = Q('114in')/2)
        

        
        # VolSpace4= geom.shapes.Box( 'Entrance4Vol',
        #         dx = Q("353in"),
        #         dy=Q('115in')/2,
        #         dz = Q('114in')/2)

        # phi=
        
        # x=(Q('114in')-Q('103in')*m.cos(phi))/m.sin(phi)

        # a = m.atan(x/Q('103in'))*Q('1 radian')

        a=(90-11.2)*m.pi/180


        # print("help me",a,y,x)

        volcut2=geom.shapes.Box( 'cut2Vol',
                dx = Q("353in")*m.sin(a),
                dy=vol3y,
                dz = Q('103in')+Q("353in")*m.cos(a))
        

        finalhalldx=Q("353in")/2-Q('114in')/2*m.cos(a)-Q('10in')
        
        cut2Pos = geom.structure.Position( 'cut2pos',
                Q('-353in'),
                Q('0in')-Q('0in'),# remove this second one ?????????,
                Q('-114in')/2) 

        finalhalldz=Q('1825in')/2

        finalhall = geom.shapes.Box( 'finalhall',
                dx = finalhalldx,
                dy=vol3y,
                dz = finalhalldz) 
        
        finalhallpos=geom.structure.Position( 'finalhall',
                -Q("353in")/2-Q('20in'),
                Q('0in'),
                finalhalldz+Q('114in')/2) 
        

        
        
        
        
        # HallPosition = geom.structure.Position( 'HallPosition',
        #         self.Position['dx'],Q("-1571in")/2
        #         self.Position['dy'],
        #         self.Position['dz'])
        

        Entrance1Pos = geom.structure.Position( 'Entrance1Pos',
                self.Hall['dx']-Q('5ft'),
                2*self.Entrance1['dz']-self.Hall['dy'],
                self.Hall['dz'])    
        
        Entrance2Pos = geom.structure.Position( 'Entrance2Pos',
                                                self.Hall['dx']-Q('5ft')-Q('346in')/2-Q('69in'),
                self.Entrance2['dy']-self.Hall['dy'],
            Q('246in')+self.Hall['dz']+Q('337in'))
        Entrance3Pos = geom.structure.Position( 'Entrance3Pos',
                self.Entrance2['dx'],
            vol3y-self.Entrance2['dy'],
                self.Entrance2['dz']+Q('114in')/2)  
        

        ExtraWallPos=  geom.structure.Position( 'Entrance1.5Pos',
                self.Hall['dx'],
                self.Hall['dy'],
                Q('0in')) 

        
        # shape4=geom.shapes.Box( 'shape4',
        #         dx = Q("353in")*m.sin(a),
        #         dy=vol3y,
        #         dz = Q('103in')+Q("353in")*m.cos(a))
        Pitlen = Q('30m')/2+Q('367in')/2
        PitBotlen=Q("330in")/2
        BottomlessPit=geom.shapes.Tubs("BottomlessPit",rmin=Q('0in'), rmax=Q("11ft"), dz=Pitlen)
        

        BottomlessPitBottom=geom.shapes.Tubs("BottomlessPitBottom",rmin=Q('0in'), rmax=Q("400in")/2, dz=PitBotlen)

        Pitpos= geom.structure.Position( 'PitPos',
                Q('0ft'),
                Q('0ft'),
                Pitlen-PitBotlen)  
        
        Pitpos2=geom.structure.Position( 'PitPos2',
                Q('0ft'),
                -vol3y+PitBotlen,
                finalhalldz)  

        Pit=geom.shapes.Boolean( 'Pit', type='union', first=BottomlessPitBottom, second=BottomlessPit, pos=Pitpos)

        

        subU = geom.shapes.Boolean( 'HallAirVolTemp3.5', type='intersection', first=VolSpace3U, second=volcut2, pos=cut2Pos,rot=geom.structure.Rotation(None, Q(' 0 deg'), phi, Q('0 deg')))

        pitplushall=geom.shapes.Boolean( 'Pitunion', type='union', first=finalhall, second=Pit, pos=Pitpos2,rot=geom.structure.Rotation(None, Q(' -90 deg'), Q(' 0 deg'), Q('0 deg')))

        subU=geom.shapes.Boolean( 'Pitunion2', type='union', first=subU, second=pitplushall, pos=finalhallpos,rot=geom.structure.Rotation(None, Q(' 0 deg'), Q(' 0 deg'), Q('0 deg')))

        U_shape = geom.shapes.Boolean( 'HallAirVolTemp4', type='union', first=VolSpace2, second=subU, pos=Entrance3Pos)

        Hall_shape = geom.shapes.Boolean( 'HallAirVolTemp.5', type='subtraction', first=VolHall, second=Volextrawall, pos=ExtraWallPos)

        Hall_shape = geom.shapes.Boolean('HallAirVolTemp1', type='union', first=Hall_shape, second=VolSpace1, pos=Entrance1Pos, rot=geom.structure.Rotation(None, Q('90 deg'), Q('0 deg'), Q('180 deg')))

        U_shape = geom.shapes.Boolean( 'HallAirVolTemp2', type='union', first=Hall_shape, second=U_shape, pos=Entrance2Pos,rot=geom.structure.Rotation(None, Q('0 deg'), Q('-11.2 deg'), Q('0 deg')))

        # U_shape = geom.shapes.Boolean( 'HallAirVolTemp3', type='union', first=U_shape, second=VolSpace3U, pos=Entrance3Pos,rot=geom.structure.Rotation(None, Q('0 deg'), Q('-11.2 deg'), Q('0 deg')))
        
        #
        Vol_lv = geom.structure.Volume( 'volMinosNDHall', material='Air', shape=U_shape)
        # self.add_volume(Vol_lv)

        Surroundings2x2_lv = self.Surroundings2x2_Builder.get_volume()
        pos = self.Surroundings2x2_pos

        ArgonCubeCryostat_pos = geom.structure.Position(self.Surroundings2x2_Builder.name+'_pos',
                                            pos['dx'],pos['dy'],pos['dz'])

        ArgonCubeCryostat_pla = geom.structure.Placement(self.Surroundings2x2_Builder.name+'_pla',
                                                volume=Surroundings2x2_lv,
                                                pos=ArgonCubeCryostat_pos,
                                                rot=geom.structure.Rotation(None,Q("0deg"),Q("180deg"),Q("0deg")))
        
        Vol_lv.placements.append(ArgonCubeCryostat_pla.name) ###???????put this back

        # self.add_volume(Vol_lv)
        
        self.add_volume( main_lv )
        HallPosition = geom.structure.Position( 'HallPosition',
                Q('0m'),
                Q('0m'),
                self.halfDimension['dz']-self.Hall['dz']-Q('10m'))
        VolPlace = geom.structure.Placement("HallAirVolPlace",volume=Vol_lv, pos=HallPosition,rot=geom.structure.Rotation(None,Q("0deg"),Q("180deg"),Q("0deg")))
        main_lv.placements.append( VolPlace.name)
        

        

        

        
        # self.add_volume( NDHallAirVol_lv )

        # for i,sb in enumerate(self.get_builders()):
        #     Pos = [Q("0m"),Q("0m"),Q("0m")]
        #     Rot = [Q("0deg"),Q("0deg"),Q("0deg")]
        #     if self.Positions!=None :
        #         Pos=self.Positions[i]
        #     if self.Positions!=None:
        #         Rot=self.Rotations[i]
        #     sb_lv = sb.get_volume()
        #     sb_pos = geom.structure.Position( sb_lv.name+'_pos', Pos[0], Pos[1], Pos[2] )
        #     sb_rot = geom.structure.Rotation( sb_lv.name+'_rot', Rot[0], Rot[1], Rot[2] )
        #     sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos, rot=sb_rot )
        #     NDHallAirVol_lv.placements.append( sb_pla.name )



