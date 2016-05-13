/*
	Projet Balise T3
	Code du microcontrôleur embarqué dans la balise fixe
	Compatible avec Teensy 3.1 ou ultérieur

	Auteur : Sylvain GAULTIER
	Date : Mai 2016
*/

#include "Communication.h"
#include "Positionning.h"
#include "enum.h"
#include <avr/io.h>
#include <avr/interrupt.h>
#include <XBee\XBee.h>

/*
	### PIN MAPPING ###
*/
#define PIN_INT_80HZ	15
#define PIN_INT_40HZ	16
#define PIN_C1_80HZ		17
#define PIN_C1_40HZ		18
#define PIN_C2_80HZ		19
#define PIN_C2_40HZ		20

#define PIN_DEL_POWER	3
#define PIN_DEL_C1		4
#define PIN_DEL_C2		5
#define PIN_DEL_INT		6

/*
	### Variables d'aquisition des données ###
*/

// Assignation d'une balise à chaque case du tableau
#define CANAL_1	0
#define CANAL_2	1
#define INT		2

// Définition des modes "Lecture" et "Ecriture" les tableaux de données
#define READ	0	// Mode traitement des données
#define WRITE	1	// Mode acquisition de données

// Tableau de stockage des instants de réception des signaux
volatile uint32_t timeArray_80Hz[3];
volatile uint32_t timeArray_40Hz[3];

// Tableau des permissions d'écriture
volatile Permission permissionArray_80Hz[3];
volatile Permission permissionArray_40Hz[3];

volatile bool rwMode_80Hz; // vaut 'READ' ou 'WRITE'
volatile bool rwMode_40Hz;

// Tableau indiquant si la case correspondante a été mise à jour
volatile bool isWritten_80Hz[3];
volatile bool isWritten_40Hz[3];

// Pour envoyer les données finales via la xBee
Communication commXBee;


/*
	### Initialisation des variables et des I/O ###
*/
void setup()
{
	Serial.begin(9600);
	commXBee.init(Serial3);

	pinMode(PIN_INT_80HZ, INPUT);
	pinMode(PIN_INT_40HZ, INPUT);
	pinMode(PIN_C1_80HZ, INPUT);
	pinMode(PIN_C1_40HZ, INPUT);
	pinMode(PIN_C2_80HZ, INPUT);
	pinMode(PIN_C2_40HZ, INPUT);

	pinMode(PIN_DEL_POWER, OUTPUT);
	pinMode(PIN_DEL_C1, OUTPUT);
	pinMode(PIN_DEL_C2, OUTPUT);
	pinMode(PIN_DEL_INT, OUTPUT);

	rwMode_80Hz = WRITE;
	rwMode_40Hz = WRITE;
	isWritten_80Hz[CANAL_1] = false;
	isWritten_80Hz[CANAL_2] = false;
	isWritten_80Hz[INT] = false;
	isWritten_40Hz[CANAL_1] = false;
	isWritten_40Hz[CANAL_2] = false;
	isWritten_40Hz[INT] = false;
	timeArray_80Hz[CANAL_1] = 0;
	timeArray_80Hz[CANAL_2] = 0;
	timeArray_80Hz[INT] = 0;
	timeArray_40Hz[CANAL_1] = 0;
	timeArray_40Hz[CANAL_2] = 0;
	timeArray_40Hz[INT] = 0;
	permissionArray_80Hz[CANAL_1] = CAN_BE_FIRST;
	permissionArray_80Hz[CANAL_2] = CAN_BE_FIRST;
	permissionArray_80Hz[INT] = MUST_BE_LAST;
	permissionArray_40Hz[CANAL_1] = CAN_BE_FIRST;
	permissionArray_40Hz[CANAL_2] = CAN_BE_FIRST;
	permissionArray_40Hz[INT] = MUST_BE_LAST;

	attachInterrupt(PIN_INT_80HZ, isr_INT_80Hz, RISING);
	attachInterrupt(PIN_INT_40HZ, isr_INT_40Hz, CHANGE);
	attachInterrupt(PIN_C1_80HZ, isr_C1_80Hz, RISING);
	attachInterrupt(PIN_C1_40HZ, isr_C1_40Hz, CHANGE);
	attachInterrupt(PIN_C2_80HZ, isr_C2_80Hz, RISING);
	attachInterrupt(PIN_C2_40HZ, isr_C2_40Hz, CHANGE);

	// Indication du démarrage de la balise
	digitalWrite(PIN_DEL_POWER, HIGH);
}



