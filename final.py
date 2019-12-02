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

for met in range(len(obj["meters"])):
 client = ModbusClient(method = obj["meters"][met]["method"], port = obj["meters"][met]['portSlave'], timeout=1 , stopbits=2, bytesize=8, parity='N', baudrate=38400)
 
 
 if client.connect() == True: 
  print("Connected meter {} with address: {}".format(obj["meters"][met]["nameMeter"], obj["meters"][met]["slaveID"]))
 else:
  print("Failed connection")
  exit()
  
 print("_______________________________________________________")
 print("_______________________________________________________")
 
 client.debug_enabled()
 #enable hardware handshake IMPORTANT
 #client.socket.rtscts=True


 #print(result.raw())

 for i in range(len(obj["meters"][met]["registers"])):
  print("Register Adrress: {}".format(obj["meters"][met]["registers"][i]["address"]))
  result = client.read_input_registers(obj["meters"][met]["registers"][i]["address"], 2, unit = obj["meters"][met]["slaveID"])
  #print(result) #response regs
  #print(result.registers) #print values of register address  

  reg_list = result.registers #list: value of registers

  #PROGRAM: DECODING 
  #getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]
  
  def binaryToFloat(value):
   f = int(value, 2) 
   return struct.unpack("f", struct.pack("I", f))[0]

  def decimalToBinary(num):
   if num > 1:
    decimalToBinary(num // 2)

  binaryLSB = decimalToBinary(reg_list[1])
  binaryMSB = decimalToBinary(reg_list[0])

  strLSB = str(bin(reg_list[1]))[2:]
  strMSB = str(bin(reg_list[0]))[2:]

  fixedLenthStrLSB = strLSB.zfill(16)
  fixedLenthStrMSB = strMSB.zfill(16)

  strDoubleWord = fixedLenthStrMSB + fixedLenthStrLSB

  # binary to float
  floatNumber = binaryToFloat(strDoubleWord)
  float(floatNumber)
  #print('Decimal equivalent of ' + strDoubleWord) 

  #print(floatNumber) #akriveis metatropi bin to float
 
  description = obj["meters"][met]["registers"][i]["Description"]
  print("Description: {}".format(description))
 
  value = str(round(floatNumber,2)) + ' ' + obj["meters"][met]["registers"][i]["var"]
  print("{} = {}".format(obj["meters"][met]["registers"][i]["shortDe"],value))
  print("----------------------------------")
 
  #write in csv
  csv.register_dialect('myDialect', delimiter = '|', quoting=csv.QUOTE_NONE, skipinitialspace=True)

  row = [ obj["meters"][met]["nameMeter"], obj["meters"][met]["slaveID"], obj["meters"][met]["registers"][i]["address"], value, description ] 
  with open('output.csv', 'a') as csvFile:
   writer = csv.writer(csvFile, dialect='myDialect')
   writer.writerow(row)
  csvFile.close

