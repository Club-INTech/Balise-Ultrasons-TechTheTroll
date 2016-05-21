#ifndef _ENUM_h
#define _ENUM_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

// Définition des permissions d'écriture
enum Permission
{
	CAN_BE_FIRST,
	CANT_BE_FIRST,
	MUST_BE_LAST
};

#endif

