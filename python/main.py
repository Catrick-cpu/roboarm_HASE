from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time as
import re
import os

#Requirements installieren:

#sudo apt update
#sudo apt install -y python3-pip python3-smbus git i2c-tools
#pip3 install adafruit-circuitpython-motorkit
#pip install curses

#I2C Adresses: 60, 61
#As Integer: 96, 97


print("Starting up...")

print("The following command should show something like 0x60 ----  0x61")
time.sleep(1)


os.system("sudo i2cdetect -y 1") #Prüfen ob Motor HATS gefunden werden


# initialise
i2c = busio.I2C(board.SCL, board.SDA)

#HAT Defenitions with adresses 0x60, 0x612
kit1 = MotorKit(i2c=i2c, address=0x60)
kit2 = MotorKit(i2c=i2c, address=0x61)

#Motor Defenitions
motors = [
    kit1.stepper1,
    kit1.stepper2,
    kit2.stepper1,
    kit2.stepper2
]

print("StepperMotor Konsole gestartet ")
print("Befehl: steppermotor(<1–4>, <forward/backward>, <steps>, [delay])")
print("Je größer der wert delay, desto langsamer drehen sich die motoren da der abstand zwischen den" /n "größer ist ")
time.sleep(2)
print("Beispiel: steppermotor(2, forward, 200, 0.005)")
print("Beenden mit: exit")
time.sleep(2)

def move_stepper(motor_id, direction, steps, delay):
    """Führt die Bewegung eines Steppers aus."""
    motor = motors[motor_id - 1]
    dir_map = {
        "forward": stepper.FORWARD,
        "backward": stepper.BACKWARD
    }

    dir_value = dir_map.get(direction.lower())
    if dir_value is None:
        print("Ungültige Richtung! Nutze 'forward' oder 'backward'.")
        return

    print(f"Motor {motor_id}: {direction} ({steps} Schritte, delay={delay})")

    for _ in range(steps):
        motor.onestep(direction=dir_value, style=stepper.SINGLE)
        time.sleep(delay)

    motor.release()
    print(f"Motor {motor_id} fertig\n")

#main loop
while True:
    try:
        command = input(">>> ").strip()

        if command.lower() in ("exit", "quit"):
            print("Beende Programm…")
            break

        # Beispiel: steppermotor(2, forward, 200, 0.005)
        match = re.match(
            r"steppermotor\(\s*(\d+)\s*,\s*([a-zA-Z]+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)",
            command
        )

        if match:
            motor_id = int(match.group(1))
            direction = match.group(2)
            steps = int(match.group(3))
            delay = float(match.group(4)) if match.group(4) else 0.01

            if 1 <= motor_id <= 4:
                move_stepper(motor_id, direction, steps, delay)
            else:
                print("Motornummer muss zwischen 1 und 4 liegen.")
        else:
            print("unknown command")
            print("usage:  steppermotor(1, forward, 200, 0.01)")


    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Fehler: {e}")

# Motoren ausschalten
for m in motors:
    m.release()

print("Programm beendet")