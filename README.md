# SiPM_QC
A GUI program for the quality control station of the SiPMs for the Muon (g-2) experiment.

## Introduction
This document is intended to give a summary of the GUI program for the quality control station of the SiPM for the Muon (g-2) experiment.
The main program is written in python language. 

## GUI
wxpython is used for designing the GUI of the SiPM QC Control Panel. 

## Slow Control
There are 2 main slow control devices in the system. First is the BK Precision bias voltage supply for the SiPM which is controlled though a serial-to-usb port.
Second is the LabJack device which is used to communicate with the T-sensor, PGA and EEPROM on the SiPM-board and with the multiplexer on the 16-LED-board.
SPI language is used for communication.

## Digitizer (DRS4)
DRS4 developed at PSI is used as the digitizer of the QC station. The program running drs4 is written in C language.
