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
#
# pylint: disable=E0401

"""
InnovateNow Outdoor Tracker configuration settings
"""
import inlogging as logging

# Log level
LOG_LEVEL = logging.INFO

# Customer
CUSTOMER = "InnovateNow"

# Device identifier for IoT environment
DEVICE_ID = "e3974fe0-18d9-11e8-9cfb-da0741d48d81"

# Serial Access
# True for development set this parameter to False for production
SERIAL_ACCESS = True

# Reset device after the specified seconds
DEVICE_RESET_AFTER_SECONDS = 7200

# FTP Access
# True for development set this parameter to False for production
FTP_ACCESS = True
FTP_USER = "InnovateNow"
FTP_PASSWORD = "123IN4567890"

# WLAN settings
WLAN_SSID = "HARTOG_GUEST" # SSID to connect to
WLAN_KEY = "1234567890"    # SSID key
WLAN_INT_ANTENNA = True    # True internal antenna else False

# BLE scan time in seconds before sending the results to AWS
# 240
SCAN_TIME_IN_SECONDS = 240

# Sensor I2C ENVIRONMENT_I2C_BUS
SENSOR_I2C_BUS = 0
SENSOR_I2C_SDA_PIN = 'P22'
SENSOR_I2C_SCL_PIN = 'P21'

# Environmental sensor is the BME280 sensor (temp, humidity and barometric pressure)
ENVIRONMENT_SENSOR_AVAILABLE = True
ENVIRONMENT_SENSOR_ID = '4c871008-18da-11e8-a5ea-96c32e02788c'

# GPS is an optional sensor
# When this setting is set to False you can add a fixed latitude/longitude
GPS_AVAILABLE = True
GPS_SENSOR_ID = '837ae7a6-18da-11e8-a5ea-96c32e02788c'
GPS_PORT = 'I2C'   # I2C or UART
GPS_UART_TX_PIN = 'P3'
GPS_UART_RX_PIN = 'P4'
GPS_FIXED_LATITUDE = None
GPS_FIXED_LONGITUDE = None

# Distance greater than last coords in NVRAM use the stored values
# Device should be static this rule will help to stabilize the coordinates
# when gps is activated on board
GPS_COORD_DIFF_UPDATE_RULE = 25 # meters

# NTP for setting the correct time
NTP_POOL_SERVER = "nl.pool.ntp.org"

# LED color configuration
LED_COLOR_ERROR = 0xff0000      # Red
LED_COLOR_WARNING = 0xff3700    # Orange
LED_COLOR_OK = 0xff00           # Green
LED_COLOR_OFF = 0x000000        # Off
