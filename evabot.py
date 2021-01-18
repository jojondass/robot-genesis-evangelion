import tweepy
import time
import sys
import pause
import datetime
import os.path
from glob import glob

Online = True

#key 
consumer_key = "yEp4rgBOnmqjsBOBmJ0VcIGlb"
consumer_secret = "KJFkYD8zypxxJ59GYouqvFLpEO0hANWvRvXTzTWSLoGGYzf3JN"
access_key = "864887996033748992-AKZBw2wreU8LpQajovh7uJc4RjiFSAL"
access_key_secret = "1gJ7auqctwB0HeyPuUGvA5I8lbKDr6FDOSNs6PGCtL4Nu"


# config
slogan = ""
path = ".images/"
interval = 20


def sendTweet(message,filename):
	print("sending", message, filename)
	if not Online:	# Offline mode always works
		return True
	else:
		try:
			api.update_with_media("images/"+str(filename))
			print("Sent!")
			return True
		except:
			print("Not sent!")
			return False

# state
lastImage = ""
imageNumber = 0

# load images
imageList = sorted(os.listdir("./images"))
listlength = len(imageList)
print(listlength, "files")


# resume state
if not os.path.isfile("state.txt"):
	saveFile = open("state.txt","w")
	saveFile.write(imageList[0])
	saveFile.close()
	print("Starting new save")
else:
	with open("state.txt","r") as saveFile:
		line = saveFile.readlines()
		lastImage = line[0]
		lastImage.replace("//",r"/")
	num = 0
	for image in imageList:
		if(image == lastImage):
			imageNumber = num
			break
		num = num + 1
	print("Resuming at " + imageList[imageNumber])

if imageNumber >= listlength-1:
	imageNumber = 0



if Online:
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_key,access_key_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	try:
		api.verify_credentials()
		print("twitter OK")
	except:
		print("twitter not OK, try again")
		sys.exit()
else:
	print("Offline testing mode")

#start posting
index = 0

while(1):
	for i in range(listlength):
		now = datetime.datetime.now()
		CanSleep = True
		try:
			index = imageNumber + i
			if index >= listlength:
				index = 0
			image = imageList[index]
			print("posting id", index)
			if sendTweet(slogan, image):
				try:
					with open("state.txt","w") as saveFile:
						next = index + 1 % (listlength - 1)
						saveFile.write(imageList[next])
						print ("saved")
				except:
					print("Progress not saved!!")
			else:
				print("Trying again")
				imageNumber -= 1
				CanSleep = False
		except:
			print("posting broke somewhere, trying again")
			i = i - 1
			CanSleep = False

		if CanSleep:
			pause.until(now + datetime.timedelta(minutes=interval))
		else:
			pause.until(now + datetime.timedelta(seconds = 5))	#try every 5 seconds
