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
        self.maxSpeed = 0.5; # 1
        self.leftMotorSpeed = 0.3;
        self.rightMotorSpeed = 0.3;
        self.minSpeed = 0.1; 
    
    def scan(self):
        self.count = 0;
        self.sensorReadings = b'000000';
        self.sensorReadings = self.irsensor.readSensor();
#        for ir in self.sensorReadings:
#            self.count = self.count + ir;
    
    def updateError(self):
        self.errorLast = self.error;

        if(self.sensorReadings == b'000000'):
            if(self.errorLast < 0):
                self.error = -180;
            elif(self.errorLast > 0):
                self.error = 180;
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
        #three sensor on line
        elif(self.sensorReadings == b'111000' or self.sensorReadings == b'110100'):
            self.error = -150;
        elif(self.sensorReadings == b'000111' or self.sensorReadings == b'001011'):
            self.error = 150;
        elif(self.sensorReadings == b'011100'):
            self.error = -60;
        elif(self.sensorReadings == b'001110'):
            self.error = 60;
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
    
        
    def drive(self):

    def run(self):
        while(True):
            self.scan();
            self.updateError();
            self.updateCorrection();
            self.drive();
#
#            sensorReadings = self.irsensor.readSensor();
#            if(self.prevSensorReadings != sensorReadings):
#                print sensorReadings
#                self.prevSensorReadings = sensorReadings;
#            if(sensorReadings == [0,0,0,0,0,0]):
#                self.car.stop();
#            #    print "stopping because, ", sensorReadings
#            elif(sensorReadings == [0,0,1,1,1,1] or 
#                    sensorReadings == [0, 0, 1, 0, 1, 1] or 
#                    sensorReadings == [0, 0, 1, 0, 0, 1] #or 
#             #       sensorReadings == [0, 0, 1, 0, 1, 0] #or
##                    sensorReadings == [0, 0, 1, 1, 0, 1] or 
##                    sensorReadings == [0, 0, 1, 1, 1, 0] or
#                    ):
#                print("\nHard Right Turn because\n");
#                print sensorReadings
#                self.hardRightTurn();
#            elif(sensorReadings == [1,1,1,1,0,0] or 
#                    sensorReadings == [1, 1, 1, 0, 0, 0] or
#                    sensorReadings == [1, 0, 1, 0, 0, 0] #or 
#          #          sensorReadings == [0, 1, 1, 0, 0, 0]# or
##                    sensorReadings == [1, 0, 1, 1, 0, 0] or 
##                    sensorReadings == [0, 1, 1, 1, 0, 0] or
#                    ):
#                print("\nHard Left Turn becase \n");
#                print sensorReadings
#                self.hardLeftTurn();
#            elif(sensorReadings[2] == 1 or sensorReadings[3] == 1):
#                self.car.forward();
#            elif(sensorReadings[0] == 1 or sensorReadings[1] == 1):
#                self.car.left();
#            elif(sensorReadings[4] == 1 or sensorReadings[5] == 1):
#                self.car.right();

    def __del__(self):
        self.stopSensorReadingThread();

robot = LineFollowerRobot();
robot.run();


