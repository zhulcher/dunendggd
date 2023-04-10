#! /bin/bash


###FULL HALL
gegede-cli duneggd/Config/WORLD2x2ggd.cfg \
           duneggd/Config/2x2_Hall_Air.cfg \
           duneggd/Config/2x2_Hall_Rock.cfg \
           duneggd/Config/2x2_MINERVA.cfg \
           duneggd/Config/ArgonCube/Cryostat_2x2.cfg
           duneggd/Config/ArgonCube/ArgonCube_2x2.cfg \
           -w World -o 2x2.gdml