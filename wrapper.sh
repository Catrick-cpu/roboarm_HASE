#! /bin/bash
# Dieses Skript wird ausgeführt wenn SystemD roboarm.service startet!
# Es soll prüfen ob ein Ordner namens roboarm_updates existiert und wenn ihn in /roboarm verschieben und die binary /roboarm/core ausführen
# Du kannst es auch verwenden um Befehle auf dem Pi auszuführen, pack sie weiter unten hin
echo Roboterarm controller wrapper script v0.1
cd /roboarm
echo "Suche lokal nach neuen Versionen in /boot/firmware/roboarm_updates (Ordner auf boot-partition)"
if [ -d "/boot/firmware/roboarm_updates" ]; then
    echo Neuer Ordner gefunden, kopiere...
    rm -rf /roboarm.old
    mkdir -p /roboarm.old
    cp -r --no-preserve=all /roboarm /roboarm.old
    rm -rf /roboarm/bin
    cp -r --no-preserve=all /boot/firmware/roboarm_updates /roboarm
    if [ -f "/roboarm/roboarm.service" ]; then
        echo "Neue Systemd-Unit-Datei gefunden, aktualisiere..."
        cp --no-preserve=all /roboarm/roboarm.service /usr/lib/systemd/system/roboarm.service
    fi

    rm -rf /boot/firmware/roboarm_updates
fi

#Hier kannst du deine Befehle einfügen, du kannst sleep 20;poweroff dahinterschreiben damit der pi danach wieder ausgeht.
#(und ja das sleep ist nötig weil diese Befehle noch beim Hochfahren ausgeführt werden und Herunterfahren da noch nicht geht.)
PORT=80

echo Der Port ist $PORT
#CORE_BIN="/pfad/zur/binary"
echo Starte $CORE_BIN # CORE_BIN ist in der SystemD Unit-Datei definiert, um es zu ändern kannst du die Zeile drüber auskommentieren
$CORE_BIN
CORE_STATUSCODE = $?
echo core ist mit code $CORE_STATUSCODE beendet worden.
exit $CORE_STATUSCODE