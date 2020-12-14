Raspberry Pi controlled daily fishtank feeder.

# Raspberry Pi python3 setup
```
sudo apt update
sudo apt full-upgrade
apt-get install python3-pip
sudo apt install python3-gpiozero
sudo apt-get install python-smbus
sudo apt-get install i2c-tools

sudo apt-get install python3-pil
sudo usermod -a -G spi,gpio,i2c pi

sudo apt-get install pigpiod
pip3 install pigpio
pip3 install pigpio-encoder

-------
sudo pigpiod
python3 main.py
```

# Components
LCD (I2C)
- 1 Header, 3 Rows

Rotary Encoder
- Rotate for choosing
- Press for selection
- clk=pin 17
- dt=18
- sw=27

Magnetic Mixing Motor
- Pin ?
- Uses a magnetic stirrer to mix food before dosing

Pump
- Pin ?
- Pumps food after Pumping

# Testing
The LCD / Encoder will be mimiced if run from your local machine using
python "curses" and the arrow keys.