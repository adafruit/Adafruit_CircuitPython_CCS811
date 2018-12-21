
Adafruit CircuitPython CCS811 Library
=====================================

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ccs811/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/ccs811/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_CCS811.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_CCS811
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
    i2c_bus = busio.I2C(SCL, SDA)

Once you have created the I2C interface object, you can use it to instantiate
the CCS811 object

.. code:: python

    ccs =  adafruit_ccs811.CCS811(i2c_bus)

Reading Sensor
--------------

To read the gas sensor and temperature simply read the attributes:

.. code:: python

    print("CO2: ", ccs.eco2, " TVOC:", ccs.tvoc, " temp:", ccs.temperature)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_CCS811/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-ccs811 --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
