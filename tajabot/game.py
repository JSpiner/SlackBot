from flask import Flask
import sys
import os
import time
import redis
import util
import key
from slackclient import SlackClient

def actionStart(data):
	sc.rtm_send_message(data['channel'], "Ready~")

	for i in range(4):
		time.sleep(1)
		if i!=3:
			sc.rtm_send_message(data['channel'], str(3-i) + "!")

	sc.rtm_send_message(data['channel'], "헬로우 월드!")

def actionType(data):
	sc.rtm_send_message(data['channel'], "test2")


print (sys.version)

print ("init client")
sc = SlackClient(key.SLACK_BOT_KEY)
print ("connecting...")
 
if sc.rtm_connect():
	print("connected!")

	while True:
		response = sc.rtm_read()

		if len(response) == 0: 
			continue

		
		# response는 배열로, 여러개가 담겨올수 있음
		for data in response:
			print(data)

			if ('type' in data) is False:
				continue			
			if data['type'] == 'message':
				
				if data['text'] == ".시작":
					actionStart(data)
				elif data['text'] == "헬로우 월드!":
					actionType(data)



else:
	print ("Connection Failed")