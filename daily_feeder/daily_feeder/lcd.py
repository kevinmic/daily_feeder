from PIL import ImageFont
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from time import sleep


# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface

font = ImageFont.truetype("OpenSans-Regular.ttf", 13)
# font = ImageFont.truetype("OpenSans-Bold.ttf", 13)

serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)

max_display = 3

print('INIT LCD')
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((3, 0), 'BOOTING', font=font, fill="white")

def print_menu(header, items, selected_index):
    with canvas(device) as draw:
        menuStr = ','.join(items)
        print('Print Menu:', menuStr)
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        if header:
            draw.text((3, 0), header, font=font, fill="white")

        min_index = 0
        if selected_index - max_display >= 0:
            min_index = selected_index - max_display + 1
            selected_index = max_display - 1

        print('Min/Max/Total:', min_index, min_index + max_display, len(items))
        for item in enumerate(items[min_index:min_index+max_display]):
            index = item[0]
            text = item[1]
            if selected_index == index:
                text = "> " + text
            else:
                text = "  " + text
            draw.text((3, (index+1)*13), text, font=font, fill="white")
