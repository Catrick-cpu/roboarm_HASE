package main

import "gobot.io/x/gobot/drivers/i2c"

type motorcontrol struct { //Daten für /api/motors/...
	Steps     int  `json:"steps"`
	Clockwise bool `json:"clockwise"`
	Rpm       int  `json:"rpm"`
}

type motor_driver struct {
	dev     *i2c.AdafruitMotorHatDriver
	address int
}

func setupOperatingArray() {
	operating[0] = false
	operating[1] = false
	operating[2] = false
	operating[3] = false
}
