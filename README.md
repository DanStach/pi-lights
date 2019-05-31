# rpi-lpd8806
This project's goal is to have example python code that runs lpd8806 lights on a raspberry pi.

## Install Instuctions
- clone repo
- wire strand to RPi 3b
  - Pi GND  (09) -> Strand GND
  - Pi MOSI (19) -> Strand DI
  - Pi SCLK (23) -> Strand CI
  - Pi +5V  (02) -> Strand +5V

*Please note:*
need to do a clean install of Raspbian OS to ensure no additional install instructions are needed

*Prior References:*
https://github.com/DanStach/rpi-ws2811/blob/master/Install.md
https://github.com/longjos/RPi-LPD8806/blob/master/README.md
https://learn.adafruit.com/digital-led-strip/wiring
https://cdn-shop.adafruit.com/datasheets/lpd8806+english.pdf


## Hardware Considerations
- RPI 3b 
  - SD = 16gb, Ram = 1gb,  CPU = 4× 1.2GHz
  - OS = Raspbian
  - neopixel = 32 lpd8806 (powered from RPI +5v pinout)
