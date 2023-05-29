# RPi4_WeatherStation
Repository storing the code for my weather station project. 

The script integrated_sensors.py is executed from the Raspbian command line using python3 as follows, once navigated to the correct directory:

"python3 integrated_sensors.py"

A tkinter-generated window will appear on the screen and after a brief period, display readings for temperature, humidity, and pressure. 
These readings will update every 2 seconds and the refreshed values will be shown on the window. The script will terminate when the
window is closed. 

Ensure that the DHT22 sensor and the BMP280 sensor are correctly connected to the Raspberry Pi 4's pinout or the scripts will run into errors. 
For example, the script here is written with the DHT22 sensor's DATA pin connected to GPIO 4 on the Raspberry Pi. Additionally, ensure that I2C
interfacing is enabled on the Raspberry Pi 4. 
