max_display = 3

class MenuDisplayer:
    def __init__(self, menu, printer):
        self._menu = menu
        self._printer = printer

    def max_count(self):
        return len(self._menu.values())

    def current_count(self):
        return 0

    def display_index(self, selected_index):
        items = self._menu.value_names()
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
        return self._menu.values()[selected_index].controller(self._printer)

class CounterDisplayer:
    def __init__(self, counter, printer):
        self._counter = counter
        self._printer = printer

    def max_count(self):
        return self._counter.max()

    def current_count(self):
        return self._counter.value

    def display_index(self, selected_index):
        self._printer(self._counter.parent.name(), ['', self._counter.name(), f'>     {selected_index}'])

    def select_index(self, selected_index):
        self._counter.value = selected_index
        return self._counter.parent_controller(self._printer)
