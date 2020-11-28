class Name:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name


class SecondSelector(Name):
    value = 0
    max_value = 59


class MinuteSelector(Name):
    value = 0
    max_value = 59


class HourSelector(Name):
    value = 0
    max_value = 23

class MenuItem(Name):
    def __init__(self, key, name, values):
        super().__init__(name)
        self._parent = None
        self._key = key
        self._values = values

        for value in values:
            if type(value) == MenuItem:
                value._parent = self

    def parent(self):
        return self._parent

    def values(self):
        values = self._values
        if self.parent():
            values = values + [self._parent]
        return values

    def value_names(self):
        values = [value.name() for value in self._values]
        if self.parent():
            values += ['Return']
        return values


MENU = MenuItem('root', 'MAIN', values=[
    MenuItem('run_now', 'Run Now', values=[
        SecondSelector('Dose Seconds')
    ]),
    MenuItem('pg_1', 'Program 1', values=[
        SecondSelector('Stir Seconds'),
        SecondSelector('Dose Seconds'),
        MenuItem('dose_freq', 'Dose Frequence', values=[
            HourSelector('Hours'),
            MinuteSelector('Minutes'),
        ]),
        HourSelector('Start Hour'),
        HourSelector('End Hour'),
    ]),
    MenuItem('pg_2', 'Program 2', values=[
        SecondSelector('Stir Seconds'),
        SecondSelector('Dose Seconds'),
        MenuItem('dose_freq', 'Dose Frequence', values=[
            HourSelector('Hours'),
            MinuteSelector('Minutes'),
        ]),
        HourSelector('Start Hour'),
        HourSelector('End Hour'),
    ]),
    MenuItem('', 'Set Time', values=[
        HourSelector('Hour'),
        MinuteSelector('Minute'),
    ]),
])

