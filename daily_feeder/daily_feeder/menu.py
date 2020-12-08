from daily_feeder.displayer import MenuDisplayer, CounterDisplayer
from daily_feeder.data_saver import read, write


class BaseDisplayer:
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

    def controller(self, printer):
        return self._controller(self, printer)

    def parent_controller(self, printer):
        return self._parent.controller(printer)

    def data_key(self):
        data_key = self._key
        if data_key:
            parent = self.parent
            while parent:
                print(f"curr_key:{data_key} parent:{parent}")
                if parent._key:
                    data_key = parent._key + '.' + data_key
                parent = parent.parent
        return data_key

    def _load(self, properties):
        pass


class Counter(BaseDisplayer):
    _value = 0

    def __init__(self, max, value_name_postpend=None, controller=CounterDisplayer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = max
        self._value_name_postpend = value_name_postpend

        self._controller = controller

    def value_as_string(self, count = None):
        value = count if count else self._value
        value = str(value)
        if self._value_name_postpend:
            value += self._value_name_postpend
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
            print(f"WRITING KEY:{key} value:{self._value}")
            write({key: self._value})

    def _load(self, properties):
        key = self.data_key()
        if key and key in properties:
            self._value = int(properties[key])


class SecondCounter(Counter):
    def __init__(self, *args, **kwargs):
        super().__init__(60, ' seconds', *args, **kwargs)


class MinuteCounter(Counter):
    def __init__(self, *args, **kwargs):
        super().__init__(60, ' mintues', *args, **kwargs)


class HourCounter(Counter):
    def __init__(self, *args, **kwargs):
        super().__init__(24, ' hours', *args, **kwargs)


class AmPmHourCounter(Counter):
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

class MenuItem(BaseDisplayer):
    _controller = MenuDisplayer

    def __init__(self, key, name, values):
        super().__init__(key=key, name=name)
        self._parent = None
        self._key = key
        self._values = values

        for value in values:
            value.parent = self

    def values(self):
        values = self._values
        if self.parent:
            values = values + [self._parent]
        return values

    def value_names(self):
        values = [value.name() for value in self._values]
        if self.parent:
            values += ['Return']
        return values

    def _load(self, properties):
        for value in self._values:
            value._load(properties)

class ProgramSettings(MenuItem):
    def __init__(self, *args, **kwargs):
        values=[
            SecondCounter(key='stir_seconds', name='Stir'),
            SecondCounter(key='dose_seconds', name='Dose'),
            MinuteCounter(key='freq_minutes', name='Frequency'),
            HourCounter(key='freq_hour', name='Frequency'),
            AmPmHourCounter(key='start_hour', name='Start Hour'),
            AmPmHourCounter(key='end_hour', name='End Hour'),
        ]
        super().__init__(values=values, *args, **kwargs)

RUN_NOW_C = SecondCounter(key='', name='Dose')
RUN_NOW_M = MenuItem('run_now', 'Run Now', values=[RUN_NOW_C])
PROGRAM_1 = ProgramSettings('pg_1', 'Program 1')
PROGRAM_2 = ProgramSettings('pg_2', 'Program 2')
CLOCK_M = MenuItem('', 'Set Time', values=[HourCounter(key='', name='Hour'), MinuteCounter(key='', name='Minute'), ])

MAIN_MENU = MenuItem('', 'MAIN', values=[
    RUN_NOW_M,
    PROGRAM_1,
    PROGRAM_2,
    CLOCK_M,
])

MAIN_MENU._load(read())

