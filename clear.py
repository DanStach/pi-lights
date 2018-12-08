import time
import random
import math
import spidev
import collections

# Instantiate SPI device
spi = spidev.SpiDev()
spi.open(0, 0)
SIZE = 160
ALL = -1
buf = []

class LedStrip:
  def __init__(self, size):
    self.size = size
    self.lights = [0x80] * size * 3
    self.zeroes = [0] * 3 * ((32+63)/64)

  def write(self):
    buf = self.lights[:]
    spi.xfer2(self.zeroes)
    spi.xfer2(buf)
    buf = self.lights[:]
    spi.xfer2(self.zeroes)
    spi.xfer2(buf)

  def init_strip(self):
    self.clr_all()

  def clr_led(self, index):
    self.lights[index*3+0] = 0x80
    self.lights[index*3+1] = 0x80
    self.lights[index*3+2] = 0x80
    self.write()

  def clr_all(self):
    self.lights = [0x80 for i in self.lights]
    self.write()

def main():
  myStrip = LedStrip(SIZE)
  myStrip.init_strip()
  myStrip.clr_all()


if __name__ == "__main__":
  main()