/*
	### Boucle de lecture et de traitement des données ###
*/
void loop()
{
	// Objets permettant le calcul de la position
	Positionning kalman_80Hz;
	Positionning kalman_40Hz;

	/*
		Position calculée, en mm
	*/
	float positionX_80Hz = 0;
	float positionY_80Hz = 1000;

	float positionX_40Hz = 0;
	float positionY_40Hz = 1000;

	while (true)
	{
		if (rwMode_80Hz == READ)
		{
			kalman_80Hz.updatePosition(timeArray_80Hz[CANAL_1], timeArray_80Hz[CANAL_2], timeArray_80Hz[INT]);
			positionX_80Hz = kalman_80Hz.getX();
			positionY_80Hz = kalman_80Hz.getY();

			commXBee.sendPosition(positionX_80Hz, positionY_80Hz, true);

			// DEBUG 
			Serial.printf("#80#%u;%u;%u\n", timeArray_80Hz[CANAL_1], timeArray_80Hz[CANAL_2], timeArray_80Hz[INT]);

			// Mise à jour des permissions en fonction de la position
			updatePermissions(positionX_80Hz, positionY_80Hz, permissionArray_80Hz);

			// Passage en mode 'Acquisition'
			isWritten_80Hz[CANAL_1] = false;
			isWritten_80Hz[CANAL_2] = false;
			isWritten_80Hz[INT] = false;

			rwMode_80Hz = WRITE;
		}

		if (rwMode_40Hz == READ)
		{
			kalman_40Hz.updatePosition(timeArray_40Hz[CANAL_1], timeArray_40Hz[CANAL_2], timeArray_40Hz[INT]);
			positionX_40Hz = kalman_40Hz.getX();
			positionY_40Hz = kalman_40Hz.getY();

			commXBee.sendPosition(positionX_40Hz, positionY_40Hz, false);

			// DEBUG
			Serial.printf("#40#%u;%u;%u\n", timeArray_40Hz[CANAL_1], timeArray_40Hz[CANAL_2], timeArray_40Hz[INT]);

			// Mise à jour des permissions en fonction de la position
			updatePermissions(positionX_40Hz, positionY_40Hz, permissionArray_40Hz);

			// Passage en mode 'Acquisition'
			isWritten_40Hz[CANAL_1] = false;
			isWritten_40Hz[CANAL_2] = false;
			isWritten_40Hz[INT] = false;

			rwMode_40Hz = WRITE;
		}
	}
}



void updatePermissions(float x, float y, volatile Permission permissionArray[3])
{
	if (x < -1000 && y < 200)
	{
		permissionArray[CANAL_2] = CAN_BE_FIRST;
		permissionArray[CANAL_1] = CANT_BE_FIRST;
		permissionArray[INT] = CANT_BE_FIRST;
	}
	if (x < -1000 && y > 1800)
	{
		permissionArray[CANAL_1] = CAN_BE_FIRST;
		permissionArray[CANAL_2] = CANT_BE_FIRST;
		permissionArray[INT] = CANT_BE_FIRST;
	}
	else if (x < -700)
	{
		permissionArray[INT] = MUST_BE_LAST;
		permissionArray[CANAL_1] = CAN_BE_FIRST;
		permissionArray[CANAL_2] = CAN_BE_FIRST;
	}
	else if (x > 700)
	{
		permissionArray[INT] = CAN_BE_FIRST;
		permissionArray[CANAL_1] = CANT_BE_FIRST;
		permissionArray[CANAL_2] = CANT_BE_FIRST;
	}
	else
	{
		permissionArray[CANAL_1] = CAN_BE_FIRST;
		permissionArray[CANAL_2] = CAN_BE_FIRST;
		permissionArray[INT] = CAN_BE_FIRST;
	}
}


