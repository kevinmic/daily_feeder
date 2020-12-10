import logging

import daily_feeder.data_saver
from daily_feeder.encoder.rotary import watch
from daily_feeder.menu import SecondCounter, MenuController, ProgramSettingsMenuController, HourCounter, MinuteCounter
from daily_feeder.printer.lcd import print_lcd
from daily_feeder.pump.controller import PumpController


def load_menu(properties, printer):
    run_now_c = SecondCounter(key='', name='Dose')
    run_now_m = MenuController('run_now', 'Run Now', values=[run_now_c])
    program_1 = ProgramSettingsMenuController('pg_1', 'Program 1')
    program_2 = ProgramSettingsMenuController('pg_2', 'Program 2')
    clock_m = MenuController('', 'Set Time', values=[
        HourCounter(key='', name='Hour'),
        MinuteCounter(key='', name='Minute'),
    ])

    main_menu = MenuController('', 'MAIN', values=[
        run_now_m,
        program_1,
        program_2,
        clock_m,
    ])

    main_menu.load(properties, printer)
    return (main_menu, [program_1, program_2])


MAIN_MENU, programs = load_menu(daily_feeder.data_saver.read(), print_lcd)
pump_controller = PumpController(programs)
pump_controller.start()

try:
    watch(MAIN_MENU.displayer())
except KeyboardInterrupt:
    pump_controller.quit()
except:
    logging.exception("Unexpected error")
    pump_controller.quit()
