from pigpio_encoder import pigpio_encoder
from daily_feeder.displayer.menu_display import display

my_rotary = pigpio_encoder.Rotary(clk=17, dt=18, sw=27)

curr_menu = None

def rotary_callback(counter):
    global curr_counter
    curr_counter = counter
    display(curr_menu.name(), curr_menu.value_names(), counter)


def sw_short():
    reset_rotary(curr_menu.values()[my_rotary.counter])


def sw_long(*args, **kwargs):
    pass


def reset_rotary(menu):
    print(dir(my_rotary))
    global curr_menu
    curr_menu = menu

    my_rotary.setup_rotary(min=0, max=len(menu.values())-1, scale=1, debounce=200,
                           rotary_callback=rotary_callback)
    rotary_callback(my_rotary.counter)


my_rotary.setup_switch(debounce=200, long_press=True, sw_short_callback=sw_short, sw_long_callback=sw_long)


def watch(menu):
    reset_rotary(menu)
    my_rotary.watch()
