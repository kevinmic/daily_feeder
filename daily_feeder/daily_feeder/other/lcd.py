
from PIL import ImageFont
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from time import sleep


# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
#font = ImageFont.truetype("OpenSans-Regular.ttf", 13)
font = ImageFont.truetype("OpenSans-Bold.ttf", 13)

serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)

text = ["Hello World"]
while True:
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        for i in range(len(text)):
            draw.text((3, i*13), text[i], font=font, fill="white")
    text.insert(0, input())
    if len(text) > 10:
        break
