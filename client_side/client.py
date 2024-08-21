#!/usr/bin/env python3
import socket
import bluetooth
import pandas as pd
from datetime import datetime
import messageSender
from INA219 import INA219

def PrintData(start_time, end_time, INA219Values):
    print(f"Start time: {start_time}\n")
    print(f"End time: {end_time}\n")
    print("INA129 Values: \n")
    print(f"Bus Voltage: {INA219Values['bus_voltage']:6.3f} V")
    print(f"Shunt Voltage: {INA219Values['shunt_voltage']:9.6f} V")
    print(f"Current: {INA219Values['current']:9.6f} A")
    print(f"Power: {INA219Values['power']:6.3f} W")
    print(f"Percent: {INA219Values['percent']:3.1f}%")
    print("")

def GetINA219Values(ina219):
    bus_voltage = ina219.getBusVoltage_V()
    shunt_voltage = ina219.getShuntVoltage_mV() / 1000
    current = ina219.getCurrent_mA()
    power = ina219.getPower_W()
    percent = (bus_voltage - 6)/2.4*100
    if(percent>100):percent=100
    if(percent<0):percent=0
    
    return {
        'bus_voltage': bus_voltage,
        'shunt_voltage': shunt_voltage,
        'current': current,
        'power': power,
        'percent': percent
    }

def getDataFrame(filename):
    return pd.read_excel('data.xlsx')

def SendUnencryptedData(dataframe):
    ina219 = INA219(i2c_bus=1, addr=0x42)
    for index, row in dataframe.iterrows():
        try:
            row_string = " ".join([str(value) for value in row.values])
            message = row_string.encode()
            client.send(message)
            
            data = client.recv(1024)
            print(f'At index  # {index}\n')
            print(f"Received: {data.decode('utf-8')}" + " @ {} \n".format(str(datetime.now()))) 
            
            if (index == 0):
                start_time = str(datetime.now())
            end_time = str(datetime.now())
            INA219Values = GetINA219Values(ina219)
        except OSError:
            pass
    PrintData(start_time, end_time, INA219Values)

def SendEncryptedData(dataframe, key, encryptionType):
    ina219 = INA219(i2c_bus=1, addr=0x42)
    for index, row in dataframe.iterrows():
        try:
            row_string = " ".join([str(value) for value in row.values])
                
            if (encryptionType == 2):
                nonce = messageSender.generateNonce()
                encryptedMessage = messageSender.CCMencrypt(row_string.encode(), key, nonce)
                delimiter = b'...'
                client.send(encryptedMessage + delimiter + nonce)
            elif (encryptionType == 3):
                encryptedMessage = messageSender.ECBencrypt(row_string.encode(), key)
                client.send(encryptedMessage)
            elif (encryptionType == 4):
                nonce = messageSender.generateNonce()
                encryptedMessage = messageSender.GCMencrypt(row_string.encode(), key, nonce)
                delimiter = b'...'
                client.send(encryptedMessage + delimiter + nonce)
            elif (encryptionType == 5):
                iv = messageSender.generateIV()
                encryptedMessage = messageSender.CAST5encrypt(row_string.encode(), key, iv)
                delimiter = b'...'
                client.send(encryptedMessage + delimiter + iv)
            elif (encryptionType == 6):
                nonce = messageSender.generateNonce()
                encryptedMessage = messageSender.Chaencrypt(row_string.encode(), key, nonce)
                delimiter = b'...'
                client.send(encryptedMessage + delimiter + nonce)
            elif (encryptionType == 7):
                encryptedMessage = messageSender.RSAencrypt(row_string.encode(), key)
                client.send(encryptedMessage)
            elif (encryptionType == 8):
                iv = messageSender.generateIV()
                encryptedMessage = messageSender.TripleDESencrypt(row_string.encode(), key, iv)
                delimiter = b'...'
                client.send(encryptedMessage + delimiter + iv)
        
            data = client.recv(1024)
            print(f'At index  # {index}\n')
            print(f"Received: {data.decode('utf-8')}" + " @ {} \n".format(str(datetime.now()))) 
            
            if (index == 0):
                start_time = str(datetime.now())
            end_time = str(datetime.now())
            INA219Values = GetINA219Values(ina219)
        except OSError:
            pass
    PrintData(start_time, end_time, INA219Values)
    
client = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client.connect(("B8:27:EB:DD:F4:28", 2))

print("Connected")

print("These are the available methods for sending the data:\n")
print("1. Unencrypted\n")
print("2. AES-CCM\n")
print("3. AES-ECB\n")
print("4. AES-GCM\n")
print("5. CAST5\n")
print("6. ChaCha20Poly1305\n")
print("7. RSA\n")
print("8. TripleDES\n")

encryptionType = input("Please enter the number associated with the encryption method of your choosing from the above list to send the data:\n")

client.send(encryptionType)

dataframe = getDataFrame('data.xlsx')
encryptionType = int(encryptionType)

if encryptionType == 1:
    SendUnencryptedData(dataframe)
else:
    key = client.recv(1024)
    print(f"Received key {key}")
    SendEncryptedData(dataframe, key, encryptionType)
                        
print("Disconnected")
client.close()
