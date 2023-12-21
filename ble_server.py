from pybleno import Bleno, BlenoPrimaryService, Characteristic
import ekg_data
import json
import pulse_data
import time

class SimpleCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': '12345678-1234-5678-1234-56789abcdef2',
            'properties': ['read'],
            'value': None
        })

    def onReadRequest(self, offset, callback):
        print("Read request received - Starting EKG and Pulse data collection")

        ekg_session = ekg_data.start_ekg_session(30)
        pulse_session = pulse_data.start_pulse_session(30)

        ekg_data_list = []
        pulse_data_list = []

        for _ in range(6):  # Assuming 30 seconds / 5 seconds interval
            ekg_data_point = next(ekg_session, None)
            pulse_data_point = next(pulse_session, None)

            if ekg_data_point and pulse_data_point:
                print(f"EKG Data: {ekg_data_point}, Pulse Data: {pulse_data_point}")

            time.sleep(5)

        combined_data = {
            'ekg_data': ekg_data_list,
            'pulse_data': pulse_data_list
        }

        print("EKG and Pulse data collection finished - Sending data")
        json_data = json.dumps(combined_data)
        callback(Characteristic.RESULT_SUCCESS, bytearray(json_data, 'utf-8'))

bleno = Bleno()

def on_state_change(state):
    print(f"Bluetooth State change: {state}")
    if state == 'poweredOn':
        bleno.startAdvertising('efepi', ['12345678-1234-5678-1234-56789abcdef0'])

bleno.on('stateChange', on_state_change)

def on_advertising_start(error):
    print(f"Bluetooth Advertising start: {'error ' + str(error) if error else 'success'}")
    if not error:
        service = BlenoPrimaryService({
            'uuid': '12345678-1234-5678-1234-56789abcdef1',
            'characteristics': [SimpleCharacteristic()]
        })
        bleno.setServices([service])

bleno.on('advertisingStart', on_advertising_start)

def start_bleno():
    bleno.start()

def stop_bleno():
    bleno.stopAdvertising()
    bleno.disconnect()