from datetime import datetime, timedelta
from time import sleep
import threading
import logging


class PumpController(threading.Thread):
    _quit = False
    _run_list = []
    _run_dict = {}

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
                    self._run_dose(self._programs[key])
                else:
                    logging.warning(f"SKIPPING PROGRAM - {key}")

    def _run_dose(self, program):
        dose = program.dose_seconds()
        stir = program.stir_seconds()
        logging.warning(f"RUNNING PROGRAM - program:{program.data_key()} stir:{stir} dose:{dose}")

    def _menu_timeout(self):
        pass

    def quit(self):
        self._quit = True;