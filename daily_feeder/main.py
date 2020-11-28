from pigpio_encoder import pigpio_encoder
from daily_feeder.menu import MENU
from daily_feeder.lcd import print_menu

my_rotary = pigpio_encoder.Rotary(clk=17, dt=18, sw=27)

curr_menu = None

def rotary_callback(counter):
    print('Rotary Callback - ', counter)
    global curr_counter
    curr_counter = counter
    print_menu(curr_menu.name(), curr_menu.value_names(), counter)


def sw_short():
    print('Switch short press', my_rotary.counter)
    reset_rotary(curr_menu.values()[my_rotary.counter])


def sw_long(*args, **kwargs):
    print('Switch long press', my_rotary.counter)

def reset_rotary(menu):
    print('New Menu: ', menu.name(), len(menu.values()))
    print(dir(my_rotary))
    global curr_menu
    curr_menu = menu

    my_rotary.setup_rotary(min=0, max=len(menu.values())-1, scale=1, debounce=200,
                           rotary_callback=rotary_callback)
    rotary_callback(my_rotary.counter)

my_rotary.setup_switch(debounce=200, long_press=True, sw_short_callback=sw_short, sw_long_callback=sw_long)

reset_rotary(MENU)

my_rotary.watch()
