# Adafruit_CircuitPython_CCS811
circuit python driver for CCS811 air quality sensor
# Dependencies

This driver depends on the Register and Bus Device libraries. Please ensure they are also available on the CircuitPython filesystem. This is easily achieved by downloading a library and driver bundle.

# Usage Notes

see here for wiring and installation instructions:
https://learn.adafruit.com/ccs811-air-quality-sensor/circuit-python-example

Of course, you must import the library to use it:

```
import busio
import Adafruit_CCS811
```
The way to create an I2C object depends on the board you are using. For boards with labeled SCL and SDA pins, you can:

```
from board import *
```

You can also use pins defined by the onboard microcontroller through the microcontroller.pin module.

Now, to initialize the I2C bus:

```
myI2C = busio.I2C(SCL, SDA)
```

Once you have created the I2C interface object, you can use it to instantiate the CCS811 object

```
ccs =  Adafruit_CCS811.Adafruit_CCS811(myI2C)
```

# Reading Sensor

To read the gas sensor and thermistor you can do the following: 

```
if ccs.data_ready:
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			print("CO2: ", ccs.eCO2, " TVOC:", ccs.TVOC, " temp:", temp)
		else:
			print("ERROR!")
			while(1):
				pass
```
