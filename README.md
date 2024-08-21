### Performance of Encrypted Bluetooth over Raspberry Pi

These programs were developed in python on Raspberry Pis to study the latency and power consumption of various algorithms over a bluetooth connection.

The devices are connected via bluetooth using the `pybluez` library.

8 encryption algorithms were implemented using the `pyca/cryptography` library. 

Power consumption was measured using `UPS HAT by Waveshare`. 

The client_side and server_side folders contain code designed to run on their respective raspberry pis.

The programs can be run using the `client.py` file in client_side and `server.py` in server_side.
