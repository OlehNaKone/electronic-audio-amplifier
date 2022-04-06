/*
 * GenDefines.h
 *
 * Created: 31.05.2020 03:40:47
 *  Author: Oleg
 */ 


#ifndef GENDEFINES_H_
#define GENDEFINES_H_

/* GENERAL DEFINES SECTION */

/* UART Constants*/
	#define F_CPU		8000000L
	#define baudrate	19200L
	#define bauddivider	(F_CPU/(16*baudrate)-1)
	#define HI(x)		((x)>>8)
	#define LO(x)		((x)& 0xFF)

/* TWI Constants */
	#define Fscl	75000L	// TWI SCL freq. = 75 kHz
	#define TWPSval	1		// TWPS1:0		- TWI prescaler: 00=1, 01=4, 10=16, 11=64
	#define TWBRval ((F_CPU/Fscl)-16)/(2*TWPSval)

	#define TWSRMask			0b11111000
	#define GlobalBusError		0x00
	#define WaitingForResult	0xf8
	#define SendedStart			0x08
	#define SendedReStart		0x10
	#define SendedSLAW_ACK		0x18
	#define SendedSLAW_NACK		0x20
	#define SendedData_ACK		0x28
	#define SendedData_NACK		0x30
	#define ArbitrationLost		0x38
	#define SendedSLAR_ACK		0x40
	#define SendedSLAR_NACK		0x48
	#define ReceivedData_ACK	0x50
	#define ReceivedData_NACK	0x58

	#define UserCall_0			0xfa
	#define UserCall_1			0xfb
	#define UserCall_2			0xfc
	#define UserCall_3			0xfd
	#define UserCall_4			0xfe
	#define UserCall_5			0xff

/* PreAmp Constants */
	#define PreAmpWriteAddresss	0b10000010	// In the DataSheet named as MAD
	#define PreAmpReadAddresss	0b10000011
	#define PreAmpRegistersCount 5
	#define PreAmpLeftVolumeRegister	0	// In the DataSheet named as SAD
	#define PreAmpRightVolumeRegister	1
	#define PreAmpBassRegister			2
	#define PreAmpTrebleRegister		3
	#define PreAmpSwitchesRegister		4
	#define PreAmpSwitchesRegisterAddressOffset 4	// Switches Register have 0x08 address
	
	/* Count of The Volume Steps = 36 */
		#define VolMax		255		// +6 dB
		#define VolMin		220		// -64 dB
		#define VolOFF		219		// -80 dB

	/* Count of The Bass Steps = 10 */
		#define BassMax		251		// +15 dB
		#define BassZero	246		// 0 dB
		#define BassMin		242		// -12 dB

	/* Count of The Treble Steps = 9 */
		#define TrebleMax	250		// +12 dB
		#define TrebleZero	246		// 0 dB
		#define TrebleMin	242		// -12 dB

	/* Switches Register Bits */
		#define PreAmpSwitchBitsOffset	(1<<7)|(1<<6)
		#define PreAmpMuteBit			5
		#define PreAmpStereoEffectsBit	4
		#define PreAmpMonoStereoBit		3
		#define PreAmpMusicLine1Bit		2
		#define PreAmpMusicLine0Bit		1
		#define PreAmpInputSelectorBit	0
		
		#define PreAmpMuteON			(1<<PreAmpMuteBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpMuteOFF			(0<<PreAmpMuteBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpInputExtStereo	(1<<PreAmpMusicLine1Bit)|(1<<PreAmpMusicLine0Bit)|(0<<PreAmpInputSelectorBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpInputIntStereo	(1<<PreAmpMusicLine1Bit)|(1<<PreAmpMusicLine0Bit)|(1<<PreAmpInputSelectorBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpInputExtSoundA	(0<<PreAmpMusicLine1Bit)|(1<<PreAmpMusicLine0Bit)|(0<<PreAmpInputSelectorBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpInputExtSoundB	(1<<PreAmpMusicLine1Bit)|(0<<PreAmpMusicLine0Bit)|(0<<PreAmpInputSelectorBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpInputIntSoundA	(0<<PreAmpMusicLine1Bit)|(1<<PreAmpMusicLine0Bit)|(1<<PreAmpInputSelectorBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpInputIntSoundB	(1<<PreAmpMusicLine1Bit)|(0<<PreAmpMusicLine0Bit)|(1<<PreAmpInputSelectorBit)|(PreAmpSwitchBitsOffset)
		
		#define PreAmpSoundModeSaptial	(1<<PreAmpMonoStereoBit)|(1<<PreAmpStereoEffectsBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpSoundModeStereo	(1<<PreAmpMonoStereoBit)|(0<<PreAmpStereoEffectsBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpSoundModePseudo	(0<<PreAmpMonoStereoBit)|(1<<PreAmpStereoEffectsBit)|(PreAmpSwitchBitsOffset)
		#define PreAmpSoundModeMono		(0<<PreAmpMonoStereoBit)|(0<<PreAmpStereoEffectsBit)|(PreAmpSwitchBitsOffset)

/* Communication defines */
	#define CalledByUser_UpdateVolume	0
	#define CalledByUser_UpdateBass		2
	#define CalledByUser_UpdateTreble	3
	#define CalledByUser_UpdateSwitches 4
	#define CalledByUser_UpdateAll		5
	#define CalledByTWIInterruptWorker	254

		
/* Ports Defines */
	#define UART_DDR   DDRD
	#define UART_PORT  PORTD

	#define I2C_DDR   DDRC
	#define I2C_PORT  PORTC

	#define SPI_DDR   DDRB
	#define SPI_PORT  PORTB

	#define MainAmpControl_PORTreg	PORTD
	#define MainAmpControl_PINreg	PIND
	#define MainAmpControl_DDRreg	DDRD
	#define AmpFault_bit	2
	#define	AmpStbyPwm_bit	5

	#define DisplayRCLK_bit 0




#endif /* GENDEFINES_H_ */