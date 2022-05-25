import os
import math
import random
import time
from typing import List

from pynput import keyboard
from pynput.keyboard import Key, Listener
import numpy as np


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys
        import termios  # for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def get_random_prime_integer(bounds):
    for i in range(bounds.__len__() - 1):
        if bounds[i + 1] > bounds[i]:
            x = bounds[i] + np.random.randint(bounds[i + 1] - bounds[i])
            if is_prime(x):
                return x

        else:
            if is_prime(bounds[i]):
                return bounds[i]

        if is_prime(bounds[i + 1]):
            return bounds[i + 1]

    newBounds = [0 for i in range(2 * bounds.__len__() - 1)]
    newBounds[0] = bounds[0]
    for i in range(1, bounds.__len__()):
        newBounds[2 * i - 1] = int((bounds[i - 1] + bounds[i]) / 2)
        newBounds[2 * i] = bounds[i]

    return get_random_prime_integer(newBounds)


def is_prime(x):
    count = 0
    for i in range(int(x / 2)):
        if x % (i + 1) == 0:
            count = count + 1
    return count == 1


def pow_desc(exp: int, mod: int, message, debug=False):
    print(f'Titkosítjuk: a(z) {message} üzenetet {exp} kulccsal és {mod} modulóval')
    res = 1
    coefficient = 1
    base = message
    while exp > 1:
        if coefficient != 1:
            if debug: print(f'{message}^{exp} * {coefficient} ({mod}) = ')
        else:
            if debug: print(f'{message}^{exp} ({mod}) = ')

        if exp % 2 != 0:
            exp -= 1
            coefficient *= base
            if coefficient > mod:
                coefficient %= mod
            if debug: print(f'{message}^{exp} * {coefficient} ({mod}) = ')
            res = (res * message) % mod
        message = message ** 2
        if debug: print(f'{message}^{exp} * {coefficient} ({mod}) = ')
        message %= mod
        exp //= 2

    if coefficient != 1:
        if debug: print(f'{message}^{exp} * {coefficient} ({mod}) = ')
    else:
        if debug: print(f'{message}^{exp} ({mod}) = \n{exp & 1}')
    return (message * res) % mod


