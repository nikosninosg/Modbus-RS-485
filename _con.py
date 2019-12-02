#!/usr/bin/python3

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 2, bytesize = 8,  parity='N', baudrate= 38400)
con = client.connect()
print(con)
#diavazei tous prwtous x registers
request = client.read_holding_registers(0x00,0x64,unit=0x1B) #200 - 300 = 0xc8 - 0x12c #0x2c=44
print (request.registers)									#100=0x64
print(request)
