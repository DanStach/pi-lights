# orginal code found at https://github.com/vherr2/pi-lights
import time
import random
import math
import spidev
import collections

# Instantiate SPI device
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 4000 #2019-05-30 Note: maxspeed that works on RPI3b max_speed_hz = 40000000
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
        if (index == ALL):
            for i in range(0, len(self.lights), 3):
                self.lights[i+0] = 0x80 | green
                self.lights[i+1] = 0x80 | red
                self.lights[i+2] = 0x80 | blue
        else:
            self.lights[index*3+0] = 0x80 | green
            self.lights[index*3+1] = 0x80 | red
            self.lights[index*3+2] = 0x80 | blue

    def set_led(self, red, green, blue, index):
        self.set_led_no_write(red, green, blue, index)
        self.write()

    def clr_led(self, index):
        if (index == ALL):
            for i in range(len(self.lights)):
                self.lights[i] = 0x80
        else:
            self.lights[index*3+0] = 0x80
            self.lights[index*3+1] = 0x80
            self.lights[index*3+2] = 0x80
        self.write()

    def fade_in(self, red_max, green_max, blue_max, interval, index):
        tmp_red = 0
        tmp_green = 0
        tmp_blue = 0
        for i in range(interval):
            tmp_red = min(tmp_red+int(math.ceil(float(red_max)/interval)), red_max)
            tmp_green = min(tmp_green+int(math.ceil(float(green_max)/interval)), green_max)
            tmp_blue = min(tmp_blue+int(math.ceil(float(blue_max)/interval)), blue_max)
            self.set_led(tmp_red, tmp_green, tmp_blue, index)

    def fade_out(self, interval, index):
        if (index == ALL):
            orig_green = self.lights[0]&127
            orig_red = self.lights[1]&127
            orig_blue = self.lights[2]&127
        else:
            orig_green = self.lights[index*3+0]&127
            orig_red = self.lights[index*3+1]&127
            orig_blue = self.lights[index*3+2]&127
        tmp_red = orig_red
        tmp_green = orig_green
        tmp_blue = orig_blue
        for i in range(interval*2):
            tmp_red = max(tmp_red-int(math.ceil(float(orig_red)/interval)), 0)
            tmp_green = max(tmp_green-int(math.ceil(float(orig_green)/interval)), 0)
            tmp_blue = max(tmp_blue-int(math.ceil(float(orig_blue)/interval)), 0)
            self.set_led(tmp_red, tmp_green, tmp_blue, index)

    def strobe(self, red_max, green_max, blue_max, interval, index):
        self.fade_in(red_max, green_max, blue_max, interval, index)
        self.fade_out(interval, index)

    def rand_strobe(self, max_val, interval, index):
        self.strobe(random.randrange(0, max_val), random.randrange(0, max_val), random.randrange(0, max_val), interval, index)

    def shift(self):
        tmp = collections.deque(self.lights)
        tmp.rotate(3)
        for i in range(len(self.lights)):
            self.lights[i] = tmp[i]
        self.write()

    def shift_init(self, red_max, green_max, blue_max):
        for i in range(self.size):
            if (i%3 == 0):
                self.set_led_no_write(red_max, 0, 0, i)
            if (i%3 == 1):
                self.set_led_no_write(0, green_max, 0, i)
            if (i%3 == 2):
                self.set_led_no_write(0, 0, blue_max, i)
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
        time.sleep(0.5)

    def fade_test(self, max_val, interval):
        for i in range(self.size):
            self.rand_strobe(max_val, interval, i)
        self.rand_strobe(max_val, interval, ALL)

def main():
    myStrip = LedStrip(SIZE)
    myStrip.init_strip()
    myStrip.clr_led(ALL)
    myStrip.shift_init(127,127,127)
    #while True:
    #    myStrip.shift()
    myStrip.basic_test(1, 1, 1)
    myStrip.fade_test(64, 20)
    
    while True:
        
        myStrip.rand_strobe(20, 20, ALL)

if __name__ == "__main__":
    main()