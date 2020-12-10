from datetime import datetime, date, time, timedelta

from daily_feeder.menu import ProgramSettingsMenuController


class Pg2(ProgramSettingsMenuController):
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

def test_5_all():
    assert Pg2(0, 0, 5, 10).next_run() == get_time(0, 0, 15)
    assert Pg2(0, 0, 5, 1434).next_run() == get_time(0, 23, 55)
    assert Pg2(0, 0, 5, 1435).next_run() == get_time(1, 0, 0)
    assert Pg2(0, 0, 5, 1439).next_run() == get_time(1, 0, 0)
    assert Pg2(0, 0, 5, 1440).next_run() == get_time(1, 0, 5)

def test_61_offset():
    assert Pg2(6, 5, 61, 0).next_run() == get_time(0, 0, 18)
    assert Pg2(6, 5, 61, 17).next_run() == get_time(0, 0, 18)
    assert Pg2(6, 5, 61, 18).next_run() == get_time(0, 1, 19)
    assert Pg2(6, 5, 61, 60*1 + 18).next_run() == get_time(0, 1, 19)
    assert Pg2(6, 5, 61, 60*1 + 19).next_run() == get_time(0, 2, 20)
    assert Pg2(6, 5, 61, 60*2 + 20).next_run() == get_time(0, 3, 21)
    assert Pg2(6, 5, 61, 60*3 + 21).next_run() == get_time(0, 4, 22)
    assert not Pg2(6, 5, 61, 60*4 + 22).next_run()
    assert Pg2(6, 5, 61, 60*5 + 23).next_run() == get_time(0, 6, 0)
    assert Pg2(6, 5, 61, 60*6 - 1).next_run() == get_time(0, 6, 0)
    assert Pg2(6, 5, 61, 60*6 + 1).next_run() == get_time(0, 7, 1)
    assert Pg2(6, 5, 61, 60*23 + 16).next_run() == get_time(0, 23, 17)
    assert Pg2(6, 5, 61, 60*23 + 17).next_run() == get_time(1, 0, 18)
    assert Pg2(6, 5, 61, 60*24 + 18).next_run() == get_time(1, 1, 19)


def test_181_0():
    assert Pg2(0, 8, 181, -1).next_run() == get_time(0, 0, 0)
    assert Pg2(0, 8, 181, 0).next_run() == get_time(0, 3, 1)
    assert Pg2(0, 8, 181, 60*3 + 1).next_run() == get_time(0, 6, 2)
    assert not Pg2(0, 8, 181, 60*6 + 2).next_run()
    assert not Pg2(0, 8, 181, 60*9 + 3).next_run()
    assert not Pg2(0, 8, 181, 60*12 + 4).next_run()
    assert not Pg2(0, 8, 181, 60*15 + 5).next_run()
    assert not Pg2(0, 8, 181, 60*18 + 6).next_run()
    assert not Pg2(0, 8, 181, 60*21 + 6).next_run()
    assert Pg2(0, 8, 181, 60*21 + 7).next_run() == get_time(1, 0, 0)
    assert Pg2(0, 8, 181, 60*24 - 1).next_run() == get_time(1, 0, 0)


def test_181_offset():
    assert Pg2(20, 4, 181, 60*20 - 1).next_run() == get_time(0, 20, 0)
    assert Pg2(20, 4, 181, 60*20 + 0).next_run() == get_time(0, 23, 1)
    assert Pg2(20, 4, 181, 60*23 + 1).next_run() == get_time(1, 2, 2)
    assert Pg2(20, 4, 181, 60*2 + 1).next_run() == get_time(0, 2, 2)
    assert not Pg2(20, 4, 181, 60*2 + 2).next_run()
    assert not Pg2(20, 4, 181, 60*5 + 3).next_run()
    assert not Pg2(20, 4, 181, 60*8 + 4).next_run()
    assert not Pg2(20, 4, 181, 60*11 + 5).next_run()
    assert not Pg2(20, 4, 181, 60*14 + 6).next_run()
    assert Pg2(20, 4, 181, 60*17 + 7).next_run() == get_time(0, 20, 0)


def test_61_all():
    start = 18
    for i in range(0,6):
        assert Pg2(6, 6, 61, 60*i).next_run() == get_time(0, i, start + i)

    assert Pg2(6, 6, 61, 60*6 - 1).next_run() == get_time(0, 6, 0)

    for i in range(6,23):
        offset = i - 6
        assert Pg2(6, 6, 61, 60*i + offset).next_run() == get_time(0, i + 1, offset + 1)

    assert Pg2(6, 6, 61, 60*24 + 17).next_run() == get_time(1, 0, 18)


def test_even_all():
    for i in range(0, 1438, 2):
        minute = i%60 + 2
        hour = int(i / 60)
        if minute == 60:
            hour += 1
            minute = 0

        assert Pg2(0, 0, 2, i).next_run() == get_time(0, hour, minute)

    assert Pg2(0, 0, 2, 1438).next_run() == get_time(1, 0, 0)
    assert Pg2(0, 0, 2, 1440).next_run() == get_time(1, 0, 2)


def get_time(day, hour, minute):
    return datetime.combine(date.today(), time(hour=hour, minute=minute)) + timedelta(days=day)

def test_load_menu():
    properties = {
        'pg.enabled': 1,
        'pg.stir_seconds': 2,
        'pg.dose_seconds': 3,
        'pg.freq_minutes': 4,
        'pg.freq_hour': 5,
        'pg.start_hour': 6,
        'pg.end_hour': 7,
    }
    printer = ""
    pg = ProgramSettingsMenuController('pg', 'Program 1')
    pg.load(properties, printer)
    values = pg.values()

    assert 7 == len(values)
    assert values[0].name() == "Enabled: True"
    assert values[1].name() == "Stir: 2 seconds"
    assert values[2].name() == "Dose: 3 seconds"
    assert values[3].name() == "Frequency: 4 minutes"
    assert values[4].name() == "Frequency: 5 hours"
    assert values[5].name() == "Start Hour: 6 AM"
    assert values[6].name() == "End Hour: 7 AM"
