try:
    from daily_feeder.printer.pi import printer
except ImportError:
    from daily_feeder.printer.fake import printer

def print_lcd(header, lines):
    printer(header, lines)
