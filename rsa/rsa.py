import math
import sys
import os
from pynput import keyboard
from pynput.keyboard import Key, Listener
import random
from functions import *
from typing import List
# import pywintypes
# import win32api


# GLOBALS
highlight = "\x1b[6;30;42m"
info_text = "\033[38;5;208m"
normal_text = "\033[0;0m"


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
                print(f'Az általam vett nyílt kulcs: {self.e}')
            self._get_private_key()
        else:
            limits = [1500, 2000]
            self.p, self.q = get_random_prime_integer(limits), get_random_prime_integer(limits)
            while self.p == self.q:
                self.p, self.q = get_random_prime_integer(limits), get_random_prime_integer(limits)
            self.n = self.p * self.q
            self.fi = (self.p - 1) * (self.q - 1)
            self._get_public_key()
            self._get_private_key()

    def _get_public_key(self):
        self.e = random.randint(2, self.fi)
        gcd = math.gcd(self.e, self.fi)
        if gcd != 1:
            while gcd != 1:
                self.e = random.randint(2, self.fi)
                gcd = math.gcd(self.e, self.fi)

    def _get_private_key(self):
        gcd, a, b = diophantine_equation(self.e, self.fi)
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
            0: "Személy generálás",
            1: "Személy hozzáadás",
            2: "Személy adatainak kiírása",
            3: "Üzenet küldés",
            4: "Üzenet fogadás",
            5: "Alap műveletek",
            "static": "Szóközzel válasszon opciót!"
        })
    with keyboard.Listener(on_release=choice.on_release) as listener:
        listener.join()

    if choice.selected_key == 0:
        name = input("Kérem az új személy nevét: ")
        gen_person = Person(name=name)
        persons.append(gen_person)

    if choice.selected_key == 1:
        name = input("Kérem az új személy nevét: ")
        persons.append(Person(name=name, debug=True))

    if choice.selected_key == 2:
        name = input("Kérem a személy nevét: ")
        person = get_person_by_name(name)
        person.print_all_data()

    if choice.selected_key == 3:
        digital = Menu(
            {
                0: "Digitálisan aláírva",
                1: "Sima kódolás",
                "static": "Szóközzel válasszon opciót!"
            })
        with keyboard.Listener(on_release=digital.on_release) as listener:
            listener.join()
        if digital.selected_key == 0:
            whom = input("Az ön neve: ")
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

    if choice.selected_key == 4:
        digital = Menu(
            {
                0: "Digitálisan aláírva",
                1: "Sima dekódolás",
                "static": "Szóközzel válasszon opciót!"
            })
        with keyboard.Listener(on_release=digital.on_release) as listener:
            listener.join()

        if digital.selected_key == 0:
            whom = input("Kitől érkezik: ")
            target = input("Az ön neve: ")
            sender_person = get_person_by_name(whom)
            receiver_person = get_person_by_name(target)
            digitally_signed_message = int(input("Titkosított üzenet: "))
            message = receiver_person.receive_message(sender_person.share_pub_key(), digitally_signed_message, True)
            print(f'Titkosított üzenet: {digitally_signed_message},  üzenet: {message}')
        else:
            target = input("Az ön neve: ")
            receiver_person = get_person_by_name(target)
            en_message = int(input("Titkosított üzenet: "))
            message = receiver_person.receive_message((0, 0), en_message)
            print(f'Titkosított üzenet: {en_message},  üzenet: {message}')

    if choice.selected_key == 5:
        operation = Menu(
            {
                0: "euclidean_algorithm(a, b)",
                1: "diophantine_equation(a, b)",
                2: "pow_desc(exp, mod, message)",
                3: "Vissza",
                "static": "Szóközzel válasszon opciót!"
            })
        with keyboard.Listener(on_release=operation.on_release) as listener:
            listener.join()
        os.system("cls")
        if operation.selected_key == 0:
            mod_fi = int(input("Adja meg az \'a\' számot (fi(n)): "))
            e_test = int(input("Adja meg a \'b\' számot (e): "))
            print(f'Meghívott függvény:', info_text, f'euclidean_algorithm({mod_fi}, {e_test})', normal_text)
            gcd = euclidean_algorithm(mod_fi, e_test)
            print(f'Legnagyobb közös osztó: ', info_text, gcd, normal_text)
        if operation.selected_key == 1:
            mod_fi = int(input("Adja meg az \'a\' számot (fi(n)): "))
            e_test = int(input("Adja meg a \'b\' számot (e): "))
            print(f'Meghívott függvény:', info_text, f'diophantine_equation({mod_fi}, {e_test})', normal_text)
            diophantine_equation(mod_fi, e_test, True)
        if operation.selected_key == 2:
            key = int(input("Adja meg a kulcsot (e/t): "))
            mod = int(input("Adja meg a modulót (n): "))
            message = int(input("Adja meg az üzenetet (m): "))
            print(f'Meghívott függvény:', info_text, f'pow_desc({key}, {mod}, {message})', normal_text)
            coded_message = pow_desc(key, mod, message, True)
            print(f'Titkosított üzenet: {message} -> {coded_message}')

    print()
    print("Nyomja meg a szóköz gombot a folytatáshoz!")
    with Listener(on_release=on_release) as main_listener:
        main_listener.join()


while True:
    main()
