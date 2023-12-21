import spidev
import time
from datetime import datetime

# Initialize SPI connection
spi = spidev.SpiDev()
spi.open(0, 0)  # Using SPI bus 0, device (chip select) 0
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def read_pulse_value():
    pulse_channel = 2  # Replace with the correct channel number
    return read_channel(pulse_channel)  # Reading from the specified channel

def start_pulse_session(duration_seconds):
    pulse_data_list = []

    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        pulse_value = read_pulse_value()
        yield {'timestamp': datetime.now().isoformat(), 'value': pulse_value}
        time.sleep(5)  # Yield data every 5 seconds

    return pulse_data_list

if __name__ == "__main__":
    print(start_pulse_session(10))  # Test pulse session for 10 seconds
