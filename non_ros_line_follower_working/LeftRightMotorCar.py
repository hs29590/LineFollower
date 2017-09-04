import RPi.GPIO as GPIO
import time
import sys
from gpiozero import Motor

'''Four Motor car with right and left motors combined'''
class LeftRightMotorCar():

    def __init__(self, lP, lN, rP, rN):
        
        # self, left Pos, left Neg, right Pos, right Neg
        
        self.motorLeft = Motor(lP, lN);
        self.motorRight = Motor(rP, rN);
        self.motorLeft.stop();
        self.motorRight.stop();

    def forward(self,speed = 0.3):
        self.motorLeft.forward(speed);
        self.motorRight.forward(speed);

    def backward(self,speed = 0.3):
        self.motorLeft.backward(speed);
        self.motorRight.backward(speed);
   
    def motorLForward(self,speed):
        self.motorLeft.forward(speed);

    def motorLBackward(self,speed):
        self.motorLeft.backward(speed);

    def motorRForward(self,speed):
        self.motorRight.forward(speed);

    def motorRBackward(self,speed):
        self.motorRight.backward(speed);

    def motorRStop(self):
        self.motorRight.stop();

    def motorLStop(self):
        self.motorLeft.stop();

    def right(self,speed = 0.3):
        #left fwd
        self.motorLeft.forward(speed);
        self.motorRight.backward(speed);
        
    def left(self,speed = 0.3):
        #left rev
        self.motorLeft.backward(speed);
        self.motorRight.forward(speed);
    
    def stop(self):
        self.motorLeft.stop();
        self.motorRight.stop();

    def trialRun(self):
        self.forward();
        time.sleep(2);
        self.right();
        time.sleep(2);
        self.reverse();
        time.sleep(2);
        self.left();
        time.sleep(2);
        self.stop();

    def __del__(self):
        self.stop();
