import struct
import time
import RPi.GPIO as GPIO
import smbus

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)

print(" ")


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


def QuickStart(smbus_value):
    address = 0x36
    smbus_value.write_word_data(address, 0x06, 0x4000)


def PowerOnReset(smbus_value):
    address = 0x36
    smbus_value.write_word_data(address, 0xfe, 0x0054)


#PowerOnReset(bus)
QuickStart(bus)

print("Initialize the MAX17040 ......")

while True:
    print("++++++++++++++++++++")
    print("Voltage:%5.2fV" % readVoltage(bus))
    print("Battery:%5i%%" % readCapacity(bus))
    if readCapacity(bus) == 100:
        print("Battery FULL")
    if readCapacity(bus) < 5:
        print("Battery LOW")

    if GPIO.input(4) == GPIO.HIGH:
        print("Power Adapter Plug In ")

    if GPIO.input(4) == GPIO.LOW:
        print("Power Adapter Unplug")

    print("++++++++++++++++++++")
    time.sleep(2)
