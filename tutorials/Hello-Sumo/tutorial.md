#Tutorials

Many of the tutorials on the websites are either A) confusing, or B) too in-depth. Read below to see what we thought we could do better on.


##Sumo

###Basic Sumo run-through

This tutorial is the Hello Sumo tutorial found [here](http://sumo.dlr.de/wiki/Tutorials/Hello_Sumo). This will show you how to create your own simulation from nothing.

1. Create a directory to place your files in. In my case, I called this Hello-Sumo/.

2. The two necessary components to run a simulation are: a road network(described in the .net.xml) and cars to run on the network(described by the .rou.xml file). The first of these is generated from two parts. The first is a list of nodes, or junctions in the road network(a .nod.xml file). The second is a list of edges, which describes how those junctions are connected(a .edg.xml file). Note: these two files are only used to generate the .net.xml file.
    * First create a file called hello.nod.xml, and in it describe three nodes like this:
    ```
    #filename: hello.nod.xml
    <nodes>
        <node id="1" x="-250.0" y="0.0" />
        <node id="2" x="+250.0" y="0.0" />
        <node id="3" x="+251.0" y="0.0" />
    </nodes>
    ```
    These three nodes are junctions in our road. The id is a unique id, and the coordinates are specified.
    * Then create your edges file called hello.edg.xml, then describe the two edges like this:
    ```
    #filename: hello.edg.xml
    <edges>
      <edge from="1" id="1to2" to="2" />
      <edge from="2" id="out" to="3" />
    </edges>
    ```
    These two edges are connected the "from" node to the "to" node. CRAZY right? Use the node id to specify this, and assign the edge a unique id as well.

3. After you have your nodes and your edges, you can now generate your net.xml file. Do this by running the following command:
`netconvert --node-files=hello.nod.xml --edge-files=hello.edg.xml --output-file=hello.net.xml`
At this point you can run your net.xml file in sumo to see your road network. Do this with the following command:
`sumo-gui -n hello.net.xml`

4. Once you're properly satisfied with your majestic road network, you can put a vehicle on it. Do this by creating the hello.rou.xml routes file. Paste the following into it:
    ```
   #filename: hello.rou.xml
    <routes>
        <vType accel="1.0" decel="5.0" id="Car" length="2.0" maxSpeed="100.0" sigma="0.0" />
        <route id="route0" edges="1to2 out"/>
        <vehicle depart="1" id="veh0" route="route0" type="Car" />
    </routes>
   ``` 
