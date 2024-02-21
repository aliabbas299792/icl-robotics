"""
Various bits of helpful code, focusing on wrapping around curses,
  since curses is how we're getting user input from the terminal
  without sudo, and it appears to mess up display formatting if you
  also try to use print
"""

import curses
import time
import signal
from dataclasses import dataclass
from bot_control.Bot import Bot


def cleanup():
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    Bot._reset_bp()


@dataclass
class CursesState:
    stdscr: curses.window
    current_line: int = 0
    max_lines: int = 0


def main_wrapper(main):
    def signal_handler(_, __):
        cleanup()
        exit(0)

    def wrap(local_stdscr):
        CursesState.stdscr = local_stdscr
        CursesState.max_lines = local_stdscr.getmaxyx()[0]  # Set max_lines
        signal.signal(signal.SIGINT, signal_handler)
        main()

    curses.wrapper(wrap)


def curse_print(text):
    CursesState.stdscr.addstr(CursesState.current_line, 0, text)
    CursesState.current_line += 1
    CursesState.stdscr.refresh()

    # Screen clearing logic
    if CursesState.current_line >= CursesState.max_lines:
        CursesState.stdscr.clear()
        CursesState.current_line = 0


def curse_getkey():
    try:
        return CursesState.stdscr.getkey()
    except:
        cleanup()
        exit(0)


def curse_noecho():
    curses.noecho()


class ControlProcedure:
    def __init__(self, control_loop_fn):
        self.control_loop_fn = control_loop_fn
        curse_noecho()

    def start_procedure(self):
        while True:
            inp = curse_getkey()
            self.control_loop_fn(inp)
            time.sleep(0.1)
