from daily_feeder.displayer import MenuDisplayer, CounterDisplayer


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


class ProgramSettings(MenuItem):
    def __init__(self, *args, **kwargs):
        values=[
            SecondCounter(key='stir_seconds', name='Stir Seconds'),
            SecondCounter(key='dose_seconds', name='Dose Seconds'),
            MenuItem('dose_freq', 'Dose Frequency', values=[
                HourCounter(key='hour', name='Hours'),
                MinuteCounter(key='minutes', name='Minutes'),
            ]),
            HourCounter(key='start_hour', name='Start Hour'),
            HourCounter(key='end_hour', name='End Hour'),
        ]
        super().__init__(values=values, *args, **kwargs)


MENU = MenuItem('root', 'MAIN', values=[
    MenuItem('run_now', 'Run Now', values=[
        SecondCounter(key='', name='Dose Seconds')
    ]),
    ProgramSettings('pg_1', 'Program 1'),
    ProgramSettings('pg_1', 'Program 2'),
    MenuItem('', 'Set Time', values=[
        HourCounter(key='', name='Hour'),
        MinuteCounter(key='', name='Minute'),
    ]),
])

