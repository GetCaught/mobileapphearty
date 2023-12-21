import json
import time
from datetime import datetime
import spidev
import RPi.GPIO as GPIO

# SPI Setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CE0)
spi.max_speed_hz = 1350000

# GPIO Setup for Buzzer
BUZZER_PIN = 27
# GPIO Setup for LEDs
RED_LED_PIN = 21
GREEN_LED_PIN = 20

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def read_ekg_value():
    return read_channel(0)  # Reading from channel 0

def start_ekg_session(duration_seconds):
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        ekg_value = read_ekg_value()
        yield {'timestamp': datetime.now().isoformat(), 'value': ekg_value}
        time.sleep(5)  # Yield data every 5 seconds
    
    # Turn on red LED and buzzer for session start
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    buzzer = GPIO.PWM(BUZZER_PIN, 650)
    buzzer.start(50)
    time.sleep(2)
    buzzer.stop()

    ekg_data_list = []
    start_time = time.time()

    while time.time() - start_time < duration_seconds:
        ekg_value = read_ekg_value()
        ekg_data_list.append({'timestamp': datetime.now().isoformat(), 'value': ekg_value})
        time.sleep(0.5)
    

    # Turn off red LED, turn on green LED, and emit two quick buzzes for session end
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    buzzer = GPIO.PWM(BUZZER_PIN, 250)
    buzzer.start(50)
    for _ in range(2):
        time.sleep(0.1)
    buzzer.stop()

    return json.dumps(ekg_data_list)

def cleanup():
    """Cleanup GPIO resources"""
    GPIO.cleanup()

if __name__ == "__main__":
    # Uncomment the line below for testing
    print(start_ekg_session(10))  # Start an EKG session for 10 seconds
    cleanup()  # Clean up GPIO resources after the test
