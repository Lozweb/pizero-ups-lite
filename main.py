import smbus
import struct


class UpsLite:

    def __init__(self, bus=1, bus_adresse=0x36, volt_adress=1, capacity_address=2):
        # ups-lite v1.2 default pin GPIO2, GPIO3 mode i2c => bus=1 bus_ad = 0x36, volt=1, capacity=2
        self.bus = smbus.SMBus(bus)
        self.bus_adresse = bus_adresse
        self.volt_address = volt_adress
        self.capacity_address = capacity_address
        self.quickStart()
        self.powerOnReset()

    def read_voltage(self):
        return self.read_formated_data(self.volt_address) * 1.25 / 1000 / 16

    def read_capacity(self):
        return self.read_formated_data(self.capacity_address) / 256

    def read_formated_data(self, address):
        return struct.unpack("<H", struct.pack(">H", self.bus.read_word_data(self.bus_adresse, address)))[0]

    def quickStart(self):
        self.bus.write_word_data(self.bus_adresse, 0x06, 0x4000)

    def powerOnReset(self):
        self.bus.write_word_data(self.bus_adresse, 0xfe, 0x0054)

    def print_value(self, value: str):
        if value == "voltage":
            print("Voltage: %5.2fV" % self.read_voltage())
        elif value == "capacity":
            print("Capacity: %5i%%" % self.read_capacity())
        else:
            print("Unknown value please try with voltage or capacity")
