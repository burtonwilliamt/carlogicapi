
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
    }
}

void TutorialAppl::receiveSignal(cComponent* source, simsignal_t signalID, cObject* obj, cObject* details) {
    Enter_Method_Silent();
    if (signalID == mobilityStateChangedSignal) {
        handlePositionUpdate(obj);
    }
}

void TutorialAppl::onData(WaveShortMessage* wsm) {
    //TODO: do something when receive a message
}

void TutorialAppl::onBeacon(WaveShortMessage* wsm) {
    //do something
}

void TutorialAppl::handlePositionUpdate(cObject* obj) {
    BaseWaveApplLayer::handlePositionUpdate(obj);

    //TODO: do something when position updates
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
