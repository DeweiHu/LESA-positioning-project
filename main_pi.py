# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 16:16:48 2019

@author: Dewei
"""

# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import numpy as np
import matplotlib.pyplot as plt

# since the 3*3 matrix created by each sensor may be hard to visualize in the image, the dilate function is used to enlarge each pixel to a size of kernel, here the ker=[a,b]
def dilate(A,ker):
    
    Dilate = np.zeros([ker[0]*A.shape[0],ker[1]*A.shape[1]])

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            Dilate[ker[0]*i:ker[0]*(i+1),ker[1]*j:ker[1]*(j+1)] = A[i,j]
    return Dilate

# the rearange function shows how the pixels correspond to the number of sensor connected to specific GPIO 
def rearange(A):
    M = np.zeros([3,3])
    M[0,0] = A[7]
    M[0,1] = A[8]
    M[0,2] = A[6]
    M[1,0] = A[2]
    M[1,1] = A[5]
    M[1,2] = A[4]
    M[2,0] = A[1]
    M[2,1] = A[0]
    M[2,2] = A[3]
    return M

# rotation of a matrix(this is useful because the installation orientation of pod in LESA are not the same for each pod)
def rotate(A):
    B = np.fliplr(np.transpose(A))
    return B

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    start = time.time()
    for i in range(15):
        client.subscribe('worker_{}'.format(i+1))
    end = time.time()
    print('time comsumed:{}'.format(end-start))

data = ''
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global data
    data = msg.topic+str(msg.payload)
#    print(msg.topic+' ------ '+str(msg.payload)+'\n'+' ------ '+'receive time: '+str(datetime.datetime.now())+'\n')
#    file.write(msg.topic+str(msg.payload)+'\n')
    
# Set up the name for the main pi
Pod = 'main_Pi'

# Publish the time to activate
wt = 5
idx = time.time()
switch = idx + wt
publish.single(Pod, switch, hostname='192.168.1.3')

# setup the canvas to draw on
fig = plt.figure()
ax = fig.add_subplot(111)
# getting in full screen
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

while int(switch-idx) > 0:
    print('Activate in '+str(int(switch-idx))+' '+'seconds...')
    time.sleep(1)
    idx = time.time()
print('Start receiving...')

#file = open('nightwalk_2.txt','w')

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message 
client.connect('192.168.1.3', 1883, 60)

#%% The main loop
client.loop_start()
#Image = np.zeros([12,36])
Image = np.random.random((12,36))

im = ax.imshow(Image)
#im = ax.imshow(np.random.random((12,36)))
plt.show(block=False)
Z = 1

while True:
    if len(data)>0:
        # extract the worker number
        idx1 = data.find('_')
        idx2 = data.find('b')
        num = int(data[idx1+1:idx2])
        # extract the reading value
        pos1 = data.find('[')
        pos2 = data.find(']')
        read = data[pos1+1:pos2]
        # transform the string to a vector 
        vec = np.zeros([9])
        for i in range(8):
            comma = read.find(',')
            vec[i] = float(read[:comma])
            read = read[comma+2:]
        vec[8] = float(read)
        # transform the vector to a pre-defined matrix
        pod = rearange(vec)
        if num == 1:
            Image[6:9,14:17] = rotate(pod/3500)
        if num == 2:
            Image[6:9,9:12] = pod/3500
        if num == 3:
            Image[3:6,2:5] = pod/3500
        if num == 4:
            Image[6:9,5:8] = pod/3500
        if num == 5:
            Image[9:12,0:3] = pod/3500
        if num == 6:
            Image[9:12,12:15] = pod/3500
        if num == 7:
            Image[9:12,21:24] = pod/3500
        if num == 8:
            Image[0:3,27:30] = pod/3500
        if num == 10:
            Image[0:3,30:33] = rotate(rotate(pod/3500))
        if num == 11:
            Image[7:10,33:36] = rotate(rotate(pod/3500))
        if num == 12:
            Image[6:9,18:21] = rotate(pod/3500)
        if num == 13:
            Image[6:9,23:26] = rotate(pod/3500)
        if num == 14:
            Image[6:9,27:30] = rotate(rotate(rotate(pod/3500)))
    im.set_array(Image)
#    im.set_array(np.random.random((12,36)))

    print(Image)
    fig.canvas.draw()
    if Z == 1:
      Image = np.zeros([12,36])
      Z=0
else:
    client.loop_stop()


        
