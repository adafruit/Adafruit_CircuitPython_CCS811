
Adafruit CircuitPython CCS811 Library
=====================================

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ccs811/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/ccs811/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

CircuitPython driver for the `CCS811 air quality sensor <https://www.adafruit.com/product/3566>`_.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Notes
===========

See `the guide <https://learn.adafruit.com/ccs811-air-quality-sensor/circuit-python-example>`_
for wiring and installation instructions.

Of course, you must import the library to use it:

.. code:: python

    import busio
    import adafruit_CCS811

Next, initialize the I2C bus object.

.. code:: python

    from board import *
    myI2C = busio.I2C(SCL, SDA)

Once you have created the I2C interface object, you can use it to instantiate
the CCS811 object

.. code:: python

    ccs =  adafruit_ccs811.CCS811(myI2C)

Reading Sensor
--------------

To read the gas sensor and temperature simply read the attributes:

.. code:: python

    print("CO2: ", ccs.eCO2, " TVOC:", ccs.TVOC, " temp:", ccs.temperature)

API Reference
=============

.. toctree::
   :maxdepth: 2

   api
