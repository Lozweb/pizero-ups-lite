import smbus
import struct
import time

ADDRESS = 0x36


def readVoltage(bus):
    try:
        read = bus.read_word_data(ADDRESS, 1)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 / 1000 / 16
        return voltage
    except:
        return 0.0


def readCapacity(bus):
    try:
        read = bus.read_word_data(ADDRESS, 3)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped / 256
        return capacity
    except:
        return 0.0


def QuickStart(bus):
    address = 0x36
    bus.write_word_data(address, 0x06, 0x4000)


def PowerOnReset(bus):
    address = 0x36
    bus.write_word_data(address, 0xfe, 0x0054)


bus = smbus.SMBus(1)
PowerOnReset(bus)
QuickStart(bus)

while True:
    print("Voltage: %5.2fV" % readVoltage(bus))
    print("Capacity: %5i%%" % readCapacity(bus))
    time.sleep(1)
