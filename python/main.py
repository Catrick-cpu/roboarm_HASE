from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import time
import board
import busio
import os 
import curses

#Requirements installieren:

#sudo apt update
#sudo apt install -y python3-pip python3-smbus git i2c-tools
#pip3 install adafruit-circuitpython-motorkit
#pip install curses


#I2C Adresses: 60, 61
#As Integer: 96, 97

os.system("sudo i2cdetect -y 1") #Prüfen ob Motor HATS gefunden werden
#   ⬆ sollte etwas anzeigen wie 60, 61 ⬆


# I2C initialisieren
i2c = busio.I2C(board.SCL, board.SDA)

# Zwei HATs
kit1 = MotorKit(i2c=i2c, address=0x60)
kit2 = MotorKit(i2c=i2c, address=0x61)

# Motoren
motors = [
    kit1.stepper1,
    kit1.stepper2,
    kit2.stepper1,
    kit2.stepper2
]

# Namen der Motoren
motor_names = ["Motor 1", "Motor 2", "Motor 3", "Motor 4"]

# Initial ausgewählter Motor
current = 0#

# Funktion für das UI
def main(stdscr):
    global current
    curses.curs_set(0)  # Cursor ausblenden
    stdscr.nodelay(1)   # Keine Blockierung bei getch()
    stdscr.timeout(100)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Stepper Motor Konsole (ESC zum Beenden)")
        stdscr.addstr(1, 0, "Benutze Pfeiltasten: ↑↓ →← für Vorwärts/Rückwärts")
        stdscr.addstr(2, 0, "Wechseln mit: w (hoch) / s (runter)")
        stdscr.addstr(4, 0, "Ausgewählter Motor:")

        for idx, name in enumerate(motor_names):
            marker = "->" if idx == current else "  "
            stdscr.addstr(5 + idx, 0, f"{marker} {name}")

        key = stdscr.getch()

        if key == 27:  # ESC
            break
        elif key == ord('w'):  # Motor hoch
            current = (current - 1) % len(motors)
        elif key == ord('s'):  # Motor runter
            current = (current + 1) % len(motors)
        elif key == curses.KEY_UP:  # Vorwärts
            motors[current].onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        elif key == curses.KEY_DOWN:  # Rückwärts
            motors[current].onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)

        stdscr.refresh()

    # Alle Motoren ausschalten
    for m in motors:
        m.release()

# curses starten
curses.wrapper(main)

#Funktionsweise:

#w / s → ausgewählten Motor wechseln

#↑ → Motor vorwärts

#↓ → Motor rückwärts

#ESC → Programm beenden

#Alle Motoren werden am Ende ausgeschaltet (release())

