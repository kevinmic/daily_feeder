import logging
import threading
from time import sleep

import daily_feeder.data_saver
from daily_feeder.displayer import MainDisplayer
from daily_feeder.encoder.rotary import watch, refresh_callback
from daily_feeder.menu import SecondCounter, MenuController, ProgramSettingsMenuController, HourCounter, MinuteCounter
from daily_feeder.printer.lcd import print_lcd
from daily_feeder.pump.thread_controller import PumpController
from daily_feeder.data_saver import add_write_hook


class RefreshDisplay(threading.Thread):
    _quit = False

    def __init__(self, refresh_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_callback = refresh_callback

    def run(self):
        logging.info("Starting Refresh Thread")

        while not self._quit:
            sleep(1)
            self.refresh_callback()

        logging.info("Quitting Refresh Thread")

    def quit(self):
        self._quit = True


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

    starting_view = MenuController('', 'Daily Feeder', displayer=MainDisplayer, values=[main_menu])
    starting_view.load(properties, printer)
    return starting_view, [program_1, program_2]


STARTING_VIEW, programs = load_menu(daily_feeder.data_saver.read(), print_lcd)

controller = PumpController(programs)
STARTING_VIEW.displayer().pump_controller(controller)
threads = [controller, RefreshDisplay(refresh_callback)]

add_write_hook(controller.reset)
try:
    for thread in threads:
        thread.start()
    watch(STARTING_VIEW.displayer())
except KeyboardInterrupt:
    logging.exception("Unexpected error")
finally:
    for thread in threads:
        thread.quit()
