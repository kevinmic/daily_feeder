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
        previous = None
        val = None
        while True:
            print(f"PREVIOUS val:[{val}] option:[{previous}]")
            print(f"SELECT YOUR OPTION:")
            val = input()

            if val.startswith('h'):
                curr_count = self.counter - 1
                if curr_count >= self._min:
                    previous = 'prev'
                    self.counter = curr_count
                    self._rotate_callback()
            if val.startswith('l'):
                curr_count = self.counter + 1
                if curr_count <= self._max:
                    previous = 'next'
                    self.counter = curr_count
                    self._rotate_callback()
            if val.startswith(' '):
                previous = 'select'
                self._select_callback()
