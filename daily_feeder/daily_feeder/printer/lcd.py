from PIL import ImageFont
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010

font = ImageFont.truetype("OpenSans-Regular.ttf", 13)

serial = i2c(port=1, address=0x3C)

device = ssd1306(serial)

start_column = 3
max_display = 3
row_height = 13

def print(header, lines):
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        if header:
            draw.text((start_column, 0), header, font=font, fill="white")

        for index, text in enumerate(lines):
            draw.text((start_column, (index+1)*row_height), text, font=font, fill="white")
