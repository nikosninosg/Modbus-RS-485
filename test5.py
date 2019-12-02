#!/usr/bin/python3

import pymodbus
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import logging

def readModbusData():
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    client=ModbusClient(method='rtu',port='/dev/ttyUSB0', baudrate=38400,timeout=1,parity='N',stopbits=2)
    print(client.connect())
    client.debug_enabled()

    log.debug("Read holding registers")
    response=client.read_holding_registers(0,1,unit= 0x1B)
    response1=client.read_holding_registers(0,1,unit= 0x1B)


    print(response) #This returns the response for whole length of registers
    print(response1)
    # print(response.getRegister(0));  #This returns value of only one 

    client.close()
readModbusData()
