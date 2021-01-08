# Zero BTC Screen
Bitcoin stock price for your RPi Zero

#### Display output example:
![display](display.jpg)

## Hardware
* Raspberry Pi Zero W (or any other RPi)
* Waveshare 2.13" eInk display

## Installation
1. Turn on SPI via `sudo raspi-config`
2. Install eInk display drivers following the manual: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
3. Copy the _waveshare_epd_ drivers to this folder
3. Run with `python3 main.py` or add it to your `/etc/rc.local` with something like this su - pi -c "/usr/bin/screen -dm sh -c 'cd /home/pi/zero-btc-screen/ && /usr/bin/python3 /home/pi/zero-btc-screen/main.py'"

