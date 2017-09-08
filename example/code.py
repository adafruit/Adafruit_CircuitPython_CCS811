from board import *
import time
import busio

import adafruit_CCS811

myI2C = busio.I2C(SCL, SDA)

ccs = adafruit_CCS811.CCS811(myI2C)

#wait for the sensor to be ready and calibrate the thermistor
while not ccs.data_ready:
	pass
temp = ccs.temperature
ccs.temp_offset = temp - 25.0

while True:
	print("CO2: ", ccs.eCO2, " TVOC:", ccs.TVOC, " temp:", ccs.temperature)
	time.sleep(.5)
