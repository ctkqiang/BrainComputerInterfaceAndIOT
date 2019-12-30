/*
 ***************************************
 * BRAINTECH PRIVATE LIMITED 👩🏽‍🔬👨🏽‍🔬👩🏽‍🔬👨🏽‍🔬🔬
 * JOHN MELODY MELISSA
 ************************************** 
 * This is a copyrighted script.
 * All rights reserved © 2019 BRAINTECH.
 ***************************************
 */

#ifndef  SERIALPORT_H
#define SERIALPORT_H
#define ARDUINO_WAIT_TIME 2000
#define MAX_DAATA_LENGTH 255

#include <windows.h>

#include <stdio.h>
#include <stdlib.h>

class SerialPort
{
private:
    HANDLE handler;
    bool connected;
    COMSTAT status;
    DWORD errors;
public:
    SerialPort(char *portName);
    ~SerialPort();

    int readSerialPort(char *buffer, unsigned int buf_size);
    bool writeSerialPort(char *buffer, unsigned int buf_size);
    bool isConnected();
};

#endif // ! SERIALPORT_H
