# orginal code found at https://github.com/vherr2/pi-lights
import time
import random
import math
import spidev
import collections

# Instantiate SPI device
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 40000000 #2019-05-30 Note: maxspeed that works on RPI3b max_speed_hz = 40000000
SIZE = 32
ALL = -1
buf = [] 

class LedStrip:
    def __init__(self, size):
        self.size = size
        self.lights = [0x80] * size * 3
        self.zeroes = [0] * 3 * int((32+63)/64)

    def write(self):
        buf = self.lights[:]
        spi.xfer2(self.zeroes)
        spi.xfer2(buf)
        buf = self.lights[:]
        spi.xfer2(self.zeroes)
        spi.xfer2(buf)

    def init_strip(self):
        for i in range(len(self.lights)):
            self.lights[i] = 0x80
        self.write()

    def set_led_no_write(self, red, green, blue, index):
        self.lights[index*3+0] = 0x80 | green
        self.lights[index*3+1] = 0x80 | red
        self.lights[index*3+2] = 0x80 | blue

    def set_leds_all_no_write(self, red, green, blue):
        for i in range(0, len(self.lights), 3):
            self.lights[i+0] = 0x80 | green
            self.lights[i+1] = 0x80 | red
            self.lights[i+2] = 0x80 | blue

    def set_led(self, red, green, blue, index):
        self.set_led_no_write(red, green, blue, index)
        self.write()
    def set_leds_all(self, red, green, blue):
        self.set_leds_all_no_write(red, green, blue)
        self.write()

    def clr_led(self, index):
        self.lights[index*3+0] = 0x80
        self.lights[index*3+1] = 0x80
        self.lights[index*3+2] = 0x80
        self.write()

    def clr_leds_all(self):
        for i in range(len(self.lights)):
            self.lights[i] = 0x80
        self.write()

    def basic_test(self, red, blue, green):
        for i in range(self.size):
            self.set_led(red, 0, 0, i)
            time.sleep(0.05)
            self.set_led(0, blue, 0, i)
            time.sleep(0.05)
            self.set_led(0, 0, green, i)
            time.sleep(0.05)
            self.set_led(red, blue, green, i)
            time.sleep(0.05)

        for i in range(self.size):
            self.clr_led(i)
            time.sleep(0.1)

        self.set_led(red, blue, green, ALL)
        time.sleep(0.5)
        self.clr_led(ALL)
        time.sleep(0.5)cd

def main():
    myStrip = LedStrip(SIZE)
    myStrip.init_strip()
    myStrip.clr_leds_all()
    myStrip.set_leds_all(1,0,0) #red
    time.sleep(1)
    myStrip.set_leds_all(0,1,0) #green
    time.sleep(1)
    myStrip.set_leds_all(0,0,1) #blue
    time.sleep(1)
    myStrip.set_leds_all(1,1,1) #white
    time.sleep(1)

if __name__ == "__main__":
    main()