bool isWritingAllowed(bool rwMode, uint8_t indice, volatile Permission permissionArray[3], volatile bool isWritten[3])
{
	if (rwMode == WRITE)
	{
		if (!isWritten[indice])
		{
			if (permissionArray[indice] == CAN_BE_FIRST)
			{
				return true;
			}
			else if (permissionArray[indice] == CANT_BE_FIRST)
			{
				for (int i = 0; i < 3; i++)
				{
					if (isWritten[i])
					{
						return true;
					}
				}
				return false;
			}
			else // cas 'MUST_BE_LAST'
			{
				for (int i = 0; i < 3; i++)
				{
					if (!isWritten[i] && i != indice)
					{
						return false;
					}
				}
				return true;
			}
		}
		else
		{
			return false;
		}
	}
	else
	{
		return false;
	}
}


/*
	### Interruptions d'acquisition des données ###
*/

void isr_INT_80Hz()
{
	if (isWritingAllowed(rwMode_80Hz, INT, permissionArray_80Hz, isWritten_80Hz))
	{
		timeArray_80Hz[INT] = micros();
		isWritten_80Hz[INT] = true;
		if (isWritten_80Hz[CANAL_1] && isWritten_80Hz[CANAL_2])
		{
			rwMode_80Hz = READ;
		}
	}
}

void isr_INT_40Hz()
{
	if (isWritingAllowed(rwMode_40Hz, INT, permissionArray_40Hz, isWritten_40Hz))
	{
		timeArray_40Hz[INT] = micros();
		isWritten_40Hz[INT] = true;
		if (isWritten_40Hz[CANAL_1] && isWritten_40Hz[CANAL_2])
		{
			rwMode_40Hz = READ;
		}
	}
}

void isr_C1_80Hz()
{
	if (isWritingAllowed(rwMode_80Hz, CANAL_1, permissionArray_80Hz, isWritten_80Hz))
	{
		timeArray_80Hz[CANAL_1] = micros();
		isWritten_80Hz[CANAL_1] = true;
		if (isWritten_80Hz[INT] && isWritten_80Hz[CANAL_2])
		{
			rwMode_80Hz = READ;
		}
	}
}

void isr_C1_40Hz()
{
	if (isWritingAllowed(rwMode_40Hz, CANAL_1, permissionArray_40Hz, isWritten_40Hz))
	{
		timeArray_40Hz[CANAL_1] = micros();
		isWritten_40Hz[CANAL_1] = true;
		if (isWritten_40Hz[INT] && isWritten_40Hz[CANAL_2])
		{
			rwMode_40Hz = READ;
		}
	}
}

void isr_C2_80Hz()
{
	if (isWritingAllowed(rwMode_80Hz, CANAL_2, permissionArray_80Hz, isWritten_80Hz))
	{
		timeArray_80Hz[CANAL_2] = micros();
		isWritten_80Hz[CANAL_2] = true;
		if (isWritten_80Hz[CANAL_1] && isWritten_80Hz[INT])
		{
			rwMode_80Hz = READ;
		}
	}
}

void isr_C2_40Hz()
{
	if (isWritingAllowed(rwMode_40Hz, CANAL_2, permissionArray_40Hz, isWritten_40Hz))
	{
		timeArray_40Hz[CANAL_2] = micros();
		isWritten_40Hz[CANAL_2] = true;
		if (isWritten_40Hz[CANAL_1] && isWritten_40Hz[INT])
		{
			rwMode_40Hz = READ;
		}
	}
}