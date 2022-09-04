import os
from pynput import keyboard
from pynput.keyboard import Key, Listener

# GLOBALS
highlight = "\x1b[6;30;42m"
info_text = "\033[38;5;208m"
normal_text = "\033[0;0m"
gray = "\033[XXXm"

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys
        import termios  # for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


class Menu:
    def print_menu(self):
        os.system("cls")
        # os.system("clear")
        options_keys = self.options.keys()
        for key in options_keys:
            if key == "static":
                print(info_text, str(self.options[key]), normal_text)
            elif key == self.selected_key:
                print(highlight, str(self.options[key]), normal_text)
            else:
                print(self.options[key])

    def select_option(self, direction: int):
        temp = list(self.options)
        if direction > 0:
            if len(temp) >= temp.index(self.selected_key) + 1 and temp[temp.index(self.selected_key) + 1] != "static":
                self.selected_key = temp[temp.index(self.selected_key) + 1]
                self.print_menu()
        elif direction < 0:
            if temp.index(self.selected_key) - 1 >= 0 and temp[temp.index(self.selected_key) - 1] != "static":
                self.selected_key = temp[temp.index(self.selected_key) - 1]
                self.print_menu()

    def __init__(self, options: dict):
        self.options = options
        self.selected_key = list(self.options)[0]
        self.print_menu()

    def on_release(self, key):
        if key == Key.up:
            self.select_option(-1)
            flush_input()
        elif key == Key.down:
            self.select_option(1)
            flush_input()
        elif key == Key.space:
            flush_input()
            return False


def on_release(key):
    if key == Key.space:
        return False
