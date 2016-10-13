/*
 * TutorialAppl.h
 *
 *  Created on: Oct 10, 2016
 *      Author: greg
 */

#ifndef TUTORIALAPPL_H_
#define TUTORIALAPPL_H_

#include "veins/modules/application/ieee80211p/BaseWaveApplLayer.h"
#include "veins/modules/mobility/traci/TraCIMobility.h"
#include "veins/modules/mobility/traci/TraCICommandInterface.h"

using Veins::TraCIMobility;
using Veins::TraCICommandInterface;
//using Veins::AnnotationManager; //add for annotations

class TutorialAppl : public BaseWaveApplLayer {
    public:
        virtual void initialize(int stage);
        virtual void receiveSignal(cComponent* source, simsignal_t signalID, cObject* obj, cObject* details);
    protected:
        TraCIMobility* mobility;
        TraCICommandInterface* traci;
        TraCICommandInterface::Vehicle* traciVehicle;
        simtime_t lastSent; // the last time this sent a message

        virtual void onData(WaveShortMessage* wsm);
        virtual void onBeacon(WaveShortMessage* wsm);
        virtual void handlePositionUpdate(cObject* obj);
        void sendMessage(std::string blockedRoadId);
        virtual void sendWSM(WaveShortMessage* wsm);
};

#endif /* TUTORIALAPPL_H_ */
