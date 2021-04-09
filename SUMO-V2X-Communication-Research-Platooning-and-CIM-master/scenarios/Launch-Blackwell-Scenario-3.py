import os
import sys
import traci
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.simulationmanager import SimulationManager
from src.simlib import setUpSimulation

setUpSimulation("../maps/BlackwellTunnelNorthApproach_no_TLS/BlackwellTunnelNorthApproach_no_TLS.sumocfg", 1)
step = 0
manager = SimulationManager(True, True, False)
while step < 5000:
    manager.handleSimulationStep()
    traci.simulationStep()
    step += 1

traci.close()
