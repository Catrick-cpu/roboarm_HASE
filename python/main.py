from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import re
import os
import random



# DISCLAIMER
# IF YOU HAVE NONE OF THE REQUIREMENTS INSTALLED 
#YOU HAVE TO COPY THEM OUT OF FOLDER "NOPIP" TO "python"

#Requirements installieren:

#sudo apt update
#sudo apt install -y python3-pip python3-smbus git i2c-tools
#pip3 install adafruit-circuitpython-motorkit
#pip install curses

#I2C Adresses: 60, 61
#As Integer: 96, 97

#sudo apt install -y i2c-tools





#Funktion	Raspberry Pi Pin	Bezeichnung	Richtung	Erklärung
#SDA (Data)	Pin 3	GPIO 2		Datenleitung (seriell bidirektional)
#SCL (Clock)	Pin 5	GPIO 3		Taktleitung (gibt Datenrhythmus vor)
#GND	Pin 6 (oder 9, 14, 20, 25, 30, 34, 39)	Ground		Gemeinsame Masse, sehr wichtig!
#3.3 V / 5 V	Pin 1 oder 2	Versorgung (optional)		Nur falls dein Sensor/Board das braucht — der Motor-HAT bekommt aber seine eigene Stromquelle!

#Raspberry Pi Zero
# ├── Pin 3 (SDA) ───────────── SDA (auf HAT)
# ├── Pin 5 (SCL) ───────────── SCL (auf HAT)
# ├── Pin 6 (GND) ───────────── GND (auf HAT + Motor-Netzteil)
# └── Pin 2 (5V)   ──────────── nur Logikstrom (wenn HAT direkt aufgesteckt)

#Motor-HAT
# ├── VIN  → 5–12 V Netzteil (+)
# ├── GND  → Netzteil (–) UND Pi-GND
# ├── M1A/M1B → Stepper 1 Spule A
# ├── M2A/M2B → Stepper 1 Spule B
# ├── (M3A–M4B für Stepper 2)



#Jeder HAT braucht eigene Motor-Stromversorgung (oder eine gemeinsame mit genügend Ampere).

#Auf dem zweiten HAT den A0-Jumper schließen/löten, damit er die Adresse 0x61 bekommt.


##SDA (Pin 3) und SCL (Pin 5) verbunden	
#GND vom Netzteil und Pi gemeinsam	
#A0-Jumper auf zweitem HAT gesetzt	
#sudo raspi-config → I2C enabled	
#sudo i2cdetect -y 1 zeigt 0x60/0x61	

#Willst du, dass ich dir eine kleine Grafik (Verdrahtungsdiagramm) dazu mache, wie alles zusammengehört (Pi Zero → zwei HATs → Stepper)?
#Dann kann ich sie dir sofort erzeugen.


input('Do you want to play a game? (y/n)')
if input == 'y':
    input('Guess a random number between 1 and 10: ')
    n = random.randint(1,10)
    if input == n:
        print('You won!!!!')

    else:
        print('You entered the wrong number')






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
print("Je größer der wert delay, desto langsamer drehen sich die motoren da der abstand zwischen den, größer ist ")
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