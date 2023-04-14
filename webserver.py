from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import sqlite3

hostName = "0.0.0.0"
serverPort = 8080
con = sqlite3.connect('htm.db')
queryLatest = "SELECT moment, temperature, humidity FROM storage order by 1 desc LIMIT 1"
queryAll = "SELECT moment, temperature, humidity FROM storage order by 1"

class SensorItem:
	def __init__(self, moment, temperature, humidity):
		self.moment = moment
		self.temperature = temperature
		self.humidity = humidity

class MyServer(BaseHTTPRequestHandler):

	def _set_headers_html(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def _set_headers_json(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_GET(self):
		print("self.path=" + self.path)
		if self.path == '/json/all':
			cur = con.cursor()
			self._set_headers_json()
			sensorItemsList = []
			for row in cur.execute(queryAll):
				sensorItemsList.append(SensorItem(str(row[0]), str(row[1]), str(row[2])))
			sensorItemsStr = json.dumps([obj.__dict__ for obj in sensorItemsList])
			response = "{\"Temperatures\":" + sensorItemsStr + "}"
			response = bytes(response, 'utf-8')
			self.wfile.write(response)
		else:
			cur = con.cursor()
			self._set_headers_html()
			sensorItemsList = []
			self.wfile.write(bytes("<html><head><title>LATEST ROOM TEMP AND HUMIDITY</title></head>", "utf-8"))
			self.wfile.write(bytes("<body>", "utf-8"))
			for row in cur.execute(queryLatest):
				self.wfile.write(bytes("<p><H1>Moment: " + row[0] + " UTC</H1>", "utf-8"))
				self.wfile.write(bytes("<p><H1>Temperature: " + str(row[1]) + " &deg;C</H1>", "utf-8"))
				self.wfile.write(bytes("<p><H1>Humidity: " + str(row[2]) + " %</H1>", "utf-8"))
				self.wfile.write(bytes("<br/>", "utf-8"))
			self.wfile.write(bytes("</body>", "utf-8"))
			self.wfile.write(bytes("</html>", "utf-8"))


if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	con.close()
	print("Server stopped.")


