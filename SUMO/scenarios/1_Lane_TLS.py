import os
import sys
import traci
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from SUMO.src.simlib import setUpSimulation

setUpSimulation("../maps/1_Lane/1_Lane_TLS.sumocfg",3)
step = 0
while step < 5000:
    traci.simulationStep()
    step += 1

traci.close()
