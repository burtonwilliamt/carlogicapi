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

        # if the next ID is the same as us, then we can platoon
        # nextType = traci.vehicle.getTypeID(//nextID)
        # if we are doing CarLogic, and the nextID is anythng but human, we can platoon

        laneIdStr, idInLaneStr= veh.split("_",1)
        laneId = int(laneIdStr)
        idInLane = -1
        if(idInLaneStr != "roadBlock"):
            idInLane = int(idInLaneStr)
        # print("ID: " + laneIdStr)
        typeID = traci.vehicle.getTypeID(veh)

        # carInFront = "none"
        # if(idInLane > 1):
        #     carInFront = laneId+"_"+idInLane-1

        pos = traci.vehicle.getPosition(veh)
        ang = traci.vehicle.getAngle(veh)
        speed = traci.vehicle.getSpeed(veh)
        edge = traci.vehicle.getRoadID(veh)
        stopState = traci.vehicle.getStopState(veh)
        isStoped = (stopState % 2 == 1)

        # print "Step: %04d | Position: (%03.3f, %03.3f) | Speed: %02.2f" % (step, pos[0], pos[1], speed)

        traci.vehicle.setLaneChangeMode(veh, 0)
        # if(laneId == 2):


        if(veh.endswith("roadBlock")):
            if(step == 20):
                # print "Slowing down"
                # stop_pos = (pos[0]+10, pos[1])
                trynastop = True
                traci.vehicle.setStop(veh, edge, pos[0]+50.0, laneId)

            if isStoped and step == 200:
                traci.vehicle.resume(veh)


    traci.simulationStep(.1)


    step += 1


traci.close()
