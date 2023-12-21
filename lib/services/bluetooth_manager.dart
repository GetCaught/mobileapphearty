import 'dart:async';
import 'package:flutter/services.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

enum BluetoothConnectionState {
  disconnected,
  connecting,
  connected,
}

class BluetoothManager {
  BluetoothDevice? targetDevice;
  BluetoothCharacteristic? targetCharacteristic;
  Stream<BluetoothConnectionState> get connectionStateStream =>
      _connectionStateController.stream;
  final _connectionStateController =
      StreamController<BluetoothConnectionState>();
  Stream<List<int>>? dataStream; // Stream for ECG data
  VoidCallback? onSaveGraph;

  void initialize() {
    FlutterBluePlus.adapterState.listen((state) {
      if (state == BluetoothAdapterState.off) {
        // Handle Bluetooth off
      } else if (state == BluetoothAdapterState.on) {
        // Handle Bluetooth on
      }
    });
  }

  Future<String?> startScanning() async {
    try {
      FlutterBluePlus.startScan(timeout: const Duration(seconds: 4));

      FlutterBluePlus.scanResults.listen((results) {
        for (ScanResult r in results) {
          if (r.device.platformName == 'efepi') {
            targetDevice = r.device;
            connectToDevice();
            FlutterBluePlus.stopScan();
            break;
          }
        }
      });
      return null; // No error
    } on PlatformException catch (e) {
      if (e.code == 'startScan' && e.message == 'bluetooth must be turned on') {
        return 'Bluetooth skal være tændt for at forbinde.';
      }
      return 'En uforventet fejl opstod.';
    }
  }

  void connectToDevice() async {
    await targetDevice?.connect();
    discoverServices();
  }

  void discoverServices() async {
    if (targetDevice == null) return;

    List<BluetoothService> services = await targetDevice!.discoverServices();
    for (BluetoothService service in services) {
      if (service.uuid.toString() == '12345678-1234-5678-1234-56789abcdef1') {
        var characteristics = service.characteristics;
        for (BluetoothCharacteristic c in characteristics) {
          if (c.uuid.toString() == '12345678-1234-5678-1234-56789abcdef2') {
            targetCharacteristic = c;
            await c.setNotifyValue(true);
            dataStream = c.lastValueStream;
            break;
          }
        }
      }
    }
  }
}
