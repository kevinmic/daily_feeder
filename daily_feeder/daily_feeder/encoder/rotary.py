import logging

try:
    from daily_feeder.encoder.pi import PiRotery as Rotary
except ImportError:
    from daily_feeder.encoder.fake import FakeRotery as Rotary


rotary = None
base_display = None
curr_display = None
max_timeout = 20
timeout_counter = 0


def _rotary_callback():
    logging.debug("Rotate Callback")
    _change_timeout(0)
    curr_display.display_index(rotary.counter)


def refresh_callback():
    global curr_display
    if timeout_counter >= max_timeout:
        logging.debug(f"Refresh Timeout Exceeded: {timeout_counter}")
        _set_menu(base_display)
    elif curr_display is base_display:
        curr_display.display_index(rotary.counter)
    else:
        logging.debug(f"Inc Refresh Timeout: {timeout_counter}")
        _change_timeout(timeout_counter + 1)


def _select_short():
    global curr_display
    logging.debug("Select Callback")
    _set_menu(curr_display.select_index(rotary.counter))


def _set_menu(controller):
    global curr_display
    _change_timeout(0)
    curr_display = controller
    logging.debug(f"set menu: {controller} max:{curr_display.max_count()}, curr:{curr_display.current_count()}")
    rotary.reset(0, curr_display.max_count() - 1, curr_display.current_count())
    _rotary_callback()


def _change_timeout(timeout):
    global timeout_counter
    timeout_counter = timeout


def watch(displayer):
    logging.info("Start Watch")
    global rotary, base_display
    base_display = displayer
    rotary = Rotary(displayer, select_callback=_select_short, rotate_callback=_rotary_callback)
    _set_menu(displayer)

    rotary.watch()
