from datetime import datetime, timedelta
from time import sleep
import threading
import logging


class MotorController:
    def __init__(self, name):
        self._name = name

    def on(self):
        logging.info(f"TURN ON {self._name}")

    def off(self):
        logging.info(f"TURN OFF {self._name}")

    def name(self):
        return self._name


STIRRING_MOTOR = MotorController('STIRRER')
DOSING_PUMP = MotorController('PUMP')


class PumpController(threading.Thread):
    _quit = False
    _run_list = []
    _run_dict = {}
    _reset = False
    _active_dose = None

    def __init__(self, programs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._programs = {}
        for program in programs:
            key = program.data_key()
            self._programs[key] = program
            self._run_dict[key] = None

    def run(self):
        logging.info("Starting Pump Controller")

        while not self._quit:
            logging.debug("Pump Controller Run")
            self._reload_data()
            self._try_run_dose()
            self._menu_timeout()
            sleep(1)

        logging.info("Exiting Pump Controller")

    def _reload_data(self):
        # Only run if we don't have an entry for a given program
        self._reset_run()

        missing = None in self._run_dict.values()
        if missing:
            now = datetime.now()
            for key, p in self._programs.items():
                if not self._run_dict[key]:
                    logging.debug(f"Reload Data key:{key}")
                    next_run = p.next_run()
                    skip = False
                    if not next_run:
                        logging.debug(f"Nothing to run, look again in the next minute or so, key:{key}")
                        next_run = now + timedelta(seconds=60 - now.second)
                        skip = True

                    logging.info(f"Next Run: key:{key} next:{next_run} skip:{skip}")
                    self._run_list.append((next_run, key, skip))
                    self._run_dict[key] = next_run

            self._run_list.sort(key=lambda v: v[0])

    def _try_run_dose(self):
        now = datetime.now()
        if self._run_list and now >= self._run_list[0][0]:
            runtime, key, skip = self._run_list.pop(0)
            self._run_dict[key] = None
            if not skip:
                if now < (runtime + timedelta(minutes=1)):
                    self._active_dose = Dose(self._programs[key])
                    self._active_dose.run()
                    self._active_dose = None
                else:
                    logging.warning(f"SKIPPING PROGRAM - {key}")

    def _menu_timeout(self):
        pass

    def _reset_run(self):
        """Used by threading processor to recalculate the run list if needed"""
        if self._reset:
            self._run_list.clear()
            for key in self._run_dict:
                self._run_dict[key] = None
            self._reset = False

    def next_run(self):
        if self._run_list:
            return self._run_list[0][0]
        return None

    def print_active_dose(self):
        if self._active_dose:
            return self._active_dose.print_lines()
        return None

    def reset(self):
        """Hook into threaded processor to tell it that it needs to reset"""
        self._reset = True

    def quit(self):
        self._quit = True


class Dose:
    _done = False
    _stir = None
    _dose = None

    def __init__(self, program):
        self._program = program
        self._dose = TimedPinController(self._program.dose_seconds(), DOSING_PUMP)
        self._stir = TimedPinController(self._program.stir_seconds(), STIRRING_MOTOR)

    def run(self):
        logging.warning(f"RUNNING PROGRAM - program:{self._program.data_key()} stir:{self._stir.remaining_seconds()} "
                        f"dose:{self._dose.remaining_seconds()}")
        try:
            self._stir.start()
            while self._stir.remaining_seconds() > 0:
                sleep(0.1)

            self._dose.start()
            while self._dose.remaining_seconds() > 0:
                sleep(0.1)
        finally:
            self._dose.end()
            self._stir.end()

    def print_lines(self):
        return ['RUNNING: ' + self._program.name(), str(self._stir), str(self._dose)]


class TimedPinController:
    def __init__(self, total_seconds, motor):
        self._total_seconds = total_seconds
        self._motor = motor
        self._started = None

    def __str__(self):
        return f"{self._motor.name()}: {self.remaining_seconds()} seconds"

    def start(self):
        if not self._started:
            self._started = datetime.now()
            self._motor.on()

    def end(self):
        self._motor.off()

    def remaining_seconds(self):
        run_seconds = (datetime.now() - self._started).seconds if self._started else 0
        return self._total_seconds - run_seconds
