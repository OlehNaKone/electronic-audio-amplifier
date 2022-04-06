/*
 * m88pInternalModulesInitializing.h
 *
 * Created: 06.06.2020 19:35:00
 *  Author: Oleg
 */ 

#if defined (__AVR_ATmega88__)
#elif defined (__AVR_ATmega88A__)
#elif defined (__AVR_ATmega88P__)
#elif defined (__AVR_ATmega88PA__)
#elif defined (__AVR_ATmega88PB__)
#else
#	error "Wrong device type"
#endif


#ifndef M88P_INTERNALMODULESINITIALIZING_H_
#define M88P_INTERNALMODULESINITIALIZING_H_

void InternalModulesInitialization (void) {
	
	// Ports initialization:
	PORTB =	(0<<DisplayRCLK_bit) |
			(0<<PORTB1) |
			(0<<PORTB2) |
			(0<<PORTB3) |
			(0<<PORTB4) |
			(0<<PORTB5) |
			(0<<PORTB6) |
			(0<<PORTB7) ;
	
	DDRB =	(1<<DisplayRCLK_bit) |
			(0<<DDB1) |
			(0<<DDB2) |
			(0<<DDB3) |
			(0<<DDB4) |
			(0<<DDB5) |
			(0<<DDB6) |
			(0<<DDB7) ;


	PORTC =	(0<<PORTC0) |
			(0<<PORTC1) |
			(0<<PORTC2) |
			(0<<PORTC3) |
			(0<<PORTC4) |
			(0<<PORTC5) |
			(0<<PORTC6) ;
	
	DDRC =	(0<<DDC0) |
			(0<<DDC1) |
			(0<<DDC2) |
			(0<<DDC3) |
			(0<<DDC4) |
			(0<<DDC5) |
			(0<<DDC6) ;
	

	PORTD =	(0<<PORTD0) |
			(0<<PORTD1) |
			(0<<PORTD2) |
			(0<<PORTD3) |
			(0<<PORTD4) |
			(0<<AmpStbyPwm_bit) |
			(0<<PORTD6) |
			(0<<PORTD7) ;
	
	DDRD =	(0<<DDD0) |
			(0<<DDD1) |
			(0<<AmpFault_bit) |
			(0<<DDD3) |
			(0<<DDD4) |
			(1<<AmpStbyPwm_bit) |
			(0<<DDD6) |
			(0<<DDD7) ;
	
	// TCC0 initialization:
		/*
		TCC0 registers description:
		
			TCCR0A:
				COM0A(1,0) = 00...11 - Compare Output Mode if Compare A is match
				COM0B(1,0) = 00...11 - Compare Output Mode if Compare B is match
				WGM0(1,0) = 00...11 - Waveform Generation Mode
			
			TCCR0B:
				WGM0(2) = 0...1 - Waveform Generation Mode
				CS0(2,1,0) = 000...111 - T/C0 Clock Prescaler Mode - T/C0 stopped, 1, 8, 64, 256, 1024, ?0 fall, ?0 rise
				FOC0A - Force Output Compare A
				FOC0B - Force Output Compare B
			
			TCNT0 - Timer/Counter count register
			OCR0A - Output Compare Register A
			OCR0B - Output Compare Register B

			TIMSK0 - Timer/Counter Interrupt Mask Register:
				OCIE0A = 1 - Timer/Counter Compare Match A interrupt is enabled.
				OCIE0B = 1 - Timer/Counter Compare Match B interrupt is enabled.
				TOIE0 = 1 - Timer/Counter0 Overflow interrupt is enabled.

			TIFR0 - Timer/Counter 0 Interrupt Flag Register:
				OCF0A - Timer/Counter Compare Match A interrupt Flag
				OCF0B - Timer/Counter Compare Match B interrupt Flag
				TOV0 - Timer/Counter0 Overflow interrupt Flag

			GTCCR - General Timer/Counter Control Register:
				TSM = 1 - TC0 in sync. mode
				PSR10 = 1 - Timer/Counter0 prescaler is Reset.
		*/

	// SPI initialization:
		/*
		SPI registers description:
		
			SPDR - SPI data register
			
			SPCR:
				SPIE - SPI Interrupt Enable
				SPE - SPI Enable
				DORD: 0 - Little Endian | 1 - Big Endian
				MSTR: 0 - Slave | 1 - Master
				CPOL - SCK active LEVEL: 0 - HIGH | 1 - LOW
				CPHA - SCK active EDGE: 0 - Front | 1 - Rear
				SPR(1,0) - clock prescaler: 00...11 - 4, 16, 64, 128

			SPSR:
				SPI2X - if 1 SPR(1,0) divide by 2:  00...11 - 2, 8, 32, 64
				WCOL - Write COLlision Flag
				SPIF - SPI Interrupt Flag

		*/

	// TWI initialization:
		/*
		TWI registers description:

			TWBR - TWI Bit Rate Register
		
			TWSR - TWI Status Register:
				7:3.	TWS4:0		- TWI Status Bit
				1:0.	TWPS1:0		- TWI Prescaler: 00=1, 01=4, 10=16, 11=64
		
			TWDR - TWI Data Register
	
			TWCR - TWI Control Register
				7.	TWINT	- TWI Interrupt Flag
				6.	TWEA	- TWI Enable Acknowledge. 
				5.	TWSTA	- TWI START Condition
				4.	TWSTO	- TWI STOP Condition
				3.	TWWC	- TWI Write Collision Flag
				2.	TWEN	- TWI Enable
				0.	TWIE	- TWI Interrupt Enable
		
			TWAMR - TWI (Slave) Address Mask Register
				7:1.	TWAM7:1		- Each of the bits in TWAMR can mask (disable) the corresponding address bits in the TWI Address Register (TWAR).

			TWAR - TWI (Slave) Address Register
			7:1.	TWA7:0	- TWI (Slave) Address
			0.		TWGCE	- TWI General Call Recognition Enable Bit. If set, this bit enables the recognition of a General Call given over the 2-wire Serial Bus.
		*/
	TWBR = TWBRval;
	TWSR |= (0<<TWPS1)|(0<<TWPS0);
	TWCR |= (1<<TWEA)|(1<<TWIE);
	
	// USART initialization:
		/*
		USART registers description:
		
			UDR0 - Data Register
			UBRR0H & UBRR0L - Baud Rate Registers
	
			UCSR0A - Control and Status Register A:
				7.	RXC0	- USART Receive Complete - This flag bit is set when there are unread data in the receive buffer.
				6.	TXC0	- USART Transmit Complete - This flag bit is set when the entire frame in the transmit shift register has been shifted out and there are no new data currently present in the transmit buffer.
				5.	UDRE0	- USART Data Register Empty - The UDREn flag indicates if the transmit buffer (UDRn) is ready to receive new data.
				4.	FE0		- Frame Error - This bit is set if the next character in the receive buffer had a frame error when received. Always set this bit to zero when writing to UCSR0A.
				3.	DOR0	- Data OverRun - This bit is set if a data overrun condition is detected. A data overrun occurs when the receive buffer is full (two characters), it is a new character waiting in the receive shift register, and a new start bit is detected.
				2.	UPE0	- USART Parity Error - This bit is set if the next character in the receive buffer had a parity error when received and the parity checking was enabled at that point (UPMn1 = 1). This bit is valid until the receive buffer (UDRn) is read. Always set this bit to zero when writing to UCSRnA.
				1.	U2X0	- Double the USART Transmission Speed - This bit only has effect for the asynchronous operation. 
				0.	MPCM0	- Multi-processor Communication Mode - When the MPCMn bit is written to one, all the incoming frames received by the USART receiver that do not contain address information will be ignored.
		
			UCSR0B - Control and Status Register B:
				7.	RXCIE0	- RX Complete Interrupt Enable
				6.	TXCIE0	- TX Complete Interrupt Enable 
				5.	UDRIE0	- USART Data Register Empty Interrupt Enable
				4.	RXEN0	- Receiver Enable
				3.	TXEN0	- Transmitter Enable
				2.	UCSZ02	- Character Size - The UCSZn2 bits combined with the UCSZn1:0 bit in UCSRnC sets the number of data bits (character size) in a frame the receiver and transmitter use.
				1.	RXB80	- Receive Data Bit 8 - is the ninth data bit of the received character when operating with serial frames with nine data bits. Must be read before reading the low bits from UDRn.
				0.	TXB80	- Transmit Data Bit 8 - is the ninth data bit in the character to be transmitted when operating with serial frames with nine data bits. Must be written before writing the low bits to UDRn.
		
			UCSR0C - Control and Status Register C:
				7:6.	UMSEL01:0	- USART Mode Select - 00-async., 01-sync., 11-Master SPI
				5:4.	UPM01:0		- Parity Mode - 00-disabled, 10-even parity, 11-odd parity
				3.		USBS0		- Stop Bit Select - 0-single bit, 1-double bits
				2:1.	UCSZ01:0	- Character Size
				0.		UCPOL0		- Clock Polarity - 0-Transmit on Rising @ Receive on Falling, 1-Transmit on Falling @ Receive on Rising
		
			UCSZ02:0 Character Size:
				000-5-bit, 001-6-bit, 010-7-bit, 011-8-bit, 111-9-bit
		*/
	UBRR0L = LO(bauddivider);
	UBRR0H = HI(bauddivider);
	UCSR0A = 0;
	UCSR0B =	(1<<RXCIE0)	|	// The Interrupt when Receive Complete
				(0<<TXCIE0)	|	// The Interrupt when Transmit Complete
				(0<<UDRIE0)	|	// The Interrupt when Data Register Empty
				(1<<RXEN0)	|	// Receiver enable
				(1<<TXEN0)	|	// Transmitter enable
				(0<<UCSZ02);
	
	UCSR0C = 	(0<<UMSEL01)|
				(0<<UMSEL00)|
				(0<<UPM01)	|
				(0<<UPM00)	|
				(0<<USBS0)	|
				(1<<UCSZ01)	|
				(1<<UCSZ00);
				
	RXD_PORT |= 1<<RXD_BIT;		// Pull-Up Rx input for noise protection
			
	// ADC initialization.
		/* 
		ADC registers description:
		
			ADMUX:
				REFS(1,0) = 00 - AREF | 01 - AVcc | 11 - Internal 1V1 voltage reference
				ADLAR = 0 - right adj result | 1 - left adj result
				MUX(3,2,1,0) = 0000...1111 - input select:
							0000...0111 - adc0...adc7
							1110 - 1V1 voltage reference
							1111 - AGND
			
			ADCSRA:
				ADEN = 1 - ADC is Enable
				ADSC = 1 - Start Single/First Conversation
				ADATE = 1 - Auto Triggering of the ADC is enabled
				ADIF - ADC Interrupt Flag
				ADIE = 1 - ADC Conversation Complete Interrupt is activated
				Clock prescaler: ADPS(2,1,0) = 000...111 - 2, 2, 4, 8, 16, 32, 64, 128
			
			ADCSRB:
				ACME = 1 - When the ADC is switched off (ADEN in ADCSRA is zero), the ADC multiplexer selects the negative input to the Analog Comparator.
				ADC Auto Trigger Source: ADTS(2,1,0) = 000...111 - Free Runnig Mode | An. Comp. | INT0 | T/C0 comp. match A | T/C0 overflow | T/C1 comp. match B | T/C1 overflow| T/C1 capture event

			DIDR0:
				ADC5D...ADC0D: ADC5...ADC0 Digital Input Disable
		*/			

	// Analog Comparator initialization:
		/*	
		Analog Comparator registers description:
		
			ACSR:
				ACD = 1 - Analog Comparator Disable. When this bit is written logic one, the power to the Analog Comparator is switched off.
				ACBG = 1 - A fixed bandgap reference voltage is connected to the positive comparator input; 0 - The Positive Comparator Input connected to a IO Pin.
				ACO - Analog Comparator Output.
				ACI - Analog Comparator Interrupt Flag.
				ACIE - Analog Comparator Interrupt Enable.
				ACIC - 1 - enable the input capture function in Timer/Counter1 to be triggered by the analog comparator.
				ACIS(1,0) - Analog Comparator Interrupt Mode Select: 00 - when output is toggle | 10 - on Falling Output Edge | 11 - on Rising Output Edge.
		*/			
	ACSR |= (1<<ACD)|
			(0<<ACBG)|
			(0<<ACIE)|
			(0<<ACIC)|
			(0<<ACIS1)|
			(0<<ACIS0);	// Comparator disabled.

	// External Interrupts initialization:		
		/*
		Interrupt registers description:
		
			EICRA:
				ISC0(1,0) - INT0 interrupt generate mode: 00...11 - LOW level | any logic change | FALLING edge | RISING change
				ISC1(1,0) - INT0 interrupt generate mode: 00...11 - LOW level | any logic change | FALLING edge | RISING change
	
			EIMSK:
				INT0, INT1 - External Interrupt enable
	
			EIFR:
				INTF0, INTF1 - External Interrupt flags
		
			PCICR:
				PCIE2 - Pin Change Interrupt 2 Enable, any logical change on any pin of PCMSK2 will generate an interrupt
				PCIE1 - Pin Change Interrupt 1 Enable, any logical change on any pin of PCMSK1 will generate an interrupt
				PCIE0 - Pin Change Interrupt 0 Enable, any logical change on any pin of PCMSK0 will generate an interrupt
	
			PCIFR:
				PCIF2, PCIF1, PCIF0 - Pin Change Interrupt Flags
		
			PCMSK2:
				PCINT23...PCINT16 - Enable Pin Change Interrupt on each pin
		
			PCMSK1:
				PCINT14...PCINT8 - Enable Pin Change Interrupt on each pin
		
			PCMSK0:
				PCINT7...PCINT0 - Enable Pin Change Interrupt on each pin
		*/
	
	sei();	
}



#endif /* M88PINTERNALMODULESINITIALIZING_H_ */