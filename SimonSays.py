import time
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

### Constants and Variables ###
L1 = 6
L2 = 11
L3 = 10
L4 = 17
allLeds = [L1,L2,L3,L4]
B1 = 12
B2 = 8
B3 = 24
B4 = 18
N = 2
selectedColor = None
colors = []


### Functions ###

# gets the color pressed by the user
def getColor():
	while True:
		if(GPIO.input(B1)):
			return L1
		elif(GPIO.input(B2)):
			return L2
		elif(GPIO.input(B3)):
			return L3
		elif(GPIO.input(B4)):
			return L4

# plays the note for a given time
def playNote(t):
	GPIO.output(N,1)
	time.sleep(t)
	GPIO.output(N,0)

# lights a given LED for a given time
def lightLED(led,t):
	GPIO.output(led,1)
	time.sleep(t)
	GPIO.output(led,0)

# plays note and lights LED
def playColor(led,t):
	GPIO.output(led,1)
	GPIO.output(N,1)
	time.sleep(t)
	GPIO.output(N,0)
	GPIO.output(led,0)

# gets a random color/LED
def getRandColor():
	randomInt = random.randint(1,4)
	if(randomInt==1):
		return L1
	elif(randomInt==2):
		return L2
	elif(randomInt==3):
		return L3
	else:
		return L4	

# plays the sequence for the user
def playSequence():
	for led in colors:
		playColor(led,0.3)
		time.sleep(0.3)

# adds new random color to the colors array
def addColor():
	randomColor = getRandColor()
	colors.append(randomColor)

# terminates the game in an amazing way
def playEndGame():
	print "\n\n          *** THE USER HAS LOST! ***\n\n"
	time.sleep(0.1)
	GPIO.output(allLeds,1)
	for i in range(0,7):
		playNote(0.15)
		time.sleep(0.15)
	GPIO.output(allLeds,0)
	GPIO.cleanup()	# cleans up the "mess"
	exit()

# gets all the sequence, dealing with failure
def getColorSequence():
	selectedColor = None
	for color in colors:
		selectedColor = getColor()
		playColor(selectedColor,0.3)
		if(selectedColor != color):
			playEndGame()


### GPIO Setup ###
GPIO.setup(B1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B4,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(L1,GPIO.OUT)
GPIO.setup(L2,GPIO.OUT)
GPIO.setup(L3,GPIO.OUT)
GPIO.setup(L4,GPIO.OUT)
GPIO.setup(N,GPIO.OUT)

# LEDs start off
GPIO.output(L1,0)
GPIO.output(L2,0)
GPIO.output(L3,0)
GPIO.output(L4,0)

# Buzz sound warning the program started
for i in range(0,5):
	playNote(0.15)
	time.sleep(0.15)

# Wait two seconds before the game starts	
time.sleep(2)

try:
	while True:
		addColor()
		playSequence()
		getColorSequence()
		time.sleep(1)
	
except KeyboardInterrupt:
	playNote(0.5)
	GPIO.cleanup()
	print "\nProgram is over!"
