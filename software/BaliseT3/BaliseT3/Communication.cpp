#include "Communication.h"

Communication::Communication()
{
}

void Communication::init(HardwareSerial & serial)
{
	serial.begin(115200);
	xBee.setSerial(serial);
	address.setMsb(0x0013a200);
	address.setLsb(0x403e0f30);
	txRequest.setAddress64(address);
	txRequest.setPayload(message);
	txRequest.setPayloadLength(sizeof(message));
}

void Communication::sendPosition(float x, float y, bool is80Hz)
{
	if (is80Hz)
	{
		message[0] = F80Hz;
	}
	else
	{
		message[0] = F40Hz;
	}
	

	int16_t int_x, int_y;
	if (x >= INT16_MAX)
	{
		int_x = INT16_MAX;
	}
	else if (x <= INT16_MIN)
	{
		int_x = INT16_MIN;
	}
	else
	{
		int_x = (int16_t)x;
	}

	if (y >= INT16_MAX)
	{
		int_y = INT16_MAX;
	}
	else if (y <= INT16_MIN)
	{
		int_y = INT16_MIN;
	}
	else
	{
		int_y = (int16_t)y;
	}

	// Coordonnée x
	message[1] = (uint8_t)((int_x & 0b1111111100000000) >> 8);
	message[2] = (uint8_t)(int_x & 0b0000000011111111);

	// Coordonnée y
	message[3] = (uint8_t)((int_y & 0b1111111100000000) >> 8);
	message[4] = (uint8_t)(int_y & 0b0000000011111111);

	xBee.send(txRequest);
}
