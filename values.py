#!/usr/bin/env python


# Test program for DZT 6001: 80A, Single phase kWh meter, LCD, RS485/Modbus
#
# Home page: https://www.dutchmeters.com/index.php/product/dzt-6001/
# User manual: http://dutchmeters.com/wp-content/uploads/2017/06/DZT-6001-manual.pdf
# Register reference:  http://dutchmeters.com/wp-content/uploads/2017/04/DZT6001-Modbus.pdf

import time  

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 2, bytesize = 8,  parity='N', baudrate= 38400)
client.connect()

while True:

    # query the device with address 0x1B (unit=0x1B)
    # the last readable register has index 0x2c
    r = client.read_holding_registers(0x00,0x2c,unit=0x1B) #300=0x12c

    print "Voltage: %.1f V" % (int(r.registers[0])/10.0)
    print "Current: %.1f A" % (float(r.registers[1])/10.0)

    print "Active power: %d W" % r.registers[3]
    print "Reactive power: %d W" % r.registers[4]
    print "Apparent power: %d W" % r.registers[5]

    print "CosPhy: %.3f" % (float(r.registers[6])/1000.0)


    print "Active energy: %.2f kWh" % (float(r.registers[7])/100.0)
    print "Reactive energy: %.2f kWh" % (float(r.registers[0x11])/100.0)


    print "Bit rate: %d " % (1200 << (r.registers[0x2a] - 1))
    print "--------------"

    time.sleep (5)
