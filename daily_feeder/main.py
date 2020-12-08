from daily_feeder.menu import MENU
from daily_feeder.encoder.rotary import watch
from daily_feeder.printer.lcd import print_lcd

watch(MENU.controller(print_lcd))
