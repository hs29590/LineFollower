import RPi.GPIO as GPIO
import time
import sys
from gpiozero import Motor

GPIO.setmode(GPIO.BCM)

### Setup Motor Control ###
leftPos = 3
leftNeg = 2
rightPos = 17
rightNeg = 4

motorLeft = Motor(leftPos, leftNeg);
motorRight = Motor(rightPos, rightNeg);
motorLeft.stop();
motorRight.stop();


sensorForHardRight = [1, 1, 1, 0, 0, 0];
sensorForCurveRight = [0, 1, 1, 0, 0, 0];
sensorForRight = [1, 0, 0, 0, 0, 0];
sensorForRight1 = [0, 1, 0, 0, 0, 0];
sensorForHardLeft = [0, 0, 1, 0, 1, 1];
sensorForCurveLeft = [0, 0, 1, 0, 1, 0];
sensorForLeft = [0, 0, 0, 0, 1, 0];
sensorForLeft1 = [0, 0, 0, 0, 0, 1];
sensorForStraight1 = [0, 0, 1, 1, 0, 0];
sensorForStraight2 = [0, 0, 0, 1, 0, 0];
sensorForStraight3 = [0, 0, 1, 0, 0, 0];
sensorForStop = [0, 0, 0, 0, 0, 0];
sensorForUTurn = [1, 1, 1, 1, 1, 1];


### Setup Line Follower Module

irsensors = [18, 23, 24, 25, 8, 7];
sensorReadings = [0, 0, 0, 0, 0, 0];

for ir in irsensors:
    GPIO.setup(ir, GPIO.IN);

def forward(speed = 0.3):
    motorLeft.forward(speed);
    motorRight.forward(speed);
    
def reverse(speed = 0.3):
    motorLeft.backward(speed);
    motorRight.backward(speed);
    
def right():
    #left fwd
    motorLeft.forward(0.3);
    motorRight.backward(0.3);
        
def left():
    #left rev
    motorLeft.backward(0.3);
    motorRight.forward(0.3);
    
def stop():
    motorLeft.stop();
    motorRight.stop();

def trial():
    forward();
    time.sleep(2);
    right();
    time.sleep(2);
    reverse();
    time.sleep(2);
    left();
    time.sleep(2);
    stop();

def rightUntilLine():
    while(sensorReadings == sensorForStraight1 or sensorReadings == sensorForStraight2 or sensorReadings == sensorForStraight3):
        right();
        for i in range(len(irsensors)):
            sensorReadings[i] = GPIO.input(irsensors[i]);
    stop();

def leftUntilLine():
    while(sensorReadings == sensorForStraight1 or sensorReadings == sensorForStraight2 or sensorReadings == sensorForStraight3):
        left();
        for i in range(len(irsensors)):
            sensorReadings[i] = GPIO.input(irsensors[i]);
    stop();

def loop():
    for i in range(len(irsensors)):
        sensorReadings[i] = GPIO.input(irsensors[i]);
    
#    if(sensorReadings == [0,0,0,0,0,0]):
#        stop();
#    elif(sensorReadings[2] == 1 or sensorReadings[3] == 1):
#       forward();
#    elif(sensorReadings[0] == 1 or sensorReadings[1] == 1):
#        right();
#    elif(sensorReadings[4] == 1 or sensorReadings[5] == 1):
#        left();
    
    if(sensorReadings == sensorForHardRight):
        print("Hard Right");
        stop();
        time.sleep(1);
        forward();
        time.sleep(0.3);
        right();
        time.sleep(0.7);
        stop();
    elif(sensorReadings == sensorForCurveRight):
#        print("Curve Right");
        right();
    elif(sensorReadings == sensorForRight or sensorReadings == sensorForRight1):
#        print("Right");
        right();
    elif(sensorReadings == sensorForHardLeft):
        print("Hard Left");
        stop();
        time.sleep(1);
        forward();
        time.sleep(0.3);
        left();
        time.sleep(0.7);
    elif(sensorReadings == sensorForCurveLeft):
#        print("Curve Left");
        left();
    elif(sensorReadings == sensorForLeft or sensorReadings == sensorForLeft1):
#        print("Left");
        left();
    elif(sensorReadings == sensorForStraight1 or sensorReadings == sensorForStraight2 or sensorReadings == sensorForStraight3):
        forward();
    elif(sensorReadings == sensorForStop):
        stop();
#        time.sleep(2);
#        right();
#        time.sleep(0.4);
#        stop();
#        time.sleep(2);
    elif(sensorReadings == sensorForUTurn):
        right();

while True:
#    right();
#    time.sleep(1);
#    stop();
#    time.sleep(1);
    loop()

GPIO.cleanup();


