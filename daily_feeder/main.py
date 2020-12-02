from daily_feeder.menu import MENU
from daily_feeder.encoder.rotary import watch
from daily_feeder.printer.lcd import print as printer

watch(MENU.controller(printer))
