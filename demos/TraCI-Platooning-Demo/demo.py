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
sumoProcess = subprocess.Popen([sumoBinary, "-c", "demo.sumo.cfg", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

import traci
traci.init(PORT)
step = 0
trynastop = False
while step < 1000:
    idList = traci.vehicle.getIDList()
    # print "ID List: ", idList
    for veh in idList:
        traci.vehicle.setLaneChangeMode(veh, 0)
        # if the next ID is the same as us, then we can platoon
        # nextType = traci.vehicle.getTypeID(//nextID)
        # if we are doing CarLogic, and the nextID is anythng but human, we can platoon

    traci.simulationStep(.1)
    pos = traci.vehicle.getPosition("veh0")
    ang = traci.vehicle.getAngle("veh0")
    speed = traci.vehicle.getSpeed("veh0")
    edge = traci.vehicle.getRoadID("veh0")
    stopState = traci.vehicle.getStopState("veh0")
    #print "Stop state: ", stopState
    isStoped = (stopState % 2 == 1)
    print "Step: %04d | Position: (%03.3f, %03.3f) | Speed: %02.2f" % (step, pos[0], pos[1], speed)
    if speed >= 2 and not trynastop:
        print "Slowing down"
        # stop_pos = (pos[0]+10, pos[1])
        trynastop = True
        traci.vehicle.setStop("veh0", edge, pos[0]+20.0)
    if(isStoped):
        print "I am stopped"


    if(speed < .01):
        print "I no speed"

    if isStoped and step == 150:
        traci.vehicle.resume("veh0")

    step += 1


traci.close()
