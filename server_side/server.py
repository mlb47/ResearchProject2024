import socket
import bluetooth
from datetime import datetime 
import messageReceiver
from INA219 import INA219

def GetINA219Values(ina219):
	bus_voltage = ina219.getBusVoltage_V()             
	shunt_voltage = ina219.getShuntVoltage_mV() / 1000 
	current = ina219.getCurrent_mA()                   
	power = ina219.getPower_W() 
	percent = (bus_voltage - 6)/2.4*100
	if(percent > 100):percent = 100
	if(percent < 0):percent = 0
	return {
		'bus_voltage': bus_voltage,
		'shunt_voltage': shunt_voltage,
		'current': current,
		'power': power,
		'percent': percent
	}

#ina219 = INA219(i2c_bus=1, addr=0x42)
	
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 2
server.bind(("B8:27:EB:DD:F4:28", 2))
server.listen(1)

print("Waiting for connection")

client, address = server.accept()
print(f"Connection from {address}")

encryptionType = client.recv(1024)

encryptionType = int(encryptionType)

if(encryptionType == 2):
	key = messageReceiver.CCMgenerateKey()
elif(encryptionType == 3):	
	key = messageReceiver.ECBgenerateKey()
elif(encryptionType == 4):
	key = messageReceiver.GCMgenerateKey()
elif(encryptionType == 5):
	key = messageReceiver.CAST5generateKey()
elif(encryptionType == 6):
	key = messageReceiver.ChagenerateKey()
elif(encryptionType == 7):
	private_key = messageReceiver.RSAgeneratePrivateKey()
	key = messageReceiver.RSAserializePublicKey(private_key)
elif(encryptionType == 8):
	key = messageReceiver.TripleDESgenerateKey()
		
if(encryptionType != 1):
	client.send(key)

index = 0;
try:
	while True:
		
		data = client.recv(1024)
		
		if(encryptionType == 1):
			plaintext = data
		if(encryptionType == 2):
			delimiter = b'...'
			parts = data.split(delimiter)
			message = parts[0]
			nonce = parts[1]
			plaintext = messageReceiver.CCMdecrypt(message, key, nonce) 
		elif(encryptionType == 3):	
			message = data
			plaintext = messageReceiver.ECBdecrypt(message, key)
		elif(encryptionType == 4):
			delimiter = b'...'
			parts = data.split(delimiter)
			message = parts[0]
			nonce = parts[1]
			plaintext = messageReceiver.GCMdecrypt(message, key, nonce)
		elif(encryptionType == 5):
			delimiter = b'...'
			parts = data.split(delimiter)
			message = parts[0]
			iv = parts[1]	
			plaintext = messageReceiver.CAST5decrypt(message, key, iv)
		elif(encryptionType == 6):
			delimiter = b'...'
			parts = data.split(delimiter)
			message = parts[0]
			nonce = parts[1]
			plaintext = messageReceiver.Chadecrypt(message, key, nonce)
		elif(encryptionType == 7):
			message = data
			plaintext = messageReceiver.RSAdecrypt(message, private_key)
		elif(encryptionType == 8):
			delimiter = b'...'
			parts = data.split(delimiter)
			message = parts[0]
			iv = parts[1]	
			plaintext = messageReceiver.TripleDESdecrypt(message, key, iv)
		
		client.send(plaintext) 
		
		if(index==0):
			start_time  = str(datetime.now())
		index+=1
		end_time = str(datetime.now())
		#INA219Values = GetINA219Values(ina219)
		if not data:
			break

except OSError:
	pass

print(f"Start Time: 	{start_time}\n")
print(f"End time: {end_time}\n")
#print(f"Bus Voltage:  	{start_INA219Values['bus_voltage']:6.3f} V")
#print(f"Shunt Voltage:	{start_INA219Values['shunt_voltage']:9.6f} V")
#print(f"Current:       	{start_INA219Values['current']:9.6f} A")
#print(f"Power:         	{start_INA219Values['power']:6.3f} W")
#print(f"Percent:       	{start_INA219Values['percent']:3.1f}%")	
#print("")
print("\nDisconnected")

client.close()
server.close()
