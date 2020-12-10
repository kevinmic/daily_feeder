from datetime import date, datetime, time, timedelta
from daily_feeder.menu import ProgramSettings

from daily_feeder.minute_comparer import allowed_minutes_checker

class Pg2(ProgramSettings):
    def __init__(self, start_hour, end_hour, increment, current_minute_of_day):
        self._start_hour = start_hour
        self._end_hour = end_hour
        self._increment = increment
        self._current_minute_of_day = current_minute_of_day

    def current_minute_of_day(self):
        return self._current_minute_of_day

    def enabled(self):
        return True

    def frequency_minutes(self):
        return self._increment

    def frequency_hours(self):
        return 0

    def start_hour(self):
        return self._start_hour

    def end_hour(self):
        return self._end_hour

def next_run(start_hour, end_hour, increment, current_minute_of_day):
    return Pg2(start_hour, end_hour, increment, current_minute_of_day).next_run()
