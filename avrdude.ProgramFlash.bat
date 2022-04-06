@echo off

REM Usage: avrdude.exe [options]
REM Options:
REM   -p <partno>                Required. Specify AVR device.
REM   -b <baudrate>              Override RS-232 baud rate.
REM   -B <bitclock>              Specify JTAG/STK500v2 bit clock period (us).
REM   -C <config-file>           Specify location of configuration file.
REM   -c <programmer>            Specify programmer type.
REM   -D                         Disable auto erase for flash memory
REM   -i <delay>                 ISP Clock Delay [in microseconds]
REM   -P <port>                  Specify connection port.
REM   -F                         Override invalid signature check.
REM   -e                         Perform a chip erase.
REM   -O                         Perform RC oscillator calibration (see AVR053).
REM   -U <memtype>:r|w|v:<filename>[:format]
REM                              Memory operation specification.
REM                              Multiple -U options are allowed, each request
REM                              is performed in the order specified.
REM   -n                         Do not write anything to the device.
REM   -V                         Do not verify.
REM   -u                         Disable safemode, default when running from a script.
REM   -s                         Silent safemode operation, will not ask you if
REM                              fuses should be changed back.
REM   -t                         Enter terminal mode.
REM   -E <exitspec>[,<exitspec>] List programmer exit specifications.
REM   -x <extended_param>        Pass <extended_param> to programmer.
REM   -y                         Count # erase cycles in EEPROM.
REM   -Y <number>                Initialize erase cycle # in EEPROM.
REM   -v                         Verbose output. -v -v for more.
REM   -q                         Quell progress output. -q -q for less.
REM   -l logfile                 Use logfile rather than stderr for diagnostics.
REM   -?                         Display this usage.

set workdir=%~dp0
set avrdude="D:\software\installed electronic software\avrdude6.3\avrdude.exe"

set mcu=m88p
set programmer=apu2
set baud=19200

set hex_path="D:\radio\current_projects\ActiveSpeakers\ControllerSoftware\software tda8425 controller\Debug\SpeakersController.hex"

cd /D %workdir%
%avrdude% -p %mcu% -b %baud% -c %programmer% -U flash:w:%hex_path%:a
pause