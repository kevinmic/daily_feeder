from pigpio_encoder import pigpio_encoder


ROTARY = pigpio_encoder.Rotary(clk=17, dt=18, sw=27)


class PiRotery:
    def __init__(self, select_callback=None, rotate_callback=None):
        self._rotate_callback = rotate_callback
        ROTARY.setup_switch(debounce=200, long_press=False, sw_short_callback=select_callback)

    def reset(self, min, max, counter):
        ROTARY.setup_rotary(min=min, max=max, scale=1, debounce=200,
                            rotary_callback=self._rotate_callback)

        ROTARY.counter = counter

    def watch(self):
        self.reset(self._base_controller)
        ROTARY.watch()
