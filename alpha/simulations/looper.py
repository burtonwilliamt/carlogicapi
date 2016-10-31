import os, sys
# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import subprocess
PORT = 8813
sumoBinary = checkBinary('sumo-gui')
print sumoBinary
sumoProcess = subprocess.Popen([sumoBinary, "-c", "alpha.sumo.cfg", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

import traci
traci.init(PORT)
step = 0
while step < 1000:
    traci.simulationStep(.1)
    pos = traci.vehicle.getPosition("veh0")
    ang = traci.vehicle.getAngle("veh0")
    speed = traci.vehicle.getSpeed("veh0")
    print "Step: %04d | Position: (%03.3f, %03.3f) | Speed: %02.2f" % (step, pos[0], pos[1], speed)
    if speed >= 5:
        print "Slowing down"
        traci.vehicle.slowDown("veh0", 0, 3000)
    if(speed < .01):
        print "I have stopped"
    step += 1

traci.close()
