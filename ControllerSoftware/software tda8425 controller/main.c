/*
 * software tda8425 controller.c
 *
 * Created: 30.06.2019 21:36:16
 * Author : Oleg
 */ 

/* Include section*/
#include <avr\io.h>
#include <avr\interrupt.h>
#include <avr\pgmspace.h>
#include <avr\sleep.h>
#include <stdbool.h>
#include <stdint.h>
#include <D:\radio\current_projects\ActiveSpeakers\ControllerSoftware\software tda8425 controller\GenDefines.h>
#include <D:\radio\current_projects\ActiveSpeakers\ControllerSoftware\software tda8425 controller\m88p_InternalModulesInitializing.h>



/* Functions declarations */
	void main (void) __attribute__ ((noreturn));
	void InternalModulesInitialization (void);
	void InitExternalModules ();
	void PreAmpComunicating (uint8_t, uint_least8_t);
	void UARTSendChar();
	bool UpdatePreAmpDataArray (uint8_t, uint8_t);

/* RAM data */
// 	uint8_t PreAmpDataArray[PreAmpRegistersCount-1]; // Minus one because the both volume registers contains same value
	uint8_t PreAmpDataArray[PreAmpRegistersCount];

/* The User Flags definition */
volatile uint8_t UserFlags = 0;		// User Status Flags
	#define PreAmpComunicatingFlag 0
	#define FlagName1 1
	#define FlagName2 2
	#define FlagName3 3
	#define FlagName4 4
	#define FlagName5 5
	#define FlagName6 6
	#define FlagName7 7

/* Interrupt vectors */
	EMPTY_INTERRUPT (INT0_vect)			// External Interrupt Request 0
	EMPTY_INTERRUPT (INT1_vect)			// External Interrupt Request 1
	EMPTY_INTERRUPT (PCINT0_vect)		// Pin Change Interrupt Request 0
	EMPTY_INTERRUPT (PCINT1_vect)		// Pin Change Interrupt Request 1
	EMPTY_INTERRUPT (PCINT2_vect)		// Pin Change Interrupt Request 2
	EMPTY_INTERRUPT (WDT_vect)			// Watchdog Time-out Interrupt
	EMPTY_INTERRUPT (TIMER2_COMPA_vect)	// Timer/Counter2 Compare Match A
	EMPTY_INTERRUPT (TIMER2_COMPB_vect)	// Timer/Counter2 Compare Match A
	EMPTY_INTERRUPT (TIMER2_OVF_vect)	// Timer/Counter2 Overflow
	EMPTY_INTERRUPT (TIMER1_CAPT_vect)	// Timer/Counter1 Capture Event
	EMPTY_INTERRUPT (TIMER1_COMPA_vect)	// Timer/Counter1 Compare Match A
	EMPTY_INTERRUPT (TIMER1_COMPB_vect)	// Timer/Counter1 Compare Match B
	EMPTY_INTERRUPT (TIMER1_OVF_vect)	// Timer/Counter1 Overflow
	EMPTY_INTERRUPT (TIMER0_COMPA_vect)	// TimerCounter0 Compare Match A 
	EMPTY_INTERRUPT (TIMER0_COMPB_vect)	// TimerCounter0 Compare Match B 
	EMPTY_INTERRUPT (TIMER0_OVF_vect)	// Timer/Couner0 Overflow
	EMPTY_INTERRUPT (SPI_STC_vect)		// SPI Serial Transfer Complete
	EMPTY_INTERRUPT (ADC_vect)			// ADC Conversion Complete
	EMPTY_INTERRUPT (EE_READY_vect)		// EEPROM Ready
	EMPTY_INTERRUPT (ANALOG_COMP_vect)	// Analog Comparator
	EMPTY_INTERRUPT (SPM_Ready_vect)	// Store Program Memory Read

	EMPTY_INTERRUPT (USART_UDRE_vect)	// USART, Data Register Empty
	EMPTY_INTERRUPT (USART_TX_vect)		// USART Tx Complete

ISR (TWI_vect)		// The Two-wire Serial Interface Interrupt Worker.
{
	uint8_t BusState = (TWSR & TWSRMask);
	
	/* Do Reset the TWINT flag by writing 1 into him! */
	TWCR |= 1<<TWINT;
	sei();
	if (UserFlags & (1<<PreAmpComunicatingFlag)) PreAmpComunicating(BusState, CalledByTWIInterruptWorker);
}

