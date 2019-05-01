# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 20:37:25 2019

@author: hudew
"""

"""trycode.py is the code run on the raspberry pi on each pods. 
There are two steps:
    1, Pods work as subscriber, and the main pod/laptop works as the publisher. The purpose of this step is
    the laptop publish a time to activate all the pods together.
    2, The second step is all pods work as publisher and the laptop works as subscriber. Every pod has its own 
    independent channel. Once there is an update on the channel, the main laptop will receive new data."""

#Reads nine VL53L1 sensors using the PyVL53L1 library and the Python multiprocessing library for improved performance relative to threading
from multiprocessing import Process, Array, Value
import RPi.GPIO as GPIO
import PyVL53L1
import time
import datetime
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

##############   STEP 1: Receive the command of the activation time ###############
# msg is the time stamp of the activation
msg = subscribe.simple('main_Pi',hostname='192.168.1.110')
print('%s %s %s' % (msg.topic,':', str(msg.payload)))

idx = time.time()
switch = float(msg.payload)
 
while int(switch-idx) > 0: 
    idx = time.time()
    print('wait...')
    time.sleep(1)

# define a name for the pod
Pod = 'worker_9'

#Configuration parameters
INTEGRATION_TIME = 150
BLANKING_TIME = 155
STD_DEV_Sensor = 8

#List of GPIO pins corresponding to sensor enable lines
sensor_enable_GPIO = [4, 17, 27, 22, 10, 9, 11, 5, 6]

#Global sensor variables
#Program was designed so that a variable will never be written to simultaneously by two processes at the same time, so no need for lock
distances = Array('i', [0]*9, lock=False)
statuses = Array('i', [0]*9, lock=False)
complete = Array('i', [0]*9, lock=False)
begin = Value("i", 0, lock=False)

#Sensor handler processes
def Sensor0():
	PyVL53L1.StartMeasurement_0()
	while True:
		try:
			if begin.value == 1 and complete[0] == 0:
				distances[0], statuses[0] = PyVL53L1.Measure_0()
				complete[0] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_0()
			break
def Sensor1():
	PyVL53L1.StartMeasurement_1()
	while True:
		try:
			if begin.value == 1 and complete[1] == 0:
				distances[1], statuses[1] = PyVL53L1.Measure_1()
				complete[1] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_1()
			break
def Sensor2():
	PyVL53L1.StartMeasurement_2()
	while True:
		try:
			if begin.value == 1 and complete[2] == 0:
				distances[2], statuses[2] = PyVL53L1.Measure_2()
				complete[2] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_2()
			break
def Sensor3():
	PyVL53L1.StartMeasurement_3()
	while True:
		try:
			if begin.value == 1 and complete[3] == 0:
				distances[3], statuses[3] = PyVL53L1.Measure_3()
				complete[3] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_3()
			break
def Sensor4():
	PyVL53L1.StartMeasurement_4()
	while True:
		try:
			if begin.value == 1 and complete[4] == 0:
				distances[4], statuses[4] = PyVL53L1.Measure_4()
				complete[4] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_4()
			break
def Sensor5():
	PyVL53L1.StartMeasurement_5()
	while True:
		try:
			if begin.value == 1 and complete[5] == 0:
				distances[5], statuses[5] = PyVL53L1.Measure_5()
				complete[5] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_5()
			break
def Sensor6():
	PyVL53L1.StartMeasurement_6()
	while True:
		try:
			if begin.value == 1 and complete[6] == 0:
				distances[6], statuses[6] = PyVL53L1.Measure_6()
				complete[6] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_6()
			break
def Sensor7():
	PyVL53L1.StartMeasurement_7()
	while True:
		try:
			if begin.value == 1 and complete[7] == 0:
				distances[7], statuses[7] = PyVL53L1.Measure_7()
				complete[7] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_7()
			break
def Sensor8():
	PyVL53L1.StartMeasurement_8()
	while True:
		try:
			if begin.value == 1 and complete[8] == 0:
				distances[8], statuses[8] = PyVL53L1.Measure_8()
				complete[8] = 1
		except(KeyboardInterrupt):
			PyVL53L1.StopMeasurement_8()
			break

#Begin by disabling all sensors
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_enable_GPIO,GPIO.OUT)
GPIO.output(sensor_enable_GPIO,GPIO.LOW) 
    
############  STEP 2: Read distance value from sensors and update the channel ##############
# The main function: use multithreading to have all sensors work simultaneously. And pods become publishers.
def run():
	#Initialize all sensors
	GPIO.output(sensor_enable_GPIO[0], GPIO.HIGH)
	a = PyVL53L1.initialize_0(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x10)
	print("Initialized sensor 0 at pin " + str(sensor_enable_GPIO[0]) + " at address 0x" + format(a, '02x'))

	GPIO.output(sensor_enable_GPIO[1], GPIO.HIGH)
	b = PyVL53L1.initialize_1(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x20)
	print("Initialized sensor 1 at pin " + str(sensor_enable_GPIO[1]) + " at address 0x" + format(b, '02x'))

	GPIO.output(sensor_enable_GPIO[2], GPIO.HIGH)
	c = PyVL53L1.initialize_2(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x30)
	print("Initialized sensor 2 at pin " + str(sensor_enable_GPIO[2]) + " at address 0x" + format(c, '02x'))

	GPIO.output(sensor_enable_GPIO[3], GPIO.HIGH)
	d = PyVL53L1.initialize_3(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x40)
	print("Initialized sensor 3 at pin " + str(sensor_enable_GPIO[3]) + " at address 0x" + format(d, '02x'))

	GPIO.output(sensor_enable_GPIO[4], GPIO.HIGH)
	e = PyVL53L1.initialize_4(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x50)
	print("Initialized sensor 4 at pin " + str(sensor_enable_GPIO[4]) + " at address 0x" + format(e, '02x'))

	GPIO.output(sensor_enable_GPIO[5], GPIO.HIGH)
	f = PyVL53L1.initialize_5(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x60)
	print("Initialized sensor 5 at pin " + str(sensor_enable_GPIO[5]) + " at address 0x" + format(f, '02x'))

	GPIO.output(sensor_enable_GPIO[6], GPIO.HIGH)
	g = PyVL53L1.initialize_6(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x70)
	print("Initialized sensor 6 at pin " + str(sensor_enable_GPIO[6]) + " at address 0x" + format(g, '02x'))

	GPIO.output(sensor_enable_GPIO[7], GPIO.HIGH)
	h = PyVL53L1.initialize_7(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x80)
	print("Initialized sensor 7 at pin " + str(sensor_enable_GPIO[7]) + " at address 0x" + format(h, '02x'))

	GPIO.output(sensor_enable_GPIO[8], GPIO.HIGH)
	h = PyVL53L1.initialize_8(1, INTEGRATION_TIME*1000, BLANKING_TIME, 0x90)
	print("Initialized sensor 8 at pin " + str(sensor_enable_GPIO[8]) + " at address 0x" + format(h, '02x'))

	#Start all processes
	Process_0 = Process(target=Sensor0)
	Process_1 = Process(target=Sensor1)
	Process_2 = Process(target=Sensor2)
	Process_3 = Process(target=Sensor3)
	Process_4 = Process(target=Sensor4)
	Process_5 = Process(target=Sensor5)
	Process_6 = Process(target=Sensor6)
	Process_7 = Process(target=Sensor7)
	Process_8 = Process(target=Sensor8)
	Process_0.start()
	Process_1.start()
	Process_2.start()
	Process_3.start()
	Process_4.start()
	Process_5.start()
	Process_6.start()
	Process_7.start()
	Process_8.start()

	running = True
	#Main read loop
	counter = 0
	while running:
		try:
			begin.value = 1
			counter += 1    
			while complete[0] == 0 or complete[1] == 0 or complete[2] == 0 or complete[3] == 0 or complete[4] == 0 or complete[5] == 0 or complete[6] == 0 or complete[7] == 0 or complete[8] == 0:
				#Wait for all reads to complete
				pass
            
			begin.value = 0
			complete[0], complete[1], complete[2], complete[3], complete[4], complete[5], complete[6], complete[7], complete[8] = 0, 0, 0, 0, 0, 0, 0, 0, 0
			publish.single(Pod,'iter= '+str(counter)+' '+str(distances[:])+'-----'+str(time.time()),hostname='192.168.1.110')
			print('iter= '+str(counter)+' '+str(distances[:]))
            
		except KeyboardInterrupt:
			print("Stopping...")
			begin.value = 0
			quit.value = 1
			time.sleep(0.5)
			Process_0.terminate()
			Process_1.terminate()
			Process_2.terminate()
			Process_3.terminate()
			Process_4.terminate()
			Process_5.terminate()
			Process_6.terminate()
			Process_7.terminate()
			Process_8.terminate()
			time.sleep(0.5)
			for i in sensor_enable_GPIO:
				GPIO.output(int(i), GPIO.LOW)
			running = 0
			break

if __name__ == '__main__':
	run()
