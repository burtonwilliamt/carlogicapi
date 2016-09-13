# Design

## Goals

### Fall 16

The goal for this semester is to get a working demo of efficiency and safety
improvements in a traffic simulator. Comm layer will be simplified, and the
focus will be on the API.

## High Level

The Car Logic API known as the API will be the main part of a three part system. The other two are the communication layer and
the car layer.

### Communication Layer

The communication layer should be modular from the API, it is only the IO to
and from other cars. It could be sending and receiving network packets,
handling data on a radio network, or writing to a file during a simulation. It
might in the future handle security concerns like message signing, and sending
data further along in a mesh network.

### API

The API will be in charge of data management, navigation, and traffic optimizations. It will use a map based location model - a.k.a. absolute position. 

### Car Layer

The car layer will be in charge of both the driving and the local data
acquisition. The car will report data about its current state to the API, and
the API will give instructions / information to the car.
