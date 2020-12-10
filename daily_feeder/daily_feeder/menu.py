from datetime import date, datetime, time, timedelta

from daily_feeder.data_saver import write
from daily_feeder.displayer import MenuDisplayer, CounterDisplayer
from daily_feeder.minute_comparer import allowed_minutes_checker


class BaseController:
    _displayer = None

    def __init__(self, key, name):
        self._key = key
        self._name = name
        self._parent = None

    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def displayer(self):
        return self._displayer_inst

    def parent_displayer(self):
        return self._parent.displayer()

    def data_key(self):
        data_key = self._key
        if data_key:
            parent = self.parent
            while parent:
                if parent._key:
                    data_key = parent._key + '.' + data_key
                parent = parent.parent
        return data_key

    def load(self, properties, printer):
        self._displayer_inst = self._displayer(self, printer)


class CounterController(BaseController):
    _value = 0
    _displayer = CounterDisplayer

    def __init__(self, max, value_postfix=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = max
        self._value_postfix = value_postfix

    def value_as_string(self, count=None):
        value = count if count is not None else self._value
        value = str(value)
        if self._value_postfix:
            value += self._value_postfix
        return value

    def name(self, count = None):
        value = self.value_as_string(count)
        return f'{super().name()}: {value}'

    def max(self):
        return self._max

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def write(self):
        key = self.data_key()
        if key:
            write({key: self._value})

    def load(self, properties, printer):
        super().load(properties, printer)
        key = self.data_key()
        if key and key in properties:
            self._value = int(properties[key])


class BooleanCounter(CounterController):
    def __init__(self, *args, **kwargs):
        super().__init__(2, *args, **kwargs)

    def value_as_string(self, count = None):
        value = count if count else self._value
        return 'True' if value else 'False'


class SecondCounter(CounterController):
    def __init__(self, *args, **kwargs):
        super().__init__(60, ' seconds', *args, **kwargs)


class MinuteCounter(CounterController):
    def __init__(self, *args, **kwargs):
        super().__init__(60, ' minutes', *args, **kwargs)


class HourCounter(CounterController):
    def __init__(self, *args, **kwargs):
        super().__init__(24, ' hours', *args, **kwargs)


class AmPmHourCounter(CounterController):
    def __init__(self, *args, **kwargs):
        super().__init__(24, *args, **kwargs)

    def value_as_string(self, count = None):
        index = count if count else self._value
        am_pm = 'AM' if index < 12 else 'PM'
        if index == 0:
            index = 12
        elif index > 12:
            index -= 12
        return f'{index} {am_pm}'

class MenuController(BaseController):
    _displayer = MenuDisplayer

    def __init__(self, key, name, values):
        super().__init__(key=key, name=name)
        self._parent = None
        self._key = key
        self._values = values

        for value in values:
            value.parent = self

    def values(self):
        return self._values

    def value_names(self):
        return [value.name() for value in self._values]

    def load(self, properties, printer):
        super().load(properties, printer)
        for value in self._values:
            value.load(properties, printer)


def current_minute_of_day():
    now = datetime.now()
    return now.hour * 60 + now.minute


class ProgramSettingsMenuController(MenuController):
    def __init__(self, *args, **kwargs):
        self._enabled = BooleanCounter(key='enabled', name='Enabled')
        self._stir_seconds = SecondCounter(key='stir_seconds', name='Stir')
        self._dose_seconds = SecondCounter(key='dose_seconds', name='Dose')
        self._frequency_minutes = MinuteCounter(key='freq_minutes', name='Frequency')
        self._frequency_hours = HourCounter(key='freq_hour', name='Frequency')
        self._start_hour = AmPmHourCounter(key='start_hour', name='Start Hour')
        self._end_hour = AmPmHourCounter(key='end_hour', name='End Hour')
        values=[
            self._enabled,
            self._stir_seconds,
            self._dose_seconds,
            self._frequency_minutes,
            self._frequency_hours,
            self._start_hour,
            self._end_hour,
        ]
        super().__init__(values=values, *args, **kwargs)

    def next_run(self):
        if not self.enabled():
            return None

        increment = self.frequency_hours() * 60 + self.frequency_minutes()
        allowed_minutes = allowed_minutes_checker(self.start_hour() * 60, self.end_hour() * 60)
        start_minutes = self.start_hour() * 60

        curr_minute = self.current_minute_of_day()
        day_inc = 0
        if curr_minute < start_minutes:
            # if current minutes are before start_minutes then add a day
            day_inc = 1440

        # Find how far we should increment current time to reach the next offset
        increment_offset = (start_minutes - (curr_minute + day_inc)) % increment
        if increment_offset == 0:
            # the offset is now() so jump to the next offset
            increment_offset = increment

        curr_datetime = datetime.combine(date.today(), time()) + timedelta(minutes=curr_minute)
        next_offset = datetime.combine(date.today(), time()) + timedelta(minutes=curr_minute + increment_offset)
        start_datetime = datetime.combine(date.today(), time(hour=self.start_hour()))

        if start_datetime < curr_datetime:
            # We are trying to detect when the offset crosses the start boundry. When start is before
            # current this can only happen on the next day's start boundary
            start_datetime = start_datetime + timedelta(days=1)

        if curr_datetime < start_datetime and next_offset >= start_datetime:
            # If the current time and the offset time crosses the start boundary, then set
            # the next offset to the start hour
            next_offset = start_datetime

        if (next_offset.hour * 60 + next_offset.minute) in allowed_minutes:
            return next_offset
        return None

    def current_minute_of_day(self):
        return current_minute_of_day()

    def enabled(self):
        return self._enabled.value

    def stir_seconds(self):
        return self._stir_seconds.value

    def dose_seconds(self):
        return self._dose_seconds.value

    def frequency_minutes(self):
        return self._frequency_minutes.value

    def frequency_hours(self):
        return self._frequency_hours.value

    def start_hour(self):
        return self._start_hour.value

    def end_hour(self):
        return self._end_hour.value
