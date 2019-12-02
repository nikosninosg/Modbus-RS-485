#!/usr/bin/python3

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.compat import iteritems
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
import struct
import json
import math
import csv



#open json file
with open("jsonPy.json","r") as jf:
 data = jf.read()
 #print(data)



# parse file
obj = json.loads(data)
#print(obj["meters"])

for met in range(len(obj["meters"])):
 #print(obj["meters"][m])
 client = ModbusClient(method=obj["meters"][met]["method"], port=obj["meters"][met]['portSlave'], timeout=1 , stopbits=2, bytesize=8, parity='N', baudrate=38400)
 print(obj["meters"][met]["nameMeter"])
 
