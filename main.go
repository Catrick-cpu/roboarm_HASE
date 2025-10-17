package main

import (
	"fmt"
	"runtime"
	"time"

	"github.com/gin-gonic/gin"
	"gobot.io/x/gobot"
)

//data.go: enthält structs, variablen und ähnliches

var router *gin.Engine

func main() {
	driver1.address = 96 //I2C-ADRESSEN HIER EINGEBEN (als int, rechnet am besten mit website um)
	driver2.address = 97
	fmt.Println("RoboArm server v0.2")
	if runtime.GOOS == "windows" { //Anti-Windows-check
		fmt.Println("Du versuchst gerade ein Programm für einen Raspberry Pi auf Windows auszuführen. Das wird vermutlich nicht funktionieren!")
		time.Sleep(time.Second * 3)
	}
	fmt.Println("Starte...")
	setupOperatingArray()  //Array das den Status der Motoren speichert (siehe data.go)
	allocateDrivers()      //Sucht die Motor-Driver (siehe control.go)
	router = setupRouter() //Erstellt *gin.Engine und konfiguriert die API (siehe server.go)

	robot = gobot.NewRobot("roboter", //Erstellt einen neuen gobot...
		i2c_bus, //...mit allen Geräten die hier angegeben sind...
		driver1.dev,
		driver2.dev,
		startRouter, //und wenn robot.Start() aufgerufen wird, startet auch die API
	)
	fmt.Println("Das Programm hat die folgenden Verbindungen gefunden: ", robot.Connections(), "(", robot.Connections().Len(), ")")
	fmt.Println("Geräte werden betriebsbereit gemacht...")
	err := robot.Start()
	if err != nil {
		fmt.Println("Beim Starten eines Geräts ist ein Fehler aufgetreten!")
		fmt.Println(err.Error())
	}
}

func startRouter() { //Startet den Server wenn der Roboter gestartet wird
	router.Run()
}
