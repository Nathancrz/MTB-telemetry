import time
import threading
import Adafruit_ADS1x15
import board
import busio
import digitalio
import adafruit_ssd1306
from mpu6050 import mpu6050
import smbus

# Initialize MPU6050
accelerometer = mpu6050(0x68)
MPU6050_ADDRESS = 0x68
ACCEL_CONFIG = 0x1C
bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDRESS, ACCEL_CONFIG, 0x18)

# Initialize ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# Initialize OLED Display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Initialize Button
button = digitalio.DigitalInOut(board.D12)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

recording = False
lock = threading.Lock()

# Function to start or stop recording
def toggle_recording():
    global recording
    recording = not recording

def display_thread():
    while True:
        with lock:
            if recording:
                elapsed_time = round(time.time() - start_time, 1)
                oled.fill(0)
                oled.text(f"Recording... {elapsed_time}s", 0, 10, 1)
                oled.show()
        time.sleep(0.1) 

# Main loop
while True:
    if not recording and not button.value:
        toggle_recording()
        décompte = 3
        for i in range(3):
            with lock:
                oled.fill(0)
                oled.text(f"Recording starts in {décompte}", 0, 10, 1)
                oled.show()
                décompte -= 1
                time.sleep(1)
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        csv_file_name = f"/media/usb/bike_data_{current_time}.csv"
        with open(csv_file_name, 'a') as csv_file:
            csv_file.write("Time (ms), Potentiometer 0 (mm), Potentiometer 1 (mm), Acceleration X (m/s^2), Acceleration Y (m/s^2), Acceleration Z (m/s^2)\n")
            start_time = time.time()
            elapsed_time = 0
            prec = 0
            display_thread = threading.Thread(target=display_thread)
            display_thread.start()
            while recording:
                with lock:
                    prec, elapsed_time = elapsed_time, round(time.time() - start_time, 3)
                    if elapsed_time > prec:
                        csv_file.write(f"{elapsed_time},{adc.read_adc(0, gain=GAIN, data_rate=860)},{adc.read_adc(1, gain=GAIN, data_rate=860)},{','.join(map(str, accelerometer.get_accel_data().values()))}\n")
                if recording and not button.value:
                    toggle_recording()
                    with lock:
                        oled.fill(0)
                        oled.text("Done! "+ str(round(elapsed_time, 1))+" s", 0, 10, 1)
                        oled.show()
                        time.sleep(6)
    elif not recording:
        with lock:
            oled.fill(0)
            oled.text("Press to record", 0, 10, 1)
            oled.show()
        time.sleep(0.1)