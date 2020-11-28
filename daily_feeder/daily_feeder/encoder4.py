from pigpio_encoder import pigpio_encoder

my_rotary = pigpio_encoder.Rotary(clk=17, dt=18, sw=27)

def rotary_callback(counter):
    if counter == 10:
        my_rotary.setup_rotary(min=0, max=60, scale=1, debounce=200, rotary_callback=rotary_callback)
    print("Counter value: ", counter)

def sw_short():
    print("Switch short press")

def sw_long():
    print("Switch long press")


my_rotary.setup_rotary(min=0, max=30, scale=1, debounce=200, rotary_callback=rotary_callback)
my_rotary.setup_switch(debounce=200, long_press=True, sw_short_callback=sw_short, sw_long_callback=sw_long)

my_rotary.watch()