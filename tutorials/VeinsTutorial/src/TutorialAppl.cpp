
#include <stdlib.h>
#include "TutorialAppl.h"

using Veins::TraCIMobilityAccess;
using Veins::AnnotationManagerAccess;

Define_Module(TutorialAppl);

void TutorialAppl::initialize(int stage) {
    BaseWaveApplLayer::initialize(stage);
    if (stage == 0) {
        //setup veins pointers
        mobility = TraCIMobilityAccess().get(getParentModule());
        traci = mobility->getCommandInterface();
        traciVehicle = mobility->getVehicleCommandInterface();
        lastSent = simTime();
        traciVehicle->setLaneChangeMode(0);
    }
}

void TutorialAppl::receiveSignal(cComponent* source, simsignal_t signalID, cObject* obj, cObject* details) {
    Enter_Method_Silent();
    if (signalID == mobilityStateChangedSignal) {
        handlePositionUpdate(obj);
    }
}

void TutorialAppl::onData(WaveShortMessage* wsm) {
    //Receive a message with a target speed, slow down to that speed
    float message_speed = atof(wsm->getWsmData());
    traciVehicle->slowDown(message_speed, 1000); //slow down over 1s
}

void TutorialAppl::onBeacon(WaveShortMessage* wsm) {
    //do something on receiving a message from a beacon
}

void TutorialAppl::handlePositionUpdate(cObject* obj) {
    BaseWaveApplLayer::handlePositionUpdate(obj);

    //sends message every 5 seconds
    if (simTime() - lastSent >= 5) {
        std::string message = std::to_string(mobility->getSpeed());
        sendMessage(message);
        lastSent = simTime();
    }
}

void TutorialAppl::sendWSM(WaveShortMessage* wsm) {
    sendDelayedDown(wsm, individualOffset);
}

void TutorialAppl::sendMessage(std::string msg) {
    t_channel channel = dataOnSch ? type_SCH : type_CCH;
    WaveShortMessage* wsm = prepareWSM("data", dataLengthBits, channel, dataPriority, -1,2);
    wsm->setWsmData(msg.c_str());
    sendWSM(wsm);
}
