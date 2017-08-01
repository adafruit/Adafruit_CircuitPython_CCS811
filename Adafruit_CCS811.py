# The MIT License (MIT)
#
# Copyright (c) 2017 Dean Miller for Adafruit Industries.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`Adafruit_CCS811` - CCS811 air quality sensor
====================================================
This library supports the use of the CCS811 in CircuitPython. This base
class is inherited by the chip-specific subclasses.
Functions are included for reading and writing registers and manipulating
datetime objects.
Author(s): Dean Miller for Adafruit Industries.
Date: June 2017
Affiliation: Adafruit Industries
Implementation Notes
--------------------
**Hardware:**
*
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards: https://github.com/adafruit/micropython/releases
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
**Notes:**
#. Datasheet: 
"""

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit
from adafruit_register import i2c_bits
import time
import math

CCS811_ALG_RESULT_DATA = const(0x02)
CCS811_RAW_DATA = const(0x03)
CCS811_ENV_DATA = const(0x05)
CCS811_NTC = const(0x06)
CCS811_THRESHOLDS = const(0x10)

'''
CCS811_BASELINE = 0x11
CCS811_HW_ID = 0x20
CCS811_HW_VERSION = 0x21
CCS811_FW_BOOT_VERSION = 0x23
CCS811_FW_APP_VERSION = 0x24
CCS811_ERROR_ID = 0xE0
'''

CCS811_SW_RESET = const(0xFF)

'''
CCS811_BOOTLOADER_APP_ERASE = 0xF1
CCS811_BOOTLOADER_APP_DATA = 0xF2
CCS811_BOOTLOADER_APP_VERIFY = 0xF3
CCS811_BOOTLOADER_APP_START = 0xF4
'''

CCS811_DRIVE_MODE_IDLE = const(0x00)
CCS811_DRIVE_MODE_1SEC = const(0x01)
CCS811_DRIVE_MODE_10SEC = const(0x02)
CCS811_DRIVE_MODE_60SEC = const(0x03)
CCS811_DRIVE_MODE_250MS = const(0x04)

CCS811_HW_ID_CODE = const(0x81)
CCS811_REF_RESISTOR = const(100000)

class Adafruit_CCS811:
	#set up the registers
	#self.status = Adafruit_bitfield([('ERROR' , 1), ('unused', 2), ('DATA_READY' , 1), ('APP_VALID', 1), ('unused2' , 2), ('FW_MODE' , 1)])
	error = i2c_bit.ROBit(0x00, 0)
	data_ready = i2c_bit.ROBit(0x00, 3)
	app_valid = i2c_bit.ROBit(0x00, 4)
	fw_mode = i2c_bit.ROBit(0x00, 7)

	hw_id = i2c_bits.ROBits(8, 0x20, 0)

	#self.meas_mode = Adafruit_bitfield([('unused', 2), ('INT_THRESH', 1), ('INT_DATARDY', 1), ('DRIVE_MODE', 3)])
	int_thresh = i2c_bit.RWBit(0x01, 2)
	interrupt_enabled = i2c_bit.RWBit(0x01, 3)
	drive_mode = i2c_bits.RWBits(3, 0x01, 4)

	#self.error_id = Adafruit_bitfield([('WRITE_REG_INVALID', 1), ('READ_REG_INVALID', 1), ('MEASMODE_INVALID', 1), ('MAX_RESISTANCE', 1), ('HEATER_FAULT', 1), ('HEATER_SUPPLY', 1)])

	TVOC = 0
	eCO2 = 0

	def __init__(self, i2c, addr=0x5A):
		self.i2c_device = I2CDevice(i2c, addr)

			#check that the HW id is correct
		if self.hw_id != CCS811_HW_ID_CODE:
			raise RuntimeException("Device ID returned is not correct! Please check your wiring.")
		
		#try to start the app
		buf = bytearray(1)
		buf[0] = 0xF4
		self.i2c_device.write(buf, end=1, stop=True)
		time.sleep(.1)
		
		#make sure there are no errors and we have entered application mode
		if self.checkError():
			raise RuntimeException("Device returned an Error! Try removing and reapplying power to the device and running the code again.")
		if not self.fw_mode:
			raise RuntimeException("Device did not enter application mode! If you got here, there may be a problem with the firmware on your sensor.")
		
		self.interrupt_enabled = False
		
		#default to read every second
		self.setDriveMode(CCS811_DRIVE_MODE_1SEC)


	def setDriveMode(self, mode):
		self.drive_mode = mode


	def available(self):
		return self.data_ready


	def readData(self):

		if not self.data_ready:
			return False
		else:
			buf = bytearray(9)
			buf[0] = CCS811_ALG_RESULT_DATA
			self.i2c_device.write(buf, end=1, stop=False)
			self.i2c_device.read_into(buf, start=1)

			self.eCO2 = (buf[1] << 8) | (buf[2])
			self.TVOC = (buf[3] << 8) | (buf[4])
			
			if self.error:
				return buf[6]
				
			else:
				return 0
		


	def setEnvironmentalData(self, humidity, temperature):

		''' Humidity is stored as an unsigned 16 bits in 1/512%RH. The
		default value is 50% = 0x64, 0x00. As an example 48.5%
		humidity would be 0x61, 0x00.'''
		
		''' Temperature is stored as an unsigned 16 bits integer in 1/512
		degrees there is an offset: 0 maps to -25C. The default value is
		25C = 0x64, 0x00. As an example 23.5% temperature would be
		0x61, 0x00.
		The internal algorithm uses these values (or default values if
		not set by the application) to compensate for changes in
		relative humidity and ambient temperature.'''
		
		hum_perc = humidity << 1
		
		parts = math.fmod(temperature)
		fractional = parts[0]
		temperature = parts[1]

		temp_high = ((temperature + 25) << 9)
		temp_low = ((fractional / 0.001953125) & 0x1FF)
		
		temp_conv = (temp_high | temp_low)

		buf = bytearray([CCS811_ENV_DATA, hum_perc, 0x00,((temp_conv >> 8) & 0xFF), (temp_conv & 0xFF)])
		
		self.i2c_device.write(buf)



	#calculate temperature based on the NTC register
	def calculateTemperature(self):
		buf = bytearray(5)
		buf[0] = CCS811_NTC
		self.i2c_device.write(buf, end=1, stop=False)
		self.i2c_device.read_into(buf, start=1)

		VRref = (buf[1] << 8) | buf[2]
		VRntc = (buf[3] << 8) | buf[4]
		Rntc = (float(VRntc) * float(CCS811_REF_RESISTOR) / float(VRref) )

		#Code from Milan Malesevic and Zoran Stupic, 2011,
		#Modified by Max Mayfield,
		temp = math.log(Rntc)
		temp = 1. / (0.001129148 + (0.000234125 * temp) + (0.0000000876741 * temp * temp * temp))
		temp = temp - 273.15  # Convert Kelvin to Celsius
		
	 	return temp


	def setThresholds(self, low_med, med_high, hysteresis):
		buf = bytearray([CCS811_THRESHOLDS, ((low_med >> 8) & 0xF), (low_med & 0xF), ((med_high >> 8) & 0xF), (med_high & 0xF), hysteresis ])
		self.i2c_device.write(buf)


	def SWReset(self):

		#reset sequence from the datasheet
		seq = bytearray([CCS811_SW_RESET, 0x11, 0xE5, 0x72, 0x8A])
		self.i2c_device.write(seq)


	def checkError(self):
		return self.error