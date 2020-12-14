import logging
from datetime import datetime, timedelta

max_display = 3

class MenuDisplayer:
    _curr_index = 0

    def __init__(self, menu, printer):
        self._menu = menu
        self._printer = printer

    def max_count(self):
        has_parent = 1 if self._menu.parent else 0
        return len(self._menu.values()) + has_parent

    def current_count(self):
        return self._curr_index

    def display_index(self, selected_index):
        self._curr_index = selected_index
        items = self._menu.value_names()
        if self._menu.parent:
            items.append("Return")

        min_index = 0
        if selected_index - max_display >= 0:
            min_index = selected_index - max_display + 1
            selected_index = max_display - 1

        print_items = []
        for item in enumerate(items[min_index:min_index+max_display]):
            index = item[0]
            text = item[1]
            if selected_index == index:
                text = "> " + text
            else:
                text = "  " + text
            print_items.append(text)

        self._printer(self._menu.name(), print_items)

    def select_index(self, selected_index):
        next_menu = self
        values = self._menu.values()
        if len(values) > selected_index:
            next_menu = values[selected_index].displayer()
            if isinstance(next_menu, MenuDisplayer):
                # Reset the selected index when going to a child
                next_menu._curr_index = 0
        elif self._menu.parent:
            # Keep previous selected index of parent
            next_menu = self._menu.parent.displayer()

        return next_menu

class CounterDisplayer:
    def __init__(self, counter, printer):
        self._counter = counter
        self._printer = printer

    def max_count(self):
        return self._counter.max()

    def current_count(self):
        return self._counter.value

    def display_index(self, selected_index):
        name = self._counter.value_as_string(selected_index)
        self._printer(self._counter.parent.name(), ['', self._counter.name(), f'>     {name}'])

    def select_index(self, selected_index):
        self._counter.value = selected_index
        self._counter.write()

        return self._counter.parent_displayer()


class MainDisplayer(MenuDisplayer):
    _pump_controller = None

    def display_index(self, selected_index):
        if not self._display_pump_active():
            now = datetime.now()
            values = [
                now.strftime("Time: %I:%M:%S %p"),
                self._next_run_str(),
            ]
            self._printer("DAILY FEEDER", values)

    def pump_controller(self, pump_controller):
        self._pump_controller = pump_controller

    def _display_pump_active(self):
        if self._pump_controller:
            active_run = self._pump_controller.print_active_dose()
            if active_run:
                self._printer("DAILY FEEDER", active_run)
                return True

        return False

    def _next_run_str(self):
        return_str = "Next: Off"
        if self._pump_controller:
            next_run = self._pump_controller.next_run()
            if next_run:
                seconds = (next_run - datetime.now()).seconds + 1
                delta_str = str(timedelta(seconds=seconds))
                if delta_str.startswith('0:'):
                    delta_str = "0" + delta_str
                return_str = f"Next: {delta_str}"

        return return_str
