#define PIN_US			2
#define FREQUENCE		40000	//en Hz
#define DUREE_BURST_ON	10000	//en µs
#define DUREE_BURST_OFF	10000	//en µs
#define DUREE_REFREESH	1000	//en µs


void setup()
{
	Serial.begin(9600);
	pinMode(PIN_US, OUTPUT);
}

void loop()
{
	for (long frequence = 36000; frequence <= 44000; frequence += 100)
	{
		tone(PIN_US, frequence);
		Serial.println(frequence);
		delay(250);
	}
}