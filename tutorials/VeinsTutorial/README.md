## Tutorial using Simple Veins Example

I've made a simplified example project in order to make it easier to learn Veins, since the example included with Veins doesn't include any documentation and can be hard to understand.

I suggest at least reading through the [Hello-Sumo tutorial](https://github.com/burtonwilliamt/carlogicapi/blob/master/tutorials/Hello-Sumo/tutorial.md) and this [OMNet++ Tic-Toc Example](https://omnetpp.org/doc/omnetpp/tictoc-tutorial/) if you haven't already. Once you've done that you should understand how .ned files define the network in the OMNet++ simulation, how simple .ned classes have C++ code behind them, and how to configure a SUMO simulation. This tutorial should help you learn Veins, which connects OMNet++ for network simulation and SUMO for road simulation. Since a lot of the files inherit from files in the Veins project, you'll need to download Veins; check out the [Veins Download](http://veins.car2x.org/download/) to get it.

### Architecture

TODO: Add a cool class diagram here

### TutorialScenario.ned

Firstly, we need to define the network that is going to describe our example. This is described in [src/TutorialSenario.ned](https://github.com/burtonwilliamt/carlogicapi/blob/master/tutorials/VeinsTutorial/src/TutorialScenario.ned) of this project.
As you can see, this file doesn't do much except `extend Scenario` (inherit from Scenario). Open up Scenario.ned from veins/src/veins/nodes. You might need to open as text / source if you are using the OMNet++ IDE. You'll see this:
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

TraCIMobility is the simple class that holds driving-related code. It is in org.car2x.veins.modules.mobility.traci.TraCIMobility and has a .ned, .h, and .cc file. The .ned file pretty much only defines some parameters. But the C++ code is the real deal. The `TraCIMobility::changePosition()` function moves the node in the OMNet++ simulation according to the messages from the SUMO sim over TraCI. There is also code to record statistics and even some to force an accident! We won't be using that in this example, though the example provided with Veins does. Since these TraCIMobility files are long, they aren't included here, instead have a [link to the source](https://github.com/sommer/veins/blob/master/src/veins/modules/mobility/traci/TraCIMobility.cc).

### TutorialAppl

The application part of the Car is in the TutorialAppl class which is comprised of a .ned, a .h, and a .cpp in the src folder included in the VeinsTutorial project. It defines what 
