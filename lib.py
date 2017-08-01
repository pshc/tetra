import os
import sys
import time
from select import select
from subprocess import Popen, PIPE

arrow_character_codes = dict(D="left", B="down", C="right", A="up")
escape_sequence = "\x1b"
ctrl_c = "\003"

def now():
    return time.monotonic()

def get_input(deadline):
    """
    Waits for a single character of input
    and returns the string "left", "down", "right", "up",
    or None if we hit the deadline before a button was pressed.
    """

    while True:
        remaining_time = deadline - now()
        if remaining_time <= 0:
            break
        # use unix select on stdin to allow our read to time out
        read_list, _, _ = select([sys.stdin], [], [], remaining_time)
        if not read_list:
            break # timed out

        input = sys.stdin.read(1)

        # The arrow keys are read from stdin as an escaped sequence of 3 bytes.
        if input == escape_sequence:
            # The next two bytes will indicate which arrow key was pressed.
            character = sys.stdin.read(2)
            arrow = arrow_character_codes.get(character[1], None)
            if arrow:
                return arrow
        elif input == ctrl_c:
            sys.exit()

    return None

def clear_screen():
    os.system('clear')

def set_terminal_mode():
    original_terminal_state = Popen("stty -g", stdout=PIPE, shell=True).communicate()[0]
    os.system("stty -icanon -echo -isig")
    return str(original_terminal_state, 'utf-8')

def restore_terminal(state):
    os.system(f"stty {state}")
