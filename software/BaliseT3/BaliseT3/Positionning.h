#ifndef _POSITIONNING_h
#define _POSITIONNING_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class Positionning
{
public:
	Positionning();

	void updatePosition(uint32_t t1, uint32_t t2, uint32_t t3);
	float getX();
	float getY();

private:

};


#endif

