## Tutorial using Simple Veins Example

I've made a simplified example project in order to make it easier to learn Veins, since the example included with Veins doesn't include any documentation and can be hard to understand.

[Veins](http://veins.car2x.org/) is the project that we use to build and run a simulation of communinicating cars. Veins itself is an open source project that connects two open source simulators: OMNeT++ for network traffic, and SUMO for vehicle traffic. Writing a Veins project involves knowledge of all three systems. SUMO provides an API for getting and setting information about the cars in it's simulation, called TraCI. Veins will automaticlly handle the connection to TraCI when we run our project, while running the two simulators in parallel.

I suggest at least reading through the [Hello-Sumo tutorial](https://github.com/burtonwilliamt/carlogicapi/blob/master/tutorials/Hello-Sumo) and this [OMNeT++ Tic-Toc Example](https://omnetpp.org/doc/omnetpp/tictoc-tutorial/) before doing this one. Once you've done that you should understand how .ned files define the network in the OMNeT++ simulation, how simple .ned classes have C++ code behind them, and how to configure a SUMO simulation. This tutorial should help you learn Veins, which connects OMNeT++ for network simulation and SUMO for road simulation. Since a lot of the files inherit from files in the Veins project, you can download the Veins source code; check out the [Veins Download](http://veins.car2x.org/download/) to get it. If you want to run it, you'll need to install Veins and its dependencies. See the [Veins Install Guide](http://veins.car2x.org/tutorial/) until we write a better one.

### Architecture

TODO: Add a cool class diagram here

### TutorialScenario.ned

Firstly, we need to define the network that is going to describe our example. This is described in [src/TutorialSenario.ned](https://github.com/burtonwilliamt/carlogicapi/blob/master/tutorials/VeinsTutorial/src/TutorialScenario.ned) of this project. If you open .ned files in the OMNET++ IDE, you'll probably see a graphical representation  of the network; to see the source code, click the Source tab in the bottom left of the window. As you can see, this file doesn't do much except `extend Scenario` (inherit from Scenario). Open up Scenario.ned from veins/src/veins/nodes. You might need to open as text / source if you are using the OMNeT++ IDE. You'll see this:
```
package org.car2x.veins.nodes;

import org.car2x.veins.base.connectionManager.ConnectionManager;
import org.car2x.veins.base.modules.BaseWorldUtility;
import org.car2x.veins.modules.mobility.traci.TraCIScenarioManagerLaunchd;
import org.car2x.veins.modules.obstacle.ObstacleControl;
import org.car2x.veins.modules.world.annotations.AnnotationManager;

network Scenario
{
    parameters:
        double playgroundSizeX @unit(m); // x size of the area the nodes are in (in meters)
        double playgroundSizeY @unit(m); // y size of the area the nodes are in (in meters)
        double playgroundSizeZ @unit(m); // z size of the area the nodes are in (in meters)
        @display("bgb=$playgroundSizeX,$playgroundSizeY"); // displays an icon
    submodules:
        //these define the member variables of this network
        //the format is:
        //variable_name: ClassName {}
        obstacles: ObstacleControl { //models the obstacles for the radio signals
          //We don't use this in our example
            @display("p=240,50");
        }
        annotations: AnnotationManager { //manages the drawings of network traffic
          //We don't use this in our example
            @display("p=260,50");
        }
        connectionManager: ConnectionManager { //manages the wireless connections
            parameters:
                @display("p=150,0;i=abstract/multicast");
        }
        world: BaseWorldUtility { //basic world object
            parameters:
                playgroundSizeX = playgroundSizeX;
                playgroundSizeY = playgroundSizeY;
                playgroundSizeZ = playgroundSizeZ;
                @display("p=30,0;i=misc/globe");
        }
        manager: TraCIScenarioManagerLaunchd { //manages connection to SUMO through TraCI
            parameters:
                @display("p=512,128");
        }

    //allows the cars to communicate in a mesh
    connections allowunconnected:

}
```
The version above is commented more than the source code. But it defines some objects that manage the simulation.

### Car.ned

The Car class that we are using is located in the package: org.car2x.veins.nodes.Car which is the same place as Scenario.ned. Car is not in fact a simple class. It declares objects for an application, a NIC (Network Interface Card), and mobility. As well as setting up the connections between the NIC and the application. See here:
```
package org.car2x.veins.nodes;

import org.car2x.veins.base.modules.*;
import org.car2x.veins.modules.nic.Nic80211p;

module Car
{
    parameters:
        string applType; //type of the application layer
        string nicType = default("Nic80211p"); // type of network interface card
        string veinsmobilityType; //type of the mobility module
    gates:
        input veinsradioIn; // gate for sendDirect
    submodules:
        // the application handles the logic for the communication
        appl: <applType> like org.car2x.veins.base.modules.IBaseApplLayer {
            parameters:
                @display("p=60,50");
        }
        // the NIC models the wireless properties
        nic: <nicType> like org.car2x.veins.modules.nic.INic80211p {
            parameters:
                @display("p=60,166");
        }
        // the mobility handles the interface with SUMO over TraCI
        veinsmobility: <veinsmobilityType> like org.car2x.veins.base.modules.IMobility {
            parameters:
                @display("p=130,172;i=block/cogwheel");
        }

    connections:
        nic.upperLayerOut --> appl.lowerLayerIn;
        nic.upperLayerIn <-- appl.lowerLayerOut;
        nic.upperControlOut --> appl.lowerControlIn;
        nic.upperControlIn <-- appl.lowerControlOut;

        veinsradioIn --> nic.radioIn;

}
```
This class uses the same syntax for parameters and submodules, but introduces the connections. Again the above copy has been commented.

### TraCIMobility

TraCIMobility is the simple class that holds driving-related code. It is in `org.car2x.veins.modules.mobility.traci.TraCIMobility` and has a .ned, .h, and .cc file. The .ned file pretty much only defines some parameters. But the C++ code is the real deal. The `TraCIMobility::changePosition()` function moves the node in the OMNeT++ simulation according to the messages from the SUMO sim over TraCI.
```
void TraCIMobility::changePosition()
{
	// ensure we're not called twice in one time step
	ASSERT(lastUpdate != simTime());

	// keep statistics (for current step)
	currentPosXVec.record(move.getStartPos().x);
	currentPosYVec.record(move.getStartPos().y);

	Coord nextPos = calculateAntennaPosition(roadPosition);
	nextPos.z = move.getCurrentPosition().z;

	// keep statistics (relative to last step)
	if (statistics.startTime != simTime()) {
		simtime_t updateInterval = simTime() - this->lastUpdate;

		double distance = move.getStartPos().distance(nextPos);
		statistics.totalDistance += distance;
		statistics.totalTime += updateInterval;
		if (speed != -1) {
			statistics.minSpeed = std::min(statistics.minSpeed, speed);
			statistics.maxSpeed = std::max(statistics.maxSpeed, speed);
			currentSpeedVec.record(speed);
			if (last_speed != -1) {
				double acceleration = (speed - last_speed) / updateInterval;
				double co2emission = calculateCO2emission(speed, acceleration);
				currentAccelerationVec.record(acceleration);
				currentCO2EmissionVec.record(co2emission);
				statistics.totalCO2Emission+=co2emission * updateInterval.dbl();
			}
			last_speed = speed;
		} else {
			last_speed = -1;
			speed = -1;
		}
	}
	this->lastUpdate = simTime();

	move.setStart(Coord(nextPos.x, nextPos.y, move.getCurrentPosition().z)); // keep z position
	move.setDirectionByVector(Coord(cos(angle), -sin(angle)));
	move.setSpeed(speed);
	if (hasGUI()) updateDisplayString();
	fixIfHostGetsOutside();
	updatePosition();
}
```
There is also code to record statistics and even some to force an accident! Since these TraCIMobility files are long, they aren't fully included here, instead have a [link to the source](https://github.com/sommer/veins/blob/master/src/veins/modules/mobility/traci/TraCIMobility.cc).

### TutorialAppl

The application part of the Car is in the TutorialAppl class which is comprised of a .ned, a .h, and a .cpp in the src folder included in the VeinsTutorial project [here](https://github.com/burtonwilliamt/carlogicapi/blob/master/tutorials/VeinsTutorial/src/TutorialAppl.cpp). It handles the messages from other Cars, sending and receiving them. In this example, I've made the cars slow down or speed up to the surrounding car's speeds when they receive a message from another car. This is supposed to sync the Car's speeds, and it serves as a simple example. Here is a function that gets called everytime SUMO updates the position of the Car.
```
void TutorialAppl::handlePositionUpdate(cObject* obj) {
    BaseWaveApplLayer::handlePositionUpdate(obj);

    //sends message every 5 seconds
    if (simTime() - lastSent >= 5) {
        std::string message = std::to_string(mobility->getSpeed());
        sendMessage(message);
        lastSent = simTime();
    }
}
```
And here is the code that matches the speed upon receiving a message:
```
void TutorialAppl::onData(WaveShortMessage* wsm) {
    //Receive a message with a target speed, slow down / speed up to that speed
    float message_speed = atof(wsm->getWsmData());
    traciVehicle->slowDown(message_speed, 1000); //slow down over 1s
}
```
Note that the slowDown method can also speed a car up. It just changes the speed over a given time.

### omnetpp.ini

The omnetpp.ini file is where all the parameters in .ned network files get set. It serves as a configuration file for the Veins simulation, and the file that is Run to start a simulation. The parameters can be confusing to find because of the inheritance structure and the star expansions. Just know that the argument names are dotted off of the variable names, not the classes. And star expansion works in the Unix way. The beginning `*.` before everything is the TutorialScenario object. And `**` is any number of nested `*.`s.
```
[General]
cmdenv-express-mode = true
cmdenv-autoflush = true
cmdenv-status-frequency = 10000000s
ned-path = .
debug-on-errors = true

network = veinstutorial.src.TutorialScenario  # the package where the Scenario is

##### Simulation Parameters ######
# * means TutorialScenario at the begginning
sim-time-limit = 1000s
#tkenv-image-path = path/to/background/image.png
*.playgroundSizeX = 1000m
*.playgroundSizeY = 1000m
*.playgroundSizeZ = 50m

##### TraCIScenarioManager Parameters ######
*.manager.updateInterval = 0.1s
*.manager.host = "localhost"
*.manager.port = 9999
*.manager.autoShutdown = false
*.manager.moduleType = "org.car2x.veins.nodes.Car"
*.manager.moduleName = "node"
*.manager.moduleDisplayString = ""
*.manager.launchConfig = xmldoc("tutorial.launchd.xml")

##### IEEE 802.11p Wireless Parameters #######
*.connectionManager.pMax = 20mW
*.connectionManager.sat = -89dBm
*.connectionManager.alpha = 2.0
*.connectionManager.carrierFrequency = 5.890e9 Hz
*.connectionManager.sendDirect = true

*.node[*].nicType = "Nic80211p"

*.**.nic.mac1609_4.txPower = 20mW
*.**.nic.mac1609_4.bitrate = 18Mbps

*.**.nic.phy80211p.sensitivity = -89dBm
*.**.nic.phy80211p.useThermalNoise = true
*.**.nic.phy80211p.thermalNoise = -110dBm
*.**.nic.phy80211p.decider = xmldoc("config.xml")
*.**.nic.phy80211p.analogueModels = xmldoc("config.xml")
*.**.nic.phy80211p.usePropagationDelay = true

##### Car Parameters #####
# Application Parameters
*.node[*].applType = "veinstutorial.src.TutorialAppl"
*.node[*].appl.dataPriority = 2
# Mobility Parameters
*.node[*].veinsmobilityType = "org.car2x.veins.modules.mobility.traci.TraCIMobility"
*.node[*].veinsmobility.x = 0
*.node[*].veinsmobility.y = 0
*.node[*].veinsmobility.z = 0

**.debug = true
**.coreDebug = true
```
The node vector is never initialized in the code we went over, this can be confusing, but it allows an arbitrary amount of Cars in the simulation. The flow in the SUMO configuration files populate the `node[]` vector at runtime.

### Running the VeinsTutorial Example

Assuming that you have Veins and SUMO installed properly, open up the OMNet++ IDE with the `omnetpp` terminal command. You can choose the carlogicapi repo as your workspace or make a folder in your Documents for it. Import Veins and this VeinsTutorial projects in the IDE with *File > Import > General: Existing Projects into Workspace* and select the `carlogicapi/tutorials/VeinsTutorial/` directory for the tutorial. Do the same but Import Veins from its source location.
Build the VeinsTutorial project with Ctrl-B or *Project > Build All*. 
Before we run our project, we need to run a script that will start a parallel SUMO simulation when we start our Veins/OMNeT++ sim. To do this, open a seperate terminal and run: ` ./sumo-launchd.py -vv` from the root of the Veins directory. Then, you are ready to run the example. Right click on `VeinsTutorial/simulations/omnetpp.ini` in the Project Explorer and *Run As > OMNet++ Simulation*. Click the Run button or press F5 to start the simulation in the window that pops up.

### Troubleshooting

In our testing, we found that the project can fail to build because of a version mismatch error in the Veins project. We just rebuilt the Veins project by running the Makefile in the Veins src directory, then rebuilt VeinsTutorial to solve this problem.

If you didn't notice that the project didn't build before running it, you'll get this error at runtime:
```
Exception occurred executing command line.
Cannot run program "~/carlogicapi/tutorials/VeinsTutorial/VeinsTutorial" (in directory "~/carlogicapi/tutorials/VeinsTutorial/simulations"): error=2, No such file or directory
```
##### No such file "BaseWaveAppLayer.h"

This is the error:
```
15:02:35 **** Incremental Build of configuration gcc-debug for project VeinsTutorial ****
make MODE=debug all 
src/TutorialAppl.cpp
In file included from src/TutorialAppl.cpp:3:0:
src/TutorialAppl.h:11:68: fatal error: veins/modules/application/ieee80211p/BaseWaveApplLayer.h: No such file or directory
 #include "veins/modules/application/ieee80211p/BaseWaveApplLayer.h"
                                                                    ^
compilation terminated.
Makefile:101: recipe for target 'out/gcc-debug//src/TutorialAppl.o' failed
make: *** [out/gcc-debug//src/TutorialAppl.o] Error 1

15:02:36 Build Finished (took 166ms)
```
Solution: right click on *VeinsTutorial Project Folder > Properties > OMNeT++ > makemake > Options > Compile Tab* and include the path to the veins-4.6 src folder.

![Screenshot of Solution](https://camo.githubusercontent.com/2afa59eb6a09dd73ce7c99c8bad2bc3682734488/68747470733a2f2f692e696d6775722e636f6d2f7a345572536c4b2e706e67)
