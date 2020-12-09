from daily_feeder.menu import MAIN_MENU
from daily_feeder.encoder.rotary import watch
from daily_feeder.printer.lcd import print_lcd


watch(MAIN_MENU.controller(print_lcd))
