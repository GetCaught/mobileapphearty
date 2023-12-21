import ble_server
import ekg_data

def start_ble_service():
    ble_server.start_bleno()  # Ensure this function exists and is correctly implemented in ble_server.py

def stop_ble_service():
    try:
        ble_server.stop_bleno()  # Ensure this function exists and is correctly implemented in ble_server.py
        ekg_data.spi.close()  # Close the SPI connection
    except Exception as e:
        print(f"Error during BLE service shutdown: {e}")

def stop_ble_service():
    try:
        ble_server.stop_bleno()  # Ensure this function exists and is correctly implemented in ble_server.py
        ekg_data.spi.close()  # Close the SPI connection
        ekg_data.cleanup()  # Clean up GPIO resources
    except Exception as e:
        print(f"Error during BLE service shutdown: {e}")


if __name__ == '__main__':
    try:
        start_ble_service()
        print("Service is running. Press Ctrl+C to stop.")
        while True:
            pass  # Keep the program running to maintain the BLE service
    except KeyboardInterrupt:
        print("Stopping BLE service...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        stop_ble_service()