ISR (USART_RX_vect)	// USART Rx Complete
{
	
	// Firstly read the information about received byte
	if (UCSR0A & (1<<FE0 | 1<<DOR0 | 1<<UPE0)) UARTSendChar('E');
	else
	{
		uint8_t UARTData = UDR0;
		bool Status = false;
		uint8_t Value = 0;
		switch (UARTData)
		{
			case CalledByUser_UpdateVolume: case CalledByUser_UpdateBass: case CalledByUser_UpdateTreble: case CalledByUser_UpdateSwitches:
				while(!(UCSR0A & (1<<RXC0)));
				Value = UDR0;
				Status = UpdatePreAmpDataArray(UARTData, Value);
						if (Status == true) UARTSendChar('O');
						else UARTSendChar('E');
				break;
			
			case CalledByUser_UpdateAll:
				PreAmpComunicating(0xff,CalledByUser_UpdateAll);
				break;
			
			default:
				UARTSendChar('E');
				break;
		}
		
	}
}

void UARTSendChar(int Char)
{
	while(!(UCSR0A & (1<<UDRE0)));
	UDR0 = Char;
}

bool UpdatePreAmpDataArray (uint8_t Register, uint8_t Value)
{
	bool Status = false;
	
	switch (Register)
	{
		case CalledByUser_UpdateVolume:
			if ( (Value+VolMin) > VolMax ) Status = false;
			else
			{
				PreAmpDataArray[PreAmpLeftVolumeRegister] = VolMin + Value;
				PreAmpDataArray[PreAmpRightVolumeRegister] = VolMin + Value;
				Status = true;
			}
			break;
		
		case CalledByUser_UpdateBass:
			if ( (Value+BassMin) > BassMax ) Status = false;
			else
			{
				PreAmpDataArray[PreAmpBassRegister] = BassMin + Value;
				Status = true;
			}
			break;

		case CalledByUser_UpdateTreble:
			if ( (Value+TrebleMin) > TrebleMax ) Status = false;
			else
			{
				PreAmpDataArray[PreAmpTrebleRegister] = TrebleMin + Value;
				Status = true;
			}
			break;
		
		case CalledByUser_UpdateSwitches:
			PreAmpDataArray[PreAmpSwitchesRegister] = (PreAmpDataArray[PreAmpSwitchesRegister]|Value);
			Status = true;
			break;
		
		default:
			Status = false;
			break;
	}
	
	return Status;
}

void PreAmpComunicating (uint8_t BusState, uint_least8_t Caller)
{
	volatile static uint_least8_t WhatBeenSended, NextRegisterToBeSend, SendSingleRegister;
		#define RegisterSent 0
		#define DataSent 1
		#define False 0
		#define True 1
	
	void StartCommunication ()
	{
		TWCR |= (1<<TWSTA)|(1<<TWINT)|(1<<TWEN);
	}
	
	void StopCommunication ()
	{
		TWCR |= (1<<TWINT)|(1<<TWEN)|(1<<TWSTO);
		NextRegisterToBeSend = 0;
		UserFlags &= ~(1<<PreAmpComunicatingFlag);
	}
	
	switch (Caller)
	{
		case CalledByUser_UpdateAll:
			NextRegisterToBeSend = 0;
			SendSingleRegister = False;
			UserFlags |= (1<<PreAmpComunicatingFlag);
			StartCommunication();
			break;
	
		case CalledByTWIInterruptWorker:
			switch (BusState)
			{
				case SendedStart: case SendedReStart:
					TWDR = PreAmpWriteAddresss;		// Sending SLAW
					TWCR |= (~(1<<TWSTA))|(1<<TWINT)|(1<<TWEN);
					break;
			
				case SendedSLAW_ACK:		// Sending Register Address
					TWDR = (NextRegisterToBeSend == PreAmpSwitchesRegister) ? (PreAmpSwitchesRegister+PreAmpSwitchesRegisterAddressOffset) : NextRegisterToBeSend;
					TWCR |= (1<<TWINT)|(1<<TWEN);
					if (SendSingleRegister == False) NextRegisterToBeSend++;
					WhatBeenSended = RegisterSent;
					break;
			
				case SendedData_ACK:
					if (WhatBeenSended == RegisterSent)
					{
						TWDR = (SendSingleRegister == True) ? PreAmpDataArray[NextRegisterToBeSend] : PreAmpDataArray[(NextRegisterToBeSend-1)];
						TWCR |= (1<<TWINT)|(1<<TWEN);
						WhatBeenSended = DataSent;
					}
					else
					{
						if (SendSingleRegister == True) StopCommunication();
						else
						{
							if (NextRegisterToBeSend <= PreAmpSwitchesRegister) StartCommunication();
							else StopCommunication();
						}
					}
					break;
			
				default: break;
			}
	}
}



void main (void) {
	
	InternalModulesInitialization ();
	while(1){}
	
}

