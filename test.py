#!/usr/bin/python3


import pymodbus
import serial
import json
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

myUnit=0x1B

#connect with modbus
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits=2, bytesize=8, timeout=1, baudrate=38400)
connection = client.connect()
print (connection)

#starting add, num of reg to read, slave unit.
result= client.read_holding_registers(298,2,unit= myUnit)
print(result.registers[0])
print(result.registers)

debug=True
#enable hardware handshake IMPORTANT
client.socket.rtscts=True



reg = client.read_holding_registers(208,1, unit = myUnit)
print reg.registers



print (reg)



