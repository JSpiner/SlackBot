from flask import Flask
import sys
import os
import time
import redis
import util
import key
import random
from slackclient import SlackClient

def actionStart(data):
	sc.rtm_send_message(data['channel'], "Ready~")

	for i in range(4):
		time.sleep(1)
		if i!=3:
			sc.rtm_send_message(data['channel'], str(3-i) + "!")
	
	global textIndex
	global stTime
	textIndex = random.randrange(0,len(texts))
	stTime = time.time()
	print( textIndex)
	sc.rtm_send_message(data['channel'], texts[textIndex])

def actionType(data):
	print("actionType")
	
	distance = util.getEditDistance(data['text'], texts[textIndex])
	length = max(len(data['text']), len(texts[textIndex]))
	accur = (length - distance) / length * 100
	edTime = time.time()

	response = "accur : " + str(accur) + "% speed : " + str(edTime - stTime)
	sc.rtm_send_message(data['channel'], response)

	global textIndex
	textIndex = -1
print (sys.version)

texts = [
	"무궁화 꽃이 피었습니다.",
	"이것도 너프해 보시지!",
	"소프트웨어 마에스트로",
	"난 너를 사랑해 이 세상은 너 뿐이야"
]

textIndex = -1
stTime = 0

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
				print ('msg' + str(textIndex))
				if data['text'] == ".시작":
					actionStart(data)
				elif textIndex >= 0:
					actionType(data)



else:
	print ("Connection Failed")