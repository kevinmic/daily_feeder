import curses

screen = curses.initscr()

def printer(header, lines):
    screen.clear()
    screen.addstr(header + "\n")
    screen.addstr('-------\n')
    for line in lines:
        screen.addstr(line + "\n")
    screen.refresh()
