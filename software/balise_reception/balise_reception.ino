volatile unsigned long before;
volatile unsigned long now;
volatile bool updated;

void setup()
{
	Serial.begin(9600);
	attachInterrupt(0, interruption, RISING);
	before = 0;
	now = 0;
	updated = false;
}

void loop()
{
	if (updated)
	{
		Serial.println(now - before);
		updated = false;
	}
}

void interruption()
{
	before = now;
	now = micros();
	updated = true;
}