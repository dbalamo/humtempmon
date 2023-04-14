# humtempmon
humidity and temperature monitor with Python, Raspberry GPIO and DHT22 sensor

this is a simple project for monitoring room temperature and humidity,
using an old raspberry pi v1.0 GPIO ports and a cheap sensor (DHT22),
which you can buy anywhere for some €.

It's composed of two very simple python scripts,
one collecting data from the sensor and saving it inside an sqlite database,
and another exposing a basic http server to read data, while connected to your home network.

First of all, we need some work I won't cover here (refer to the appropriate doc for this) to : 

- prepare and sd card with Raspberry Pi OS (I chose Raspberry Pi OS Lite, as I only use it through ssh) ;
- connect the Raspberry to your home network and give it a fixed ip address (setup your router to reserve one for it) ;

then we need to install python3 environment and required libraries : 

	sudo apt install python3-gpiozero
	sudo apt-get install python3-dev python3-pip
	sudo python3 -m pip install --upgrade pip setuptools wheel
	sudo pip3 install Adafruit_Python_DHT
	sudo apt install sqlite3

the "Adafruit" is the library that we'll use to access GPIO pins.
Using this library, we could use three types of sensor, DHT11, DHT22, AM2302.

The Sqlite database was created using the following query : 

	CREATE TABLE storage(id INTEGER PRIMARY KEY, moment TIMESTAMP, temperature FLOAT, humidity FLOAT);

Launching the "htm.py" script with the command 
	python htm.py
we start the sensor reading (sensor is read every 5 minutes - it could be much more fast, the sensor has a new data every 2 secs) and data collecting.
We'll see inside the terminal the output for every read, like this : 

	2023-04-14 09:13:58.782882> Temp=20.1*C  Humidity=71.3%
	2023-04-14 09:19:00.054539> Temp=20.0*C  Humidity=71.2%
	2023-04-14 09:24:03.895987> Temp=20.0*C  Humidity=71.2%
	2023-04-14 09:29:05.124187> Temp=20.1*C  Humidity=71.2%
	2023-04-14 09:34:06.433277> Temp=20.1*C  Humidity=71.2%

or an error message, in case the sensor reading fails (sometime it could happen).
The script has also the capability of progressively erasing old data,
and every day erases data older than 30 days, to limit database size and increase data reading speed.

The datetime in the data is always in UTC.

Launching the "webserver.py" script we start the simple http server used to read database data from the network the Raspberry is connected on.
	python webserver.py

The http server listens on IP 0.0.0.0 (all network interfaces), and exposes two simple APIs : 

- an HTTP GET on the address : http://<IP ADDRESS>:8080 that answers in text/html , with the last sensor data read;

![humtempmon](https://user-images.githubusercontent.com/63041462/232042516-75a262f0-cdaf-4307-b555-2ca70bbccf5d.jpg)


- an HTTP GET on the address : http://<IP ADDRESS>:8080/json/all which answers in application/json, with all the data contained in the database.
The json structure is as follows : 

```yaml
{
  "Temperatures" : [
    {
      "moment" : "2023-04-13 11:24:51",
      "temperature" : "20.3",
      "humidity" : "64.7"
    },
    {
      "moment" : "2023-04-13 11:25:07",
      "temperature" : "20.3",
      "humidity" : "64.6"
    },
    {
      "moment" : "2023-04-13 11:25:35",
      "temperature" : "20.2",
      "humidity" : "64.8"
    },
    {
      "moment" : "2023-04-13 11:26:38",
      "temperature" : "20.2",
      "humidity" : "65.1"
    },
    {
      "moment" : "2023-04-13 11:34:27",
      "temperature" : "20.2",
      "humidity" : "65.6"
    },
    {
      "moment" : "2023-04-13 11:35:26",
      "temperature" : "20.2",
      "humidity" : "65.7"
    },
    {
      "moment" : "2023-04-13 11:36:27",
      "temperature" : "20.2",
      "humidity" : "65.7"
    }
  ]
}

```
For both APIs, the temperature is in Celsius degrees, and the humidity in percentage.

It's also possible to place the two scripts inside crontab, to make them start as the Raspberry powers up and make them collect data 24/7.

Feel free to improve and modify it as per your needs.

