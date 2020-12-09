from daily_feeder.menu import MAIN_MENU, PROGRAM_1, PROGRAM_2
from daily_feeder.encoder.rotary import watch
from daily_feeder.printer.lcd import print_lcd
from daily_feeder.pump.controller import PumpController


pump_controller = PumpController()
pump_controller.start()

try:
    watch(MAIN_MENU.controller(print_lcd))
except:
    pump_controller.quit()
