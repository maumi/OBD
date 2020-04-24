import obd 
import time 
import datetime
import paho.mqtt.client as mqtt
from timeit import default_timer as timer

#MQTT Verbindung
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.loop_start()

#Versuche zu verbinden
try:
    conn = obd.OBD()
    client.publish("obd/state", "ConnectionEstablished")
except:
    print("Verbindung nicht geklappt")
    client.publish("obd/state", "ConnectionFailure")
    time.sleep(5)
    quit()

cSpeed = obd.commands.SPEED
cRpm = obd.commands.RPM
cCoolant = obd.commands.COOLANT_TEMP
cFuel = obd.commands.FUEL_LEVEL
cBarometric = obd.commands.BAROMETRIC_PRESSURE
#cFuelRate = obd.commands.FUEL_RATE
cVoltage = obd.commands.CONTROL_MODULE_VOLTAGE

while True:
    tStart = timer()
    rSpeed = conn.query(cSpeed)
    if not rSpeed.is_null():
        client.publish("obd/speed", str(rSpeed.value.magnitude))
        #print("Speed ",str(rSpeed.value.magnitude))
    else:
        print("Verbindung verloren. Ende")
        client.publish("obd/state", "ConnectionLost")
        time.sleep(5)
        quit()

    rRpm = conn.query(cRpm)
    if not rRpm.is_null():
        client.publish("obd/rpm", str(rRpm.value.magnitude))
        #print("RPM ",str(rRpm.value.magnitude))
    else:
        print("Verbindung verloren. Ende")
        client.publish("obd/state", "ConnectionLost")
        time.sleep(5)
        quit()

    rCoolant = conn.query(cCoolant)
    if not rCoolant.is_null():
        client.publish("obd/coolant", str(rCoolant.value.magnitude))
        #print("Coolant ",str(rCoolant.value.magnitude))
    else:
        print("Verbindung verloren. Ende")
        client.publish("obd/state", "ConnectionLost")
        time.sleep(5)
        quit()

    rFuel = conn.query(cFuel)
    if not rFuel.is_null():
        client.publish("obd/fuel", str(rFuel.value.magnitude))
        #print("Fuel ",str(rFuel.value.magnitude))
    else:
        print("Verbindung verloren. Ende")
        client.publish("obd/state", "ConnectionLost")
        time.sleep(5)
        quit()

    rBarometric = conn.query(cBarometric)
    if not rBarometric.is_null():
        client.publish("obd/barometric", str(rBarometric.value.magnitude))
        #print("Barometric ",str(rBarometric.value.magnitude))
    else:
        print("Verbindung verloren. Ende")
        client.publish("obd/state", "ConnectionLost")
        time.sleep(5)
        quit()

    #rFuelRate = conn.query(cFuelRate)
    #if not rFuelRate.is_null():
    #    client.publish("obd/FuelRate", str(rFuelRate.value.magnitude))
        #print("FuelRate ",str(rFuelRate.value.magnitude))
    #else:
    #    print("Verbindung verloren. Ende")
    #    client.publish("obd/state", "ConnectionLost")
    #    time.sleep(5)
    #    quit()

    rVoltage = conn.query(cVoltage)
    if not rVoltage.is_null():
        client.publish("obd/voltage", str(rVoltage.value.magnitude))
        #print("Voltage ",str(rVoltage.value.magnitude))
    else:
        print("Verbindung verloren. Ende")
        client.publish("obd/state", "ConnectionLost")
        time.sleep(5)
        quit()
    tEnd = timer()
    print("Abfragezeit: ",tEnd - tStart)

    time.sleep(1)
