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
    _controller = CounterDisplayer

    def __init__(self, max, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = max

    def name(self, count = None):
        value = count if count else self._value
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
        super().__init__(59, *args, **kwargs)


class MinuteCounter(Counter):
    def __init__(self, *args, **kwargs):
        super().__init__(59, *args, **kwargs)


class HourCounter(Counter):
    def __init__(self, *args, **kwargs):
        super().__init__(23, *args, **kwargs)


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
            SecondCounter(key='stir_seconds', name='Stir Seconds'),
            SecondCounter(key='dose_seconds', name='Dose Seconds'),
            HourCounter(key='freq_hour', name='Frequency Hours'),
            MinuteCounter(key='freq_minutes', name='Frequency Minutes'),
            HourCounter(key='start_hour', name='Start Hour'),
            HourCounter(key='end_hour', name='End Hour'),
        ]
        super().__init__(values=values, *args, **kwargs)

RUN_NOW_C = SecondCounter(key='', name='Dose Seconds')
RUN_NOW_M = MenuItem('run_now', 'Run Now', values=[RUN_NOW_C])
PROGRAM_1 = ProgramSettings('pg_1', 'Program 1')
PROGRAM_2 = ProgramSettings('pg_1', 'Program 2')
CLOCK_M = MenuItem('', 'Set Time', values=[HourCounter(key='', name='Hour'), MinuteCounter(key='', name='Minute'), ])

MAIN_MENU = MenuItem('', 'MAIN', values=[
    RUN_NOW_M,
    PROGRAM_1,
    PROGRAM_2,
    CLOCK_M,
])

MAIN_MENU._load(read())

