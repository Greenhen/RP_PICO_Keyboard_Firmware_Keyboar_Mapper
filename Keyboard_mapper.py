from machine import Pin
from time import sleep_us,sleep

def scan_matrix(sorok, oszlopok):
    koordinatak=[]
    for elem in oszlopok:
        elem.value(1)
    for oszlop_index, oszlop_ertek in enumerate(oszlopok):
        oszlop_ertek.value(0)
        sleep_us(10)
        for sor_index, sor_ertek in enumerate(sorok):
            if sor_ertek.value() == 0:
                koordinatak.append((sor_index,oszlop_index))
        oszlop_ertek.value(1)
    return koordinatak

def keymap_mentes(keymap, fajlnev):
    with open(fajlnev, "w") as fajl:
        for koordinata, billentyu in keymap.items():
            fajl.write(f"{koordinata[0]},{koordinata[1]},{billentyu}\n")


sorok=[Pin(14, Pin.IN, Pin.PULL_UP),Pin(12, Pin.IN, Pin.PULL_UP)]
oszlopok=[Pin(13, Pin.OUT), Pin(11, Pin.OUT)]



buttons =[
    # Funkcióbillentyűk
    "ESC", "F1", "F2", "F3", "F4", "F5", "F6",
    "F7", "F8", "F9", "F10", "F11", "F12",
    "PRTSC", "PAUSE", "INS", "DEL",

    # Felső számsor
    "0", "1", "2", "3", "4", "5", "6",
    "7", "8", "9", "Ö", "Ü", "Ó", "BACKSPACE",

    # QWERTZ sor
    "TAB", "Q", "W", "E", "R", "T", "Z",
    "U", "I", "O", "P", "Ő", "Ú", "ENTER",

    # ASDF sor
    "CAPSLOCK", "A", "S", "D", "F", "G",
    "H", "J", "K", "L", "É", "Á", "Ű",

    # Shift sor
    "LSHIFT", "Í", "Y", "X", "C", "V", "B",
    "N", "M", ",", ".", "-", "RSHIFT",

    # Alsó sor
    "LCTRL", "FN", "WIN", "LALT",
    "SPACE",
    "ALTGR", "MENU", "RCTRL",

    # Kurzor blokk
    "HOME", "PGUP",
    "END", "PGDN",
    "UP", "LEFT", "DOWN", "RIGHT",

    # Numerikus billentyűzet
    "NUMLOCK", "NUM/", "NUM*", "NUM-",
    "NUM7", "NUM8", "NUM9",
    "NUM4", "NUM5", "NUM6",
    "NUM1", "NUM2", "NUM3",
    "NUM0", "NUM.", "NUMENTER", "NUM+"
]


keymap = {}


for button in buttons:
    print(f"Press key {button}:")
    while True:
        koordinatak = scan_matrix(sorok, oszlopok)
        if len(koordinatak) == 1 and koordinatak[0] not in keymap:
            koordinata = koordinatak[0]
            sleep(0.01)
            masodik_meres=scan_matrix(sorok, oszlopok)
            if len(masodik_meres)==1 and masodik_meres[0]==koordinata:
                break
        elif len(koordinatak) == 1 and koordinatak[0] in keymap:
            koordinata=koordinatak[0]
            sleep(0.01)
            masodik_meres=scan_matrix(sorok, oszlopok)
            if len(masodik_meres)==1 and masodik_meres[0]==koordinata:
                print("Ez a koordináta már foglalt!")
                while True:
                    if not scan_matrix(sorok, oszlopok):
                        break
        elif len(koordinatak)>1:
            sleep(0.01)
            masodik_meres=scan_matrix(sorok, oszlopok)
            if len(masodik_meres)>1:
                print("Egyszerre csak egy billentyűt nyomj meg!")
                while True:
                    if not scan_matrix(sorok, oszlopok):
                        break
    keymap[koordinata] = button
    keymap_mentes(keymap, "keymap.txt")
    while True:
        if not scan_matrix(sorok, oszlopok):
            break

