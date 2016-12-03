//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#include "CarLogicManager.h"

Define_Module(CarLogicManager);

CarLogicManager::CarLogicManager() {
    // TODO Auto-generated constructor stub

}

CarLogicManager::~CarLogicManager() {
    // TODO Auto-generated destructor stub
}

void CarLogicManager::initialize(int stage) {
    cSimpleModule::initialize(stage);

    hostname = par("hostname").stringValue();
    port = par("port");

    try {
        static TCPSocket soc(hostname, port);
        socket = &soc;
    }
    catch(SocketException &e) {
        cerr << e.what() << endl;
        exit(1);
    }

    char initPacket[] = "Init";
    int initPacketLength = strlen(initPacket);
    socket->send(initPacket, initPacketLength);

    updateInterval = par("updateInterval");
    executeOneTimestepTrigger = new cMessage("stepManager");
    scheduleAt(0.1, executeOneTimestepTrigger);

}

void CarLogicManager::handleMessage(cMessage *msg) {
    if (msg->isSelfMessage()) {
        handleSelfMsg(msg);
        return;
    }
    //must be message to be sent to python
    sendToPython(check_and_cast<Send *>(msg));
}

void CarLogicManager::handleSelfMsg(cMessage *msg) {
    if (msg == executeOneTimestepTrigger) {
        executeOneTimestep();
        scheduleAt(simTime()+updateInterval, executeOneTimestepTrigger);
    }
    else
        error("CarLogicManager received unknown self-message");
}

void CarLogicManager::executeOneTimestep() {
    //send
    try {
        char initPacket[] = "Hello";
        int initPacketLength = strlen(initPacket);
        socket->send(initPacket, initPacketLength);
    } catch (SocketException &e) {
        //nothing
    }
    //receive
    unsigned int buffer_len = 1024;
    char buffer[buffer_len+1];
    int bytesReceived;
    if ((bytesReceived = (socket->recv(buffer, buffer_len))) <= 0) return;
    buffer[bytesReceived] = '\0';
    printf("buffer:%s\n", buffer);
}

void CarLogicManager::sendToPython(Send *msg) {
    const char *buffer = msg->getData();
    unsigned int buffer_len = strlen(buffer);
    socket->send(buffer, buffer_len);
}

void CarLogicManager::finish() {
    //nothing yet
    socket->cleanUp();
}
