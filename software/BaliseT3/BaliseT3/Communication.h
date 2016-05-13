#ifndef _COMMUNICATION_h
#define _COMMUNICATION_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#include <XBee.h>

// (uint8_t) indique de quelle balise il s'agit
#define F80Hz	0
#define F40Hz	1

/*
	##### Protocole de communication #####
	Longueur de tramme : 7 octets
	tramme[0] : identifiant balise (F80Hz ou F40Hz)
	
	Coordonnée X (indices 1-2) : uint16_t
		tramme[1] : octet de poids fort
		tramme[2] : octet de poids faible

	Coordonnée Y (indices 3-4) : uint16_t
		tramme[3] : octet de poids fort
		tramme[4] : octet de poids faible
*/


class Communication
{
public:
	Communication();

	void init(HardwareSerial & serial);

	/* 
		Formate et envoi les données (x,y) précédées d'un indicateur identifiant la balise source de ces données 
		Unité : mm	
	*/
	void sendPosition(float x, float y, bool is80Hz);

private:
	XBee xBee;
	XBeeAddress64 address;
	ZBTxRequest txRequest;
	uint8_t message[5];
};

#endif

