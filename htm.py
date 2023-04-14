import Adafruit_DHT
import sqlite3
import time
from time import gmtime, strftime
from datetime import datetime

con = sqlite3.connect('htm.db')
DHT_SENSOR = Adafruit_DHT.DHT22

#GPIO4
DHT_PIN = 4

while(True):
	currHour = strftime("%H", gmtime())
	#read_retry(sensor, pin, retries=15, delay_seconds=2, platform=None)
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN, 2)
	if humidity is not None and temperature is not None:
		temperature = round(temperature, 1)
		humidity = round(humidity, 1)
		con.execute("INSERT INTO storage(moment, temperature, humidity) VALUES (CURRENT_TIMESTAMP, ? , ?)", [temperature, humidity])
		print(str(datetime.now()) + "> Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
		if currHour == "00":
			print("oldest records removal starting...")
			con.execute("delete from storage where ROUND(JULIANDAY(CURRENT_TIMESTAMP) - JULIANDAY(moment)) > 30")
			print("oldest records removal DONE")
		con.commit()
		time.sleep(300) #sleep in seconds
	else:
		print(str(datetime.now()) + "> Failed to retrieve data from humidity/temperature sensor")
		time.sleep(5)
