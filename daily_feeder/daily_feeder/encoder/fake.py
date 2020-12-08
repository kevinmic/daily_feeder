import curses

screen = curses.initscr()

class FakeRotery:
    counter = 0
    _max = 0
    _min = 0

    def __init__(self, controller, select_callback=None, rotate_callback=None):
        self._rotate_callback = rotate_callback
        self._select_callback = select_callback

    def controller(self):
        return self._curr_controller

    def reset(self, min, max, counter):
        self._min = min
        self._max = max
        self.counter = counter

    def watch(self):
        while True:
            val = screen.getch()

            # up
            if val == 65:
                curr_count = self.counter - 1
                if curr_count >= self._min:
                    self.counter = curr_count
                self._rotate_callback()

            # down
            elif val == 66:
                curr_count = self.counter + 1
                if curr_count <= self._max:
                    self.counter = curr_count
                self._rotate_callback()

            elif val == 67 or val == 68:
                self._select_callback()

            else:
                self._rotate_callback()
