import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class DRIFTBuilder(gegede.builder.Builder):

    def configure(self, 
                # sand inner volume info
                configuration = None,tracker_configuration=None, nBarrelModules = None, halfDimension = None, Material = None, GRAINThickness = None, 
                clearenceECALGRAIN = None, clearenceGRAINTracker = None, clearenceTrackerECAL = None, clearenceSupermods = None,
                # tracker
                nofUpstreamTrkMod = None, nofDownstreamTrkMod = None, nofC3H6ModAfterCMod = None,
                # tracker module
                frameThickness = None, frameMaterial = None, targetThickness = None, MylarThickness = None, NofDriftModules = None, DriftModulesWireAngles = None, DriftChamberGas = None, DriftModuleThickness = None,
                # module wire
                FieldWireRadius = None, SignalWireRadius = None, WireMaterial = None, WireAngle = None, WireWireDistance = None,
                **kwds):

            # sand inner volume info
            self.configuration              = configuration
            self.tracker_configuration      = tracker_configuration
            self.nBarrelModules             = nBarrelModules
            self.rotAngle                   = 0.5 * Q('360deg') / self.nBarrelModules
            self.halfDimension, self.Material = ( halfDimension, Material )
            self.kloeVesselRadius           = self.halfDimension['rmax'] #= Q('2m')
            self.kloeVesselHalfDx           = self.halfDimension['dz'] #= Q('1.69m')
            self.GRAINThickness             = GRAINThickness
            self.clearenceECALGRAIN         = clearenceECALGRAIN
            self.clearenceGRAINTracker      = clearenceGRAINTracker
            self.clearenceTrackerECAL       = clearenceTrackerECAL
            self.clearenceSupermods         = clearenceSupermods

            # tracker
            self.nofUpstreamTrkMod          = nofUpstreamTrkMod
            self.nofDownstreamTrkMod        = nofDownstreamTrkMod
            self.nofC3H6ModAfterCMod        = nofC3H6ModAfterCMod

            # tracker module
            self.frameThickness             = frameThickness
            self.frameMaterial              = frameMaterial
            self.targetThickness            = targetThickness
            self.MylarThickness             = MylarThickness
            self.NofDriftModules            = NofDriftModules
            self.DriftModulesWireAngles     = DriftModulesWireAngles
            self.DriftChamberGas            = DriftChamberGas
            self.DriftModuleThickness       = DriftModuleThickness

            # module wire
            self.FieldWireRadius            = FieldWireRadius
            self.SignalWireRadius           = SignalWireRadius
            self.WireMaterial               = WireMaterial
            self.WireAngle                  = WireAngle
            self.WireWireDistance           = WireWireDistance

    def init(self):

            self.GetModThickness            = lambda mod_type : self.targetThickness[mod_type] + self.NofDriftModules * self.DriftModuleThickness + (self.NofDriftModules + 1) * self.MylarThickness

            self.ModThickness               = {"CMod" : self.GetModThickness("CMod"), "C3H6Mod" : self.GetModThickness("C3H6Mod"), "TrkMod" : self.GetModThickness("TrkMod")}

            self.SuperModThickness          = self.ModThickness["CMod"] + self.ModThickness["C3H6Mod"] * self.nofC3H6ModAfterCMod + self.clearenceSupermods 

            # upstream

            self.UpstreamSpace4Tracker      = self.kloeVesselRadius - self.GRAINThickness - self.clearenceECALGRAIN - self.clearenceGRAINTracker

            self.UpstreamSpace4SuperMod     = self.UpstreamSpace4Tracker - self.nofUpstreamTrkMod * self.ModThickness["TrkMod"] 

            self.nofUpstreamSuperMod        = int( (self.UpstreamSpace4SuperMod / self.SuperModThickness).to_base_units().magnitude )

            self.UpstreamSpaceLeft          = self.UpstreamSpace4Tracker - self.SuperModThickness * self.nofUpstreamSuperMod - self.ModThickness["TrkMod"] * self.nofUpstreamTrkMod

            self.clearenceGRAINTracker     += self.UpstreamSpaceLeft

            # downstream

            self.DownstreamSpace4Tracker    = self.kloeVesselRadius - self.clearenceTrackerECAL

            self.DownstreamSpace4ExtraMods  = self.DownstreamSpace4Tracker - self.SuperModThickness * self.nofUpstreamSuperMod - self.ModThickness["TrkMod"] * self.nofDownstreamTrkMod 

            self.nofExtraMods               = 1

            self.ExtraModThickness          = self.DownstreamSpace4ExtraMods / self.nofExtraMods    

            self.nofC3H6ModInExtraMod       = int(((self.ExtraModThickness - self.clearenceSupermods - self.ModThickness["CMod"])/self.ModThickness["C3H6Mod"]).magnitude)
            
            # 
            
            self.TrackerThickness           = self.SuperModThickness * self.nofUpstreamSuperMod * 2 + self.ExtraModThickness * self.nofExtraMods + (self.nofUpstreamTrkMod + self.nofDownstreamTrkMod) * self.ModThickness["TrkMod"]

            self.PrintRecap()

    def PrintRecap(self):   

            print("")
            print("*"*20 + f" INNERVOLUME CONFIGURATION {self.configuration}" +" "+"*"*20)
            print("*"*20 + f" TRACKER CONFIGURATION {self.tracker_configuration}" +" "+"*"*20)
            print("")
            print("_"*20+" INNERVOLUME INFO "+"_"*20)
            print("")
            print("GRAINThickness                 | "+str(self.GRAINThickness))
            print("clearance GRAIN-ECAL           | "+str(self.clearenceECALGRAIN))
            print("clearance GRAIN-tracker        | "+str(self.clearenceGRAINTracker))
            print("clearance tracker-ECAL         | "+str(self.clearenceTrackerECAL))
            print("")
            print("_"*20+" MODULE INFO "+"_"*20)
            print("")
            print("trkMod       Thickness         | "+str(self.ModThickness["TrkMod"]))
            print("C3H6Mod      Thickness         | "+str(self.ModThickness["C3H6Mod"]))
            print("CMod         Thickness         | "+str(self.ModThickness["CMod"]))
            print("SuperMod     Thickness         | "+str(self.SuperModThickness))
            print("ExtramMod    Thickness         | "+str(self.ExtraModThickness))
            print("Tracker      Thickness         | "+str(self.TrackerThickness))
            print("")
            print("")
            print(f"nof upstream tracking modules  | {self.nofUpstreamTrkMod}")
            print(f"nof dwstream tracking modules  | {self.nofDownstreamTrkMod}")
            print(f"nof supermodules               | {self.nofUpstreamSuperMod * 2}")
            print(f"nof C3H6Mod in dw extra modules| {self.nofC3H6ModInExtraMod}")
            print(f"nof downstram extramods        | {self.nofExtraMods}")
            print("")
            print("_"*20+" MODULE INFO "+"_"*20)

    
    def construct(self, geom):

        self.init()

        main_lv = self.constructTracker(geom)
    
        self.add_volume( main_lv )

    def constructTracker(self, geom):

        whole_shape         = geom.shapes.PolyhedraRegular("whole_shape_for_tracker", numsides = self.nBarrelModules, rmin = Q('0cm'), rmax = self.kloeVesselRadius , dz = self.kloeVesselHalfDx, sphi = self.rotAngle)
        
        upstream_shape      = geom.shapes.Box("upstream_shape_for_tracker", dx = (self.GRAINThickness + self.clearenceECALGRAIN + self.clearenceGRAINTracker)*0.5, dy = self.kloeVesselRadius, dz = self.kloeVesselHalfDx )
        
        upstream_shape_pos  = geom.structure.Position("upstream_shape_pos_for_tracker", - self.kloeVesselRadius + 0.5 * self.GRAINThickness + self.clearenceECALGRAIN, Q('0m'), Q('0m'))
        
        tracker_shape       = geom.shapes.Boolean("tracker_shape", type='subtraction', first = whole_shape, second = upstream_shape, rot='noRotate', pos=upstream_shape_pos)
        
        main_lv             = geom.structure.Volume('SANDtracker',   material=self.Material, shape=tracker_shape)
        
        print(( "main_lv = "+ main_lv.name))
        
        self.fillTracker(geom, main_lv)
        
        return main_lv
    
    def fillTracker(self, geom, volume):
    
        self.costructSymSuperMod(geom, volume)
        
        # self.constructExtraMod(geom, volume)

        # self.constructTrackingMod(geom, volume)
    
    # def constructExtraMod(self, geom, volume):
         
    #      running_x = self.SuperModThickness * self.nofUpstreamSuperMod + self.ExtraModThickness
         
    #      for i in range(self.nofExtraMods):
              
    #           extraMod_lv = self.constructXMod(geom, running_x, label = str(i))

    #           self.placeSubVolume(volume, extraMod_lv, pos_x=running_x +  self.ExtraModThickness/2, label = str(i))

    #           running_x += self.ExtraModThickness

    
    def costructSymSuperMod(self, geom, volume):
        
        running_x = - self.SuperModThickness
    
        for i in range(self.nofUpstreamSuperMod):
            
            SuperMod_lv = self.constructSuperMod(geom, running_x, label = str(i))

            print("")
            print(f"SuperMod {i} built")
            print("")
            
            self.placeSubVolume(geom, volume, SuperMod_lv, pos_x = running_x + self.SuperModThickness/2, label = str(i)+"up")

            print(f"placing SuperMod {i} up")
            
            self.placeSubVolume(geom, volume, SuperMod_lv, pos_x = - (running_x + self.SuperModThickness/2), label = str(i)+"dw")
    
            print(f"placing SuperMod {i} dw")
            
            running_x -= self.SuperModThickness

    def constructSuperMod(self, geom, running_x, half_thickness = None, half_length = None, nofC3H6 = None, name = "SuperMod", label = ""):
        # build SuperMod main shape

        if half_thickness == None : half_thickness = self.SuperModThickness/2
        if half_length    == None : half_length    = self.kloeVesselHalfDx/2
        if nofC3H6        == None : half_length    = self.nofC3H6ModAfterCMod/2
        
        half_heigth    = self.getHalfHeight(abs(running_x))
        
        SuperMod_name  = name + label
        
        SuperMod_lv    = self.constructBox(geom, SuperMod_name, half_thickness, half_heigth, half_length)
    
        # build SuperMod subvolumes : CMod, C3H6Mod, Frame

        frame_lv       = self.constructFrame(geom, half_heigth, label = SuperMod_name)
        
        CMod_lv        = self.constructMod(geom, "C", half_heigth - self.frameThickness, label = SuperMod_name)
        
        C3H6Mod_lv     = self.constructMod(geom, "C3H6", half_heigth - self.frameThickness, label = SuperMod_name)
        
        # place subvolumes in SuperMod

        self.placeSubVolume(geom, SuperMod_lv, frame_lv)
        
        self.placeSubVolume(geom, SuperMod_lv, CMod_lv, pos_x = - half_thickness/2 + self.ModThickness["CMod"]/2)
        
        for i in range(nofC3H6):
        
            pos_x =  - half_thickness/2 + self.ModThickness["CMod"] + self.ModThickness["C3H6Mod"] * (0.5 + i)
        
            self.placeSubVolume(geom, SuperMod_lv, C3H6Mod_lv, pos_x = pos_x, label=str(i))
        
        return SuperMod_lv
    
    
    def constructFrame(self, geom, half_heigth, label = ""):

        name = "frame"+label
        
        outer_box  = geom.shapes.Box(name+"_out_shape", dx = self.SuperModThickness/2, dy = half_heigth, dz = self.kloeVesselHalfDx)
        
        inner_box  = geom.shapes.Box(name+"_in_shape", dx = self.SuperModThickness/2, dy = half_heigth - self.frameThickness, dz = self.kloeVesselHalfDx - self.frameThickness)
        
        shape      = geom.shapes.Boolean(name+"_shape", type = "subtraction", first = outer_box, second = inner_box, rot='noRotate')
        
        frame_lv   = geom.structure.Volume(name, material = self.frameMaterial, shape = shape) 
        
        return frame_lv
 
    def constructMod(self, geom, target_type, half_heigth, label = ""):
        
        half_thickness, half_length = self.ModThickness[target_type+"Mod"]/2, self.kloeVesselHalfDx - self.frameThickness

        drift_chamber_thickness     = self.NofDriftModules * self.DriftModuleThickness + (self.NofDriftModules + 1) * self.MylarThickness

        name = target_type+label

        mod_lv                      = self.constructBox(geom, name+"Mod", half_thickness, half_heigth, half_length)

        target_lv                   = self.constructBox(geom, name+"target", self.targetThickness[target_type+"Mod"]/2, half_heigth, half_length)

        DriftChamber_lv             = self.constructBox(geom, name+"drift_chamber", drift_chamber_thickness/2, half_heigth, half_length)

        # self.fillDriftChamber()

        self.placeSubVolume(geom, mod_lv, target_lv, pos_x = - half_thickness + self.targetThickness[target_type+"Mod"]/2)

        self.placeSubVolume(geom, mod_lv, DriftChamber_lv, pos_x = - half_thickness + self.targetThickness[target_type+"Mod"] + drift_chamber_thickness/2)
    
        return mod_lv

     
    def constructBox(self, geom, name, half_thickness, half_heigth, half_length, material="Air35C"):
        
        box_shape = geom.shapes.Box(name+"_shape", dx = half_thickness, dy = half_heigth, dz = half_length)
        box       = geom.structure.Volume(name, material = material, shape = box_shape)
        return box
        

    def placeSubVolume(self, geom, volume, subvolume, pos_x=Q("0mm"), pos_y=Q("0mm"), pos_z=Q("0mm"), rot_x=Q("0deg"), rot_y=Q("0deg"), rot_z=Q("0deg"), label=""):

        name     = subvolume.name + label
        position = geom.structure.Position(name + "_pos", pos_x, pos_y, pos_z)
        rotation = geom.structure.Rotation(name + "_rot", rot_x, rot_y, rot_z)
        place    = geom.structure.Placement(name + "_place", volume = subvolume.name, pos = position.name, rot = rotation.name)
        
        volume.placements.append(place.name)

    
    def getHalfHeight(self,dis2c):

        theta   = math.pi*2/self.nBarrelModules
        d       = self.kloeVesselRadius*math.tan(theta/2)
        if dis2c<d:
            return self.kloeVesselRadius
        projectedDis=d
        HalfHeight=self.kloeVesselRadius

        for i in range(1,int(self.nBarrelModules/4)):
            projectedDisPre=projectedDis
            projectedDis+=2*d*math.cos(i*theta)
            if dis2c<projectedDis:
                return HalfHeight-(dis2c-projectedDisPre)*math.tan(i*theta)
            else:
                HalfHeight-=2*d*math.sin(i*theta)