import os
import sys
import traci
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from SUMO.src.simulationmanager import SimulationManager
from SUMO.src.simlib import setUpSimulation

setUpSimulation("../maps/NormalIntersection_no_TLS/NormalIntersection_no_TLS3.sumocfg",3)
step = 0
manager = SimulationManager()
while step < 5000:
    manager.handleSimulationStep()
    traci.simulationStep()
    step += 1

traci.close()
