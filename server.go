package main

import (
	"fmt"
	"io/fs"
	"log/slog"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
)

func setupRouter() *gin.Engine { //Erstellt und konfiguriert eine gin-Webengine
	slog.Info("Erstelle API-Endpoints und HTML-Server")

	router := gin.Default()
	router.SetTrustedProxies(nil) //Proxies? Brauchen wir nicht
	router.GET("/api/poweroff", poweroff)
	router.GET("/api/reboot", reboot)
	router.POST("/api/motors/1", postMotors) //Motorsteuerung, funktion ist weiter unten
	router.POST("/api/motors/2", postMotors)
	router.POST("/api/motors/3", postMotors)
	router.POST("/api/motors/4", postMotors)

	if fs.ValidPath("./www/api") {
		slog.Error("Fehler: Datei/Ordner www/api existiert!")
		os.Exit(1)
	}

	if !fs.ValidPath("./www/index.html") { //Wenn ./www/index.html nicht existiert wird keine WebUI konfiguriert um Fehler zu vermeiden
		router.GET("/", func(c *gin.Context) {
			c.Data(http.StatusNotFound, gin.MIMEPlain, []byte("Bruder lies mal logs ja?\n================================\nTipp: Hast du index.html in den Ordner www getan und die richtige working-directory (mit cd) gesetzt?"))
		})
		slog.Warn("www/index.html nicht gefunden!")

	} else {
		router.Static("/assets", "./www/assets") //Dateien in ./www sind auf dem server verfügbar, index.html als /
		router.LoadHTMLGlob("./www/*")
		router.GET("/", func(c *gin.Context) {
			c.HTML(http.StatusOK, "index.html", gin.H{
				"content": "Index-Seite",
			})
		})
	}
	return router
}

func poweroff(c *gin.Context) {
	c.Data(http.StatusOK, gin.MIMEPlain, []byte("Der Pi sollte jetzt herunterfahren...")) //Antworte mit code 200, content type "text/plain" und einer Nachricht
	exec.Command("poweroff").Start()
}

func reboot(c *gin.Context) {
	c.Data(http.StatusOK, gin.MIMEPlain, []byte("Der Pi sollte jetzt neu starten...")) //copy+paste lol
	exec.Command("reboot").Start()
}

func postMotors(c *gin.Context) { //Verarbeiten von Motor-Befehlen
	motorid := string(c.Request.URL.Path)
	motorid, _ = strings.CutPrefix(motorid, "/api/motors/") //Herausfinden der Motor-ID
	var data motorcontrol
	err := c.BindJSON(&data)
	if err != nil {
		c.Data(http.StatusBadRequest, gin.MIMEPlain, []byte("Fehler: "+err.Error()))
		fmt.Println(err)
		return
	}
	//Code zum Bewegen hier
	slog.Info("Bewege " + motorid + " | Steps: " + strconv.Itoa(data.Steps) + " | RPM: " + strconv.Itoa(data.Rpm) + " | Uhrzeigersinn: " + strconv.FormatBool(data.Clockwise))
	c.Data(http.StatusOK, gin.MIMEPlain, []byte("Bewege "+motorid+" | Steps: "+strconv.Itoa(data.Steps)+" | RPM: "+strconv.Itoa(data.Rpm)+" | Uhrzeigersinn: "+strconv.FormatBool(data.Clockwise)))
	//Antwort mit ALLEN Daten und Log schreiben

}