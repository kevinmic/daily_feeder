class Name:
    def __init__(self, key, name):
        self._key = key
        self._name = name

    def name(self):
        return self._name


class NameValue(Name):
    _value = 0

    def __init__(self, max, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = max

    def name(self):
        return f'{super().name()}: {self._value}'

    def max(self):
        return self._max


class SecondSelector(NameValue):
    def __init__(self, *args, **kwargs):
        super().__init__(59, *args, **kwargs)


class MinuteSelector(NameValue):
    def __init__(self, *args, **kwargs):
        super().__init__(59, *args, **kwargs)


class HourSelector(NameValue):
    def __init__(self, *args, **kwargs):
        super().__init__(23, *args, **kwargs)


class MenuItem(Name):
    def __init__(self, key, name, values):
        super().__init__(key=key, name=name)
        self._parent = None
        self._key = key
        self._values = values

        for value in values:
            if isinstance(value, MenuItem):
                value.parent = self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

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
            SecondSelector(key='stir_seconds', name='Stir Seconds'),
            SecondSelector(key='dose_seconds', name='Dose Seconds'),
            MenuItem('dose_freq', 'Dose Frequency', values=[
                HourSelector(key='hour', name='Hours'),
                MinuteSelector(key='minutes', name='Minutes'),
            ]),
            HourSelector(key='start_hour', name='Start Hour'),
            HourSelector(key='end_hour', name='End Hour'),
        ]
        super().__init__(values=values, *args, **kwargs)


MENU = MenuItem('root', 'MAIN', values=[
    MenuItem('run_now', 'Run Now', values=[
        SecondSelector(key='', name='Dose Seconds')
    ]),
    ProgramSettings('pg_1', 'Program 1'),
    ProgramSettings('pg_1', 'Program 2'),
    MenuItem('', 'Set Time', values=[
        HourSelector(key='', name='Hour'),
        MinuteSelector(key='', name='Minute'),
    ]),
])

