from daily_feeder.other.i2c_lcd_driver import lcd
from time import sleep

# LCD Address
ADDRESS = 0x27

my_lcd = lcd(ADDRESS)

my_lcd.lcd_display_string("RPi I2C test", 1)
my_lcd.lcd_display_string(" Custom chars", 2)

sleep(2) # 2 sec delay


