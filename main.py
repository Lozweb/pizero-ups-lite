import struct
import time
import smbus


def readVoltage(smbus_value):
    address = 0x36
    read = smbus_value.read_word_data(address, 0X02)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 / 1000 / 16
    return voltage


def readCapacity(smbus_value):
    address = 0x36
    read = smbus_value.read_word_data(address, 0X04)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256
    return capacity


bus = smbus.SMBus(1)

while True:
    print("++++++++++++++++++++")
    print("Voltage:%5.2fV" % readVoltage(bus))
    print("Battery:%5i%%" % readCapacity(bus))
    if readCapacity(bus) == 100:
        print("Battery FULL")
    if readCapacity(bus) < 5:
        print("Battery LOW")
    print("++++++++++++++++++++")
    time.sleep(2)
