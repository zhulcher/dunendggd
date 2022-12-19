import configparser
import os
from gegede import Quantity as Q

def multigeo(multi,label):

	config = configparser.ConfigParser()
	config.optionxform = str
	config.read('duneggd/Config/ArgonCube/ArgonCubeDetector.cfg')

	cmulti=multi
	gmulti=multi

	fcdy=3026.394
	fcdz=990
	#g10dd=6.35

	#eval(config['HalfDetector']['Fieldcage_dimension'])['dd'].magnitude

	gmy=(fcdy-6.35*2*gmulti)/(fcdy-6.35*2)
	gmz=(fcdz-6.35*2*gmulti)/(fcdz-6.35*2)
	print(gmy,gmz)

	config['HalfDetector']['Cathode_dx']="Q('"+str(cmulti*6.35)+"mm')/2"

	config['HalfDetector']['Fieldcage_dimension']="{'dx':Q('952.12mm')/4,'dy':Q('3026.394mm')/2,'dz':Q('990mm')/2,'dd':Q('"+str(gmulti*6.35)+"mm')/2}"#'dx':Q('966.3mm')/4
	config['TPC']['Drift_Length']="Q('"+str(467.91-(cmulti-1)*6.35/2)+"mm')/2"#475.3
	

	config['ArCLight']['WLS_dimension']="{'dx':Q('"+str(464.215-4.5-1.738-(cmulti-1)*6.35/2)+"mm')/2,'dy':Q('"+str(299.599*gmy)+"mm')/2,'dz':Q('"+str(10*gmz)+"mm')/2,'tpb_dd':Q('"+str(.1*gmz)+"mm')/2,'dcm_dd':Q('"+str(.11*gmz)+"mm')/2}"
	
	config['ArCLight']['SiPM_dimension'] = "{'dx':Q('1.470mm')/2,'dy':Q('"+str(6.000*gmy)+"mm')/2,'dz':Q('"+str(6.000*gmz)+"mm')/2,'pitch':Q('"+str(47.000*gmy)+"mm')/2}"
	config['ArCLight']['SiPM_PCB'] = "{'dx':Q('3.000mm')/2,'dy':Q('"+str(299.599*gmy)+"mm')/3/2,'dz':Q('"+str(10*gmz)+"mm')/2,'pitch':Q('"+str(299.599*gmy)+"mm')/3/2}"
	config['PixelPlane']['PCB_dimension'] = "{'dx':Q('3.175mm')/2,'dy':Q('"+str(299.599*gmy)+"mm')/2,'dz':Q('"+str((478.318-.458)*gmz)+"mm')/2}"
	config['PixelPlane']['Asic_dimension'] = "{'dx':Q('1.422mm')/2,'dy':Q('"+str(16.000*gmy)+"mm')/2,'dz':Q('"+str(16.000*gmz)+"mm')/2}"#change this back 'dx':Q('1.422mm')/2
	config['ArCLight']['SiPM_Mask'] = "{'dx':Q('1.650mm')/2,'dy':Q('"+str(78.250*gmy)+"mm')/2,'dz':Q('"+str(10*gmz)+"mm')/2,'pitch':Q('"+str(299.599*gmy)+"mm')/3/2}"
	

	#config['HalfDetector']['Bracket_dimension'] = "{'dx':Q('"+str(multi*6.35)+"mm')/2, 'dy':Q('3000mm')/2, 'dz':Q('15.24mm')}"

	#understand input events do hiro’s list 
	#active vs total 2d plot 

	#verify cuts y from -220 to 220+314.5=94.5
	#sanity check 
	#gps with muon 


	#put total number of events in each plot 

	with open('duneggd/Config/ArgonCube/ArgonCubeDetector.cfg', 'w') as configfile:config.write(configfile)
	print(label+"multiplication factor of "+str(multi))
	os.system("gegede-cli duneggd/Config/WORLDggd.cfg \
		duneggd/Config/ND_Hall_Rock.cfg \
		duneggd/Config/ND_ElevatorStruct.cfg \
		duneggd/Config/ND_Hall_Air_Volume_Only_LAr.cfg \
		duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
		duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
		duneggd/Config/ND_CraneRailStruct1.cfg \
		duneggd/Config/ND_CraneRailStruct2.cfg \
		duneggd/Config/ND_HallwayStruct.cfg \
		duneggd/Config/ND_CryoStruct.cfg \
	   -w World -o nd_hall_only_lar_fixed_"+label+"_"+str(multi)+".gdml")

	#  duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \   
	   #duneggd/Config/SAND_ECAl.cfg \
	   #duneggd/Config/KLOE_with_3DST.cfg \

def sensdetLIE():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read('duneggd/Config/ArgonCube/ArgonCubeDetector.cfg')
	config['NDBucket']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['ArCLight']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['PixelPlane']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['TPCPlane']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['OpticalDet']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['TPC']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['HalfDetector']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['InnerDetector']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	config['ArgonCubeDetector75']['AuxParams'] = '{"SensDet":"TPCActive_shape"}'
	with open('duneggd/Config/ArgonCube/ArgonCubeDetector.cfg', 'w') as configfile: config.write(configfile)

def sensdetTRUE():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read('duneggd/Config/ArgonCube/ArgonCubeDetector.cfg')
	config.remove_option('NDBucket', 'AuxParams')
	config.remove_option('ArCLight', 'AuxParams')
	config.remove_option('PixelPlane', 'AuxParams')
	config.remove_option('TPCPlane', 'AuxParams')
	config.remove_option('OpticalDet', 'AuxParams')
	config.remove_option('TPC', 'AuxParams')
	config.remove_option('HalfDetector', 'AuxParams')
	config.remove_option('InnerDetector', 'AuxParams')
	config.remove_option('ArgonCubeDetector75', 'AuxParams')
	with open('duneggd/Config/ArgonCube/ArgonCubeDetector.cfg', 'w') as configfile: config.write(configfile)

def removemuonsens():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read('duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg')
	config.remove_option('MuonTaggerPlane', 'AuxParams')
	with open('duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg', 'w') as configfile: config.write(configfile)
def putbackmuonsens():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read('duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg')
	config['MuonTaggerPlane']['AuxParams'] = '{"SensDet":"muTag"}'
	with open('duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg', 'w') as configfile: config.write(configfile)

#for i in [.75,.1,.5,2,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,1]:

os.system("gegede-cli duneggd/Config/WORLDofArgonggd.cfg -w World -o SeaOfArgon.gdml")
exit()
for i in [1]:
	removemuonsens()
	sensdetLIE()
	multigeo(i,"LIE")
	sensdetTRUE()
	multigeo(i,"TRUE")
	#os.chdir("/dune/app/users/zhulcher/nd_sim/dggd2to3_scaled_output")
	#os.system("source neutgen.sh FHC 1000 0 skip nd_hall_with_dets"+str(i*1000))
	#os.chdir("/dune/app/users/zhulcher/nd_sim/dunendggd-2to3")
	putbackmuonsens()
	#multigeo(1,"TRUEmuontest")
	

print("done")

#root -l 'geoDisplay.C("nd_hall_only_lar_fixed_TRUE_1.gdml")'