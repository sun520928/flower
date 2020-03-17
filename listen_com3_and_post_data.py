# -*- coding: utf-8 -*-

import serial
import time
import requests
import json

SERVER_URL = 'http://127.0.0.1:5000/air'

ser = serial.Serial("COM3", 9600, timeout = 5)
ser.flushInput()

def main():
	while True:
		count = ser.inWaiting()
		if count !=0 :
			data = {}
			recv = ser.read(ser.in_waiting).decode("utf-8")
			print(time.time()," ---  recv --> ", recv)

			params = recv.split()
			for param in params:
				if len(param.split(':')) != 2:
					continue
				key = param.split(':')[0]
				value = param.split(':')[1]
				data[key] = value

			data_str = json.dumps(data)
			requests.post(url=SERVER_URL, data=data_str, headers={'Content-Type':'application/json'})
			print('post->%s %s' % (SERVER_URL, data_str))

		time.sleep(5)

if __name__ == '__main__':
	main()

