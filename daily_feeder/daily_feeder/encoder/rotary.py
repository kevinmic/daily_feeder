from pigpio_encoder import pigpio_encoder

my_rotary = pigpio_encoder.Rotary(clk=17, dt=18, sw=27)

curr_controller = None

def rotary_callback(counter):
    print("Callback", curr_controller)
    curr_controller.display_index(my_rotary.counter)


def select_short():
    print("Select Short", curr_controller)
    reset(curr_controller.select_index(my_rotary.counter))


def select_long(*args, **kwargs):
    print("Select Long", curr_controller)


def reset(menu):
    global curr_controller
    curr_controller = menu

    my_rotary.setup_rotary(min=0, max=curr_controller.max_count()-1, scale=1, debounce=200,
                           rotary_callback=rotary_callback)
    my_rotary.counter = curr_controller.current_count()
    rotary_callback(my_rotary.counter)


my_rotary.setup_switch(debounce=200, long_press=True, sw_short_callback=select_short, sw_long_callback=select_long)


def watch(controller):
    print("Watch 1")
    reset(controller)
    print("Watch 2")
    my_rotary.watch()
    print("Watch 3")
