from IR6SensorModule import IR6SensorModule
from LeftRightMotorCar import LeftRightMotorCar
import time

class LineFollowerRobot():

    # leftPos, leftNeg, rightPos, rightNeg
    def __init__(self):
        leftMotorPos = 17;
        leftMotorNeg = 4;
        rightMotorPos = 3;
        rightMotorNeg = 2;

        self.car = LeftRightMotorCar(leftMotorPos,leftMotorNeg,rightMotorPos,rightMotorNeg);

        #pins to which IRSensors are attached. - 6 of them
        self.irsensor = IR6SensorModule(18,23,24,25,8,7);

        self.sensorReadings = b'000000';
        self.count = 0;
        self.error = 0;
        self.errorLast = 0;
        self.correction =0;
        self.maxSpeed = 255;
        self.motorLSpeed = 100;
        self.motorRSpeed = 100;
        self.minSpeed = 30; 

        self.f = open('log.txt','w');
    
    def scan(self):
        self.count = 0;
        self.sensorReadings = b'000000';
        self.sensorReadings = self.irsensor.readSensor();
#        for ir in self.sensorReadings:
#            self.count = self.count + ir;
    
    def updateError(self):
        self.errorLast = self.error;

        if(self.sensorReadings == b'000000'):
       #     if(self.errorLast < 0):
       #         self.error = -180;
       #     elif(self.errorLast > 0):
       #         self.error = 180;
            self.error = 1000;#stop condition
        #one sensor on line
        elif(self.sensorReadings == b'100000'): #leftmost sensor on line
            self.error = -150;
        elif(self.sensorReadings == b'010000'): 
            self.error = -90;
        elif(self.sensorReadings == b'001000' or self.sensorReadings == b'000100'):
            self.error = 0;
        elif(self.sensorReadings == b'000010'):
            self.error =  90;
        elif(self.sensorReadings == b'000001'):#rightmost sensor on line 
            self.error = 150;
        #two sensor on line
        elif(self.sensorReadings == b'110000'):
            self.error =  -120;
        elif(self.sensorReadings == b'011000'):
            self.error =  -60;
        elif(self.sensorReadings == b'001100'):
            self.error =  0;
        elif(self.sensorReadings == b'000110'):
            self.error =  60;
        elif(self.sensorReadings == b'000011'):
            self.error =  120;
        elif(self.sensorReadings == b'001001'):
            self.error = 150;
        elif(self.sensorReadings == b'100100'):
            self.error = -150;
        elif(self.sensorReadings == b'101000'):
            self.error = -150;
        elif(self.sensorReadings == b'000101'):
            self.error = 150;
        #three sensor on line
        elif(self.sensorReadings == b'111000' or self.sensorReadings == b'110100'):
            self.error = -150;
        elif(self.sensorReadings == b'000111' or self.sensorReadings == b'001011'):
            self.error = 150;
        elif(self.sensorReadings == b'011100'):
            self.error = -60;
        elif(self.sensorReadings == b'001110'):
            self.error = 60;
        elif(self.sensorReadings == b'001101'):
            self.error = 90;
        #four sensors on line
        elif(self.sensorReadings == b'111100'):
            self.error = -150;
        elif(self.sensorReadings == b'011110'):
            self.error = 0;
        elif(self.sensorReadings == b'001111'):
            self.error = 150;
        #five sensors on line
        elif(self.sensorReadings == b'111110'):
            self.error = -150;
        elif(self.sensorReadings == b'011111'):
            self.error = 150;
        #all sex on line
        elif(self.sensorReadings == b'111111'):
            print "End";
        else:
            self.error = self.errorLast;

    def updateCorrection(self):
        if (self.error >= 0 and self.error < 30):
            self.correction = 0;

        elif(self.error >=30 and self.error < 60):
            self.correction = 0.2;
        elif(self.error >=60 and self.error < 90):
            self.correction = 0.25;

        elif(self.error >=90 and self.error < 120):
            self.correction = 0.3;
                
        elif(self.error >=120 and self.error < 150):
            self.correction = 0.35;

        elif (self.error >=150 and self.error < 180):
            self.correction = 0.45;

        elif (self.error >=180 < self.error < 1000):
	    self.correction = 0.5;

        elif (self.error >= 1000):
            self.correction = 1000;

        if (self.error <= 0 and self.error > -30):
            self.correction = 0;

        elif (self.error <= -30 and self.error > -60):
            self.correction = -0.2;

   	elif (self.error <= -60 and self.error > -90):
            self.correction = -0.25;

	elif (self.error <= -90 and self.error > -120):
            self.correction = -0.3;

	elif (self.error <= -120 and self.error > -150):
            self.correction = -0.35;

	elif (self.error <= -150 and self.error > -180):
            self.correction = -0.45;

	elif (self.error <= -180):
	    self.correction = -0.5;


        if(abs(self.correction) < 0.3):
            self.maxSpeed = 0.3;
        else:
            self.maxSpeed = 0.5;

        self.maxSpeed = 0.5;

	if (self.correction > 0 and self.correction < 1000): 

	    #self.motorRSpeed = self.maxSpeed - self.correction;
	    self.motorRSpeed = -self.correction;
            self.motorLSpeed = self.maxSpeed; 

        elif(self.correction == 0):
            self.motorRSpeed = self.maxSpeed;
            self.motorLSpeed = self.maxSpeed;

	elif (self.correction < 0):
    	    self.motorRSpeed = self.maxSpeed;
	    self.motorLSpeed = self.correction;

        elif (self.correction >= 1000): #stop condition
            self.motorRSpeed = 0;
            self.motorLSpeed = 0;
                             

    def drive(self):
#	self.motorRSpeed = self.motorRSpeed / 255.0;
#	self.motorLSpeed = self.motorLSpeed / 255.0;
        

        maxSpeed = self.maxSpeed;

	if(self.motorRSpeed < -maxSpeed):
		self.motorRSpeed = -maxSpeed;
	elif(self.motorRSpeed > maxSpeed):
		self.motorRSpeed = maxSpeed;

	if(self.motorLSpeed < -maxSpeed):
		self.motorLSpeed = -maxSpeed;
	elif(self.motorLSpeed > maxSpeed):
		self.motorLSpeed = maxSpeed;

        stri = self.sensorReadings + ', ' + str(self.error) + ', ' + str(self.correction) +  ', ' + str(self.motorRSpeed) +  ', ' + str(self.motorLSpeed);

        self.f.write(stri);
        self.f.write('\n');

        if(self.motorRSpeed > 0):
            self.car.motorRForward(self.motorRSpeed);
        elif(self.motorRSpeed < 0):
            self.car.motorRBackward(-self.motorRSpeed);
        else:
            self.car.motorRStop();
        
        if(self.motorLSpeed > 0):
            self.car.motorLForward(self.motorLSpeed);
        elif(self.motorLSpeed < 0):
            self.car.motorLBackward(-self.motorLSpeed);
        else:
            self.car.motorLStop();

    def run(self):
        while(True):
            self.scan();
            self.updateError();
            self.updateCorrection();
            self.drive();

    def __del__(self):
        self.car.stop();
        self.f.close();

robot = LineFollowerRobot();
robot.run();


