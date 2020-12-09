import logging
try:
    from daily_feeder.encoder.pi import PiRotery as Rotary
except ImportError:
    from daily_feeder.encoder.fake import FakeRotery as Rotary


rotary = None
curr_controller = None

def rotary_callback():
    logging.debug("Rotate Callback")
    curr_controller.display_index(rotary.counter)


def select_short():
    global curr_controller
    logging.debug("Select Callback")
    set_menu(curr_controller.select_index(rotary.counter))


def set_menu(controller):
    global curr_controller
    curr_controller = controller
    logging.debug(f"set menu: {controller}")
    rotary.reset(0, curr_controller.max_count()-1, curr_controller.current_count())
    rotary_callback()


def select_long(*args, **kwargs):
    logging.info("Select Long Callback")


def watch(controller):
    logging.info("Start Watch")
    global rotary
    rotary = Rotary(controller, select_callback=select_short, rotate_callback=rotary_callback)
    set_menu(controller)
    rotary.watch()
