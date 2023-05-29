import time
import tkinter as tk
from smbus2 import SMBus
import Adafruit_DHT
import threading

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
BMP280_I2CADDR = 0x76
BMP280_REGISTER_T1 = 0x88
BMP280_REGISTER_P1 = 0x8E
BMP280_REGISTER_CONTROL = 0xF4
BMP280_REGISTER_PRESSURE_DATA = 0xF7
BMP280_REGISTER_TEMP_DATA = 0xFA

bus = SMBus(1)
dig_T1 = bus.read_word_data(BMP280_I2CADDR, BMP280_REGISTER_T1)
dig_P1 = bus.read_word_data(BMP280_I2CADDR, BMP280_REGISTER_P1)
bus.write_byte_data(BMP280_I2CADDR, BMP280_REGISTER_CONTROL, 0x3F)

window = tk.Tk()
window.title("Weather Station")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = screen_width // 3
window_height = screen_height // 4
window.geometry(f"{window_width}x{window_height}")

temp_label = tk.Label(window, font=("Helvetica", 24))
temp_label.pack()
humidity_label = tk.Label(window, font=("Helvetica", 24))
humidity_label.pack()
pressure_label = tk.Label(window, font=("Helvetica", 24))
pressure_label.pack()

running = True

def update_sensor_data():
    while running:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            temp_label["text"] = "Temperature: {:.1f} °C".format(temperature)
            humidity_label["text"] = "Humidity: {:.1f} %".format(humidity)

        raw_temp = bus.read_word_data(BMP280_I2CADDR, BMP280_REGISTER_TEMP_DATA)
        var1 = ((((raw_temp/16384.0) - (dig_T1/1024.0)) * 2625))
        var2 = ((var1/4096.0) * var1)/16384.0
        var1 = ((var1 - var2)/4096.0) * (dig_T1)
        temp = var1 / 8192.0
        raw_press = bus.read_word_data(BMP280_I2CADDR, BMP280_REGISTER_PRESSURE_DATA)
        var1 = temp - 128000.0
        var2 = var1 * var1 * dig_P1
        var1 = ((var1 * dig_P1) / 131072.0) + (((dig_P1 * 32768.0) * var1) / 524288.0)
        press = 1048576.0 - raw_press
        press = (((press - (var2 / 4096.0)) * 6250.0) / var1)
        var1 = (dig_P1 * press) * press
        var2 = (press * press * press) / 128.0
        press = (press + (var1 + var2 + dig_P1) / 16.0) / 100
        pressure_label["text"] = "Pressure: {:.1f} hPa".format(press)

        window.update()
        time.sleep(2)

threading.Thread(target=update_sensor_data).start()
window.mainloop()

running = False
bus.close()
print("Stopped.")



