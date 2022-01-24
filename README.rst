
Adafruit CircuitPython CCS811 Library
=====================================

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ccs811/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ccs811/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_CCS811/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_CCS811/actions/
    :alt: Build Status

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

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ccs811/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ccs811

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ccs811

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-ccs811

Usage Notes
===========

See `the guide <https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor/python-circuitpython>`_
for wiring and installation instructions.

Of course, you must import the library to use it:

.. code:: python

    import busio
    import adafruit_ccs811

Next, initialize the I2C bus object.

.. code:: python

    from board import *
    i2c = board.I2C()   # uses board.SCL and board.SDA

Once you have created the I2C interface object, you can use it to instantiate
the CCS811 object

.. code:: python

    ccs =  adafruit_ccs811.CCS811(i2c)

Reading Sensor
--------------

To read the gas sensor simply read the attributes:

.. code:: python

    print("CO2: ", ccs.eco2, " TVOC:", ccs.tvoc)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ccs811/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CCS811/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
