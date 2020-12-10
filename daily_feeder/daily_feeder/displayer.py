import logging


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

        print(",".join(items))
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
