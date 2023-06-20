#! /bin/bash


###FULL HALL
# gegede-cli duneggd/Config/WORLD2x2ggd.cfg \
#            duneggd/Config/2x2_Hall_Air.cfg \
#            duneggd/Config/2x2_Hall_Rock.cfg \
#            duneggd/Config/2x2_MINERVA.cfg \
#            duneggd/Config/ArgonCube/Cryostat_2x2.cfg
#            duneggd/Config/ArgonCube/ArgonCube_2x2.cfg \
#            -w World -o 2x2.gdml

python setup.py develop --user
gegede-cli duneggd/Config/WORLDtest.cfg \
           duneggd/Config/ArgonCube/Hall_2x2.cfg \
           duneggd/Config/ArgonCube/ArgonCube_2x2.cfg \
           duneggd/Config/ArgonCube/Cryostat_2x2.cfg -w World -o test.gdml
#python3 pyg4_mod_and_add.py
root -l 'geoDisplay.C("test.gdml")'
#root -l 'checkOverlaps.C("test.gdml")'
#

# gegede-cli duneggd/Config/WORLD2x2ggd.cfg \
#            duneggd/Config/2x2_Hall_Air.cfg \
#            duneggd/Config/2x2_Hall_Rock.cfg \
#            duneggd/Config/2x2_MINERVA.cfg \
#            duneggd/Config/ArgonCube/Cryostat_2x2.cfg
#            duneggd/Config/ArgonCube/ArgonCube_2x2.cfg \
#            -w World -o 2x2.gdml