def gcd_extended(a, b, debug=False):
    if debug: print(f'Euklidészi algoritmus -> a: {a}, b: {b}')
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a, debug)
    x = y1 - (b // a) * x1
    y = x1
    if debug: print(f'gcd: {gcd}, x: {x}, y: {y}')
    return gcd, x, y


class RsaKey:
    def __init__(self, p: int = 0, q: int = 0, e: int = 0):
        if p != 0 or q != 0 or e != 0:
            self.p, self.q = p, q
            self.n = self.p * self.q
            self.fi = (self.p - 1) * (self.q - 1)
            self.e = e
            if math.gcd(self.e, self.fi) != 1:
                print("Nem jó nyílt kulcs.. Keresek én!")
                self._get_public_key()
            self._get_private_key()
        else:
            limits = [800, 1000]
            self.p, self.q = get_random_prime_integer(limits), get_random_prime_integer(limits)
            while self.p == self.q:
                self.p, self.q = get_random_prime_integer(limits), get_random_prime_integer(limits)
            self.n = self.p * self.q
            self.fi = (self.p - 1) * (self.q - 1)
            self._get_public_key()
            self._get_private_key()

    def _get_public_key(self):
        self.e = random.randint(2, self.fi)
        # print(f'e: {self.e}, fi: {self.fi}')
        gcd = math.gcd(self.e, self.fi)
        # print(f'GCD: {gcd}, e: {self.e}, fi: {self.fi}')
        if gcd != 1:
            while gcd != 1:
                self.e = random.randint(2, self.fi)
                gcd = math.gcd(self.e, self.fi)
                # print(f'GCD: {gcd}, e: {self.e}, fi: {self.fi}')

    def _get_private_key(self):
        gcd, a, b = gcd_extended(self.e, self.fi)
        if a > 0:
            self.t = a
            print(f'Titkos kulcs: {self.t}')
        else:
            self.t = self.fi + a
            print(f'Titkos kulcs: {self.fi} - {abs(a)} = {self.t}')


class Person:
    name = ""

    def __init__(self, key: RsaKey = None, name: str = None, debug=False):
        if name is None:
            self.name = input("A szemely neve: ")
        else:
            self.name = name
            print(f'Üdvözlöm {self.name}')
        self.proba = debug
        if key is None:
            if self.proba:
                p = int(input("1. Prim szam: "))
                q = int(input("2. Prim szam: "))
                e = int(input("Nyilt kulcs: "))
                self._key = RsaKey(p, q, e)
            else:
                self._key = RsaKey()
        else:
            self._key = key

    def share_pub_key(self) -> tuple[int, int]:
        return self._key.e, self._key.n

    def print_all_data(self):
        t_key = self._key
        print(f'{self.name} primjei: {t_key.p} es {t_key.q}')
        print(f'{self.name} modulusa: {t_key.n} es fi-je: {t_key.fi}')
        print(f'{self.name} nyilt kulcsa: {t_key.e} es titkos kulcsa: {t_key.t}')

    def send_message_to(self, foreign_key: tuple[int, int], text: int, self_coded=False) -> int:
        f_e, f_n = foreign_key
        if not self_coded:
            return pow_desc(f_e, f_n, text)
        else:
            print(f"Az en ({self.name.lower()}) titkoskulcsom rarakasa")
            init_layer = pow_desc(self._key.t, self._key.n, text)
            print("Az idegen nyiltkulcs rarakasa")
            final_layer = pow_desc(f_e, f_n, init_layer)
            return final_layer

    def receive_message(self, foreign_key: tuple[int, int], text: int, self_coded=False) -> int:
        f_e, f_n = foreign_key
        if not self_coded:
            return pow_desc(self._key.t, self._key.n, text)
        else:
            print(f"Az en ({self.name.upper()}) nyiltkulcsom lebontasa")
            init_layer = pow_desc(self._key.t, self._key.n, text)
            print("Az idegen titkoskulcs lebontasa")
            final_layer = pow_desc(f_e, f_n, init_layer)
            return final_layer


# GLOBALS
highlight = "\x1b[6;30;42m"
info_text = "\033[38;5;208m"
normal_text = "\033[0;0m"


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


persons: List[Person] = []


def get_person_by_name(name: str) -> Person:
    searched = None
    while searched is None:
        for p in persons:
            if p.name == name:
                searched = p
        if searched is None:
            print("Ez a személy nem létezik")
            input("Kérem egy másik személy nevét: ")
    return searched



def main():
    choice = None
    choice = Menu(
        {
            0: "Személy hozzáadás",
            1: "Személy adatainak kiírása",
            2: "Üzenet küldés",
            3: "Üzenet fogadás",
            4: "Alap műveletek",
            "static": "Szóközzel válasszon opciót!"
        })
    with keyboard.Listener(on_release=choice.on_release) as listener:
        listener.join()

    if choice.selected_key == 0:
        name = input("Kérem az új személy nevét: ")
        persons.append(Person(name=name, debug=True))

    if choice.selected_key == 1:
        name = input("Kérem a személy nevét: ")
        person = get_person_by_name(name)
        person.print_all_data()

    if choice.selected_key == 2:
        digital = Menu(
            {
                0: "Digitálisan aláírva",
                1: "Sima kódolás",
                "static": "Szóközzel válasszon opciót!"
            })
        with keyboard.Listener(on_release=digital.on_release) as listener:
            listener.join()
        if digital.selected_key == 0:
            whom = input("Ki küldi: ")
            target = input("Kinek szeretné küldeni: ")
            sender_person = get_person_by_name(whom)
            receiver_person = get_person_by_name(target)
            message = int(input("Üzenet: "))
            digitally_signed_message = sender_person.send_message_to(receiver_person.share_pub_key(), message, True)
            print(f'Üzenet: {message}, titkosított üzenet: {digitally_signed_message}')
        else:
            target = input("Kinek szeretné küldeni: ")
            receiver_person = get_person_by_name(target)
            message = int(input("Üzenet: "))
            en_message = receiver_person.send_message_to(receiver_person.share_pub_key(), message)
            print(f'Üzenet: {message}, titkosított üzenet: {en_message}')

    if choice.selected_key == 3:
        digital = Menu(
            {
                0: "Digitálisan aláírva",
                1: "Sima dekódolás",
                "static": "Szóközzel válasszon opciót!"
            })
        with keyboard.Listener(on_release=digital.on_release) as listener:
            listener.join()

        if digital.selected_key == 0:
            whom = input("Ki küldi: ")
            target = input("Ki a címzett: ")
            sender_person = get_person_by_name(whom)
            receiver_person = get_person_by_name(target)
            digitally_signed_message = int(input("Titkosított üzenet: "))
            message = receiver_person.receive_message(sender_person.share_pub_key(), digitally_signed_message, True)
            print(f'Titkosított üzenet: {digitally_signed_message},  üzenet: {message}')
        else:
            target = input("Kitől fogad üzenetet: ")
            receiver_person = get_person_by_name(target)
            en_message = int(input("Titkosított üzenet: "))
            message = receiver_person.receive_message((0, 0), en_message)
            print(f'Titkosított üzenet: {en_message},  üzenet: {message}')

    if choice.selected_key == 4:
        operation = Menu(
            {
                0: "Euklidészi Algoritmus és Diofantoszi egyenlet (rekurzív)",
                1: "Moduló számítás",
                2: "Vissza",
                "static": "Szóközzel válasszon opciót!"
            })
        with keyboard.Listener(on_release=operation.on_release) as listener:
            listener.join()
        if operation.selected_key == 0:
            mod_fi = int(input("Adja meg a fi függvény által kapott számot: "))
            e_test = int(input("Adja meg nyilt kulcsnak szánt számot: "))
            gcd_extended(e_test, mod_fi, True)
        if operation.selected_key == 1:
            mod = int(input("Adja meg a modulót: "))
            key = int(input("Adja meg a kulcsot: "))
            message = int(input("Adja meg az üzenetet: "))
            coded_message = pow_desc(37, 77, 8, True)
            print(f'Titkosított üzenet: {message} -> {coded_message}')


    print()
    print("Nyomja meg a szóköz gombot a folytatáshoz!")
    with Listener(on_release=on_release) as main_listener:
        main_listener.join()


while True:
    main()
