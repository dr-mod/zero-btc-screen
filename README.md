# Zero BTC Screen
Bitcoin stock price for your RPi Zero

![display](display.jpg)

## Hardware
* Raspberry Pi Zero W (or any other RPi)
* Waveshare 2.13" eInk display (supports multiple versions)

## Installation
1. Turn on SPI via `sudo raspi-config`
    ```
    Interfacing Options -> SPI
    ```
2. Install eInk display drivers
    ```
    git clone https://github.com/waveshare/e-Paper.git
    cd e-Paper/RaspberryPi_JetsonNano/python/
    pip3 install $(pwd)
    ```
    for more information refer to: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
3. Download Zero BTC Screen
    ```
    cd ~
    git clone https://github.com/dr-mod/zero-btc-screen.git
    ```
4. Run it 
    ```
    cd zero-btc-screen
    python3 main.py
    ```
5. To make it run on startup
    1. `nano /etc/rc.local` 
    2. Add one the following before `exit 0`
    ```
    /usr/bin/python3 /home/pi/zero-btc-screen/main.py&
    ```
    conversely, you can run in `screen`
    ```
    su - pi -c "/usr/bin/screen -dm sh -c 'cd /home/pi/zero-btc-screen/ && /usr/bin/python3 /home/pi/zero-btc-screen/main.py'"
    ```

## eInk multiple versions

The application supports multiple Waveshare displays.
A required display could be configured through an environment `BTC_SCREEN_DRIVER`

A value has to be the exact *epd...* name which can found here: 
https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd

There is implemented support for:
* epd2in13_V2 (default)
* epd2in13b_V3