package main

import (
	"errors"
	"log/slog"
	"os"
	"strconv"

	"gobot.io/x/gobot"
	"gobot.io/x/gobot/drivers/i2c"
	"gobot.io/x/gobot/platforms/raspi"
)

var robot *gobot.Robot
var i2c_bus *raspi.Adaptor

var operating [4]bool
var driver1 motor_driver
var driver2 motor_driver

func allocateDrivers() { //Findet die stepper motor driver mithilfe ihrer i2c-Adressen
	i2c_bus = raspi.NewAdaptor() //Raspberry pi hat nur ein i2c-Interface also muss ich nix festlegen
	if i2c_bus == nil {
		slog.Error("Konnte keinen i2c-Bus finden, du führst das auf dem Pi aus, oder?")
		slog.Error("Tipp: probiers mal mit sudo")
		os.Exit(2)
	}

	slog.Info("Suche nach stepper motor driver mit I2C-Addresse " + strconv.Itoa(driver1.address))
	driver1.dev = i2c.NewAdafruitMotorHatDriver(i2c_bus, i2c.WithAddress(driver1.address))

	if driver1.dev == nil { //Verbindungsfehler erkennen, loggen und Programm beenden
		slog.Error("Fehler beim Verbinden mit driver1! (I2C-Addresse ist " + strconv.Itoa(driver1.address) + ")")
		os.Exit(2)
	}

	slog.Info("Suche nach stepper motor driver mit I2C-Addresse " + strconv.Itoa(driver2.address))
	driver2.dev = i2c.NewAdafruitMotorHatDriver(i2c_bus, i2c.WithAddress(driver2.address))

	if driver2.dev == nil { //Verbindungsfehler erkennen, loggen und Programm beenden
		slog.Error("Fehler beim Verbinden mit driver2! (I2C-Addresse ist " + strconv.Itoa(driver2.address) + ")")
		os.Exit(2)
	}

}

func MotorControl(motorId int, steps int, rpm int, direction i2c.AdafruitDirection) error { //IF-Kette die den richtigen Motor findet, das speed setzt und ihn startet
	if motorId == 1 {
		err := driver2.dev.SetStepperMotorSpeed(0, rpm)
		if err == nil {
			err = driver1.dev.Step(0, steps, direction, i2c.AdafruitSingle)
		}
		return err
	} else if motorId == 2 {
		err := driver2.dev.SetStepperMotorSpeed(1, rpm)
		if err == nil {
			err = driver1.dev.Step(1, steps, direction, i2c.AdafruitSingle)
		}
		return err
	} else if motorId == 3 {
		err := driver2.dev.SetStepperMotorSpeed(0, rpm)
		if err == nil {
			err = driver2.dev.Step(0, steps, direction, i2c.AdafruitSingle)
		}
		return err
	} else if motorId == 4 {
		err := driver2.dev.SetStepperMotorSpeed(1, rpm)
		if err == nil {
			err = driver2.dev.Step(1, steps, direction, i2c.AdafruitSingle)
		}
		return err
	}
	return errors.New("invalid number")

}
