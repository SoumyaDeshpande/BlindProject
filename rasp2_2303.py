#The Blind Project
#Date: 03/23/2017
#Notifications provied to the user through speech for any obsticle in the path
#Raspberry Pi 3 and Ultrasonic sensors used
#---------------------------------------------------------------------------------
import threading
import time
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)

GPIO_TRIG1 = 21
GPIO_ECHO1 = 22
GPIO_TRIG2 = 23
GPIO_ECHO2 = 24
GPIO_PIEZO = 19

flag = 0
distance1 = 0

GPIO.setup(GPIO_TRIG2,GPIO.OUT)
GPIO.setup(GPIO_ECHO2,GPIO.IN)

//Used by ultrsonic sensor
def measure(GPIO_TRIGGER,GPIO_ECHO):
# This function measures a distance
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	start = time.time()

	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()

	elapsed = stop-start
	distance = (elapsed * 34300)/2

	return distance

def condition_sensor1(distance):
        if (distance <= 120.37):
                #thread_alert1.start()
                k = 0

def condition_sensor2():
        global distance1
        print distance1
        global flag
        
        if (distance1 <= 319.561 and flag == 0):
                print flag
                #os.system('espeak -ven+f "{0}"'.format("8 footsteps ahead"))
                t1 = threading.Thread(target = notify8 )
                #threads.append(t1)
                t1.start()
                t1.join()
                flag = 1
                return

        if (distance1 <= 206.545 and flag == 1):
                print flag
                #os.system('espeak -ven+f "{0}"'.format("4 footsteps ahead"))
                t2 = threading.Thread(target = notify4 )
                #threads.append(t2)
                t2.start()
                t2.join()
                flag = 2
                return

        if (distance1 >= 206.545 and flag == 2):
                flag = 0

class alert(threading.Thread):  #Notify through piezo -> Common
        def __init__(self, threadID, name, PIEZO, mark):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.PIEZO = PIEZO
                self.mark = mark
        def run(self):
                GPIO.output(self.PIEZO,True)
                time.sleep(1)
                GPIO.output(self.PIEZO,False)

class notify(threading.Thread): #Notify through speech
        def __init__(self, threadID, name, measure):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.measure = measure
        def run(self):
                if(measure == 8):
                        os.system('espeak -ven+f "{0}"'.format("8 footsteps ahead"))   
                elif(measure == 4):
                        os.system('espeak -ven+f "{0}"'.format("4 footsteps ahead"))

class sensor(threading.Thread): #Common for both sensors
        def __init__(self, threadID, name, TRIG, ECHO, mark):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.GPIO_TRIGGER = TRIG
                self.GPIO_ECHO = ECHO
                self.mark = mark
        def run(self):
                #buffer = 0.0
                global flag
                global distance1
                while True:
                        distance1 = measure(self.GPIO_TRIGGER,self.GPIO_ECHO)
                        #buffer
                        if(self.mark == 1):
                                condition_sensor1()
                        elif (self.mark == 2):
                                condition_sensor2()
                        time.sleep(1)
                        
#thread_sensor1 = sensor(1, "head", GPIO_TRIG1, GPIO_ECHO1, 1)
thread_sensor2 = sensor(2, "tail", GPIO_TRIG2, GPIO_ECHO2, 2)

#thread_alert1 = alert(3, "piezo", GPIO_PIEZO, 1)

#thread_sensor1.start()
thread_sensor2.start()
