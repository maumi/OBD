import obd
import time
import datetime
import paho.mqtt.client as mqtt

#fMessung.write("Uhrzeit;RPM;Speed;Kuehlmittel;Tanklevel;Umgebungsdruck;Spannung")
#Alle neuen Werte
def new_rpm(r):
    try:
        if connection.status() != obd.OBDStatus.CAR_CONNECTED:
            client.publish("obd/state","ConnectionLost")
            quit()
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";"+str(r.value.magnitude)+";;;;;;")
            client.publish("obd/rpm", str(r.value.magnitude))
            #print("RPM: " + str(r.value.magnitude))
        else:
           stop = True 
           print("keine Werte bei rpm")

    except:
        stop = True
        print("rpm except")
        connection.stop()
        connection.unwatch_all()
        stop = False
        quit()

#Alle neuen Werte
def new_speed(r):
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";;"+str(r.value.magnitude)+";;;;;")
            client.publish("obd/speed", str(r.value.magnitude))
            #print("Speed: " + str(r.value.magnitude))

#Alle neuen Werte
def new_kuehlmittel(r):
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";;;"+str(r.value.magnitude)+";;;;")
            client.publish("obd/coolant", str(r.value.magnitude))
            #print("Kuehlmittel: "+ str(r.value.magnitude))

#Alle neuen Werte
def new_fuel(r):
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";;;;"+str(r.value.magnitude)+";;;")
            client.publish("obd/fuel", str(r.value.magnitude))
            #print("Tanklevel: "+ str(r.value.magnitude))

#Alle neuen Werte
def new_baro_pressure(r):
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";;;;;"+str(r.value.magnitude)+";;")
            client.publish("obd/barometric", str(r.value.magnitude))
            #print("Umgebungsdruck: "+ str(r.value.magnitude))

#Alle neuen Werte
def new_voltage(r):
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";;;;;;"+str(r.value.magnitude)+";")
            client.publish("obd/voltage", str(r.value.magnitude))
            #print("Spannung: "+ str(r.value.magnitude))

#Alle neuen Werte
def new_fuel_rate(r):
        if not r.is_null():
	    #fMessung.write("\r\n"+str(r.time)+";;;;;;;"+str(r.value.magnitude))
            client.publish("obd/FuelRate", str(r.value.magnitude))
            #print("Verbrauch: "+ str(r.value.magnitude))

def connect():
    global connection
    connection = obd.Async()
    connection.watch(obd.commands.RPM, callback=new_rpm)
    connection.watch(obd.commands.SPEED, callback=new_speed)
    connection.watch(obd.commands.COOLANT_TEMP, callback=new_kuehlmittel)
    connection.watch(obd.commands.FUEL_LEVEL, callback=new_fuel)
    connection.watch(obd.commands.BAROMETRIC_PRESSURE, callback=new_baro_pressure)
    connection.watch(obd.commands.CONTROL_MODULE_VOLTAGE, callback=new_voltage)
    #connection.watch(obd.commands.FUEL_RATE, callback=new_fuel_rate)
    connection.start()

# the callback will now be fired upon receipt of new values

client = mqtt.Client()

client.connect("localhost", 1883, 60)
client.loop_start()

stop = False

obd.logger.setLevel(obd.logging.DEBUG)
#Ein paar Mal versuchen, zu verbinden
i = 1
while i <= 100:
    try:
        connect()
        #connection = obd.Async()
        client.publish("obd/state","connected")
        break
    except:
        print(i)
        print("Nicht verbunden")
        i = i+1
        client.publish("obd/state", "ConnectionRetry")
        time.sleep(3)
        if i == 100:
            #print("Zu viele Versuche")
            client.publish("obd/state","ConnectionMaxRetry")
            connection.stop()
            connection.unwatch_all()
            quit()

time_now = datetime.datetime.now()
fName = "Leon-"+str(time_now.year)+"-"+str(time_now.month)+"-"+str(time_now.day)+"-"+str(time_now.hour)+"-"+str(time_now.minute)+".csv"
#fMessung = open(fName,"a")
#time.sleep(18000)
#connection.stop()
#client.publish("obd/state","ConnectionEnd")
while True:
    if stop == False:
        time.sleep(1)
    else:
        connection.stop()
        connection.unwatch_all()
        stop = False
        quit()
        #connect()
