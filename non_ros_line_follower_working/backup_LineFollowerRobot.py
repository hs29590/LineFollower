from IR6SensorModule import IR6SensorModule
from LeftRightMotorCar import LeftRightMotorCar
import time
import threading

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
        
        self.prevSensorReadings = [1,1,1,1,1,1];
        self.sensorReadings = [0,0,0,0,0,0];
        self.startSensorReadingThread();

    def _sensorReadingThread(self):
        self.sensorReadings = self.irsensor.readSensor();

    def startSensorReadingThread(self):
        self.thread = threading.thread(target=self._sensorReadingThread).start();

    def stopSensorReadingThread(self):
        self.thread.join();

    def hardRightTurn(self):
        self.car.forward();
        time.sleep(0.2);
        self.car.stop();
        while(True):
            self.car.right(); #take right with speed 0.2 times the max
            time.sleep(0.1);
            self.car.stop();
            sensorReadings = self.irsensor.readSensor();
            if(self.prevSensorReadings != sensorReadings):
                print "inside Hard right turn",
                print sensorReadings;
                self.prevSensorReadings = sensorReadings;
            if(sensorReadings[2] == 1 or sensorReadings[3] == 1):
                break;
        self.car.stop();
    
    def hardLeftTurn(self):
        self.car.forward();
        time.sleep(0.2);
        self.car.stop();
        while(True):
            self.car.left(); #take right with speed 0.2 times the max
            sensorReadings = self.irsensor.readSensor();
            if(self.prevSensorReadings != sensorReadings):
                print "inside Hard left turn",
                print sensorReadings;
                self.prevSensorReadings = sensorReadings;
            if(sensorReadings[2] == 1 or sensorReadings[3] == 1):
                break;
        self.car.stop();

    def run(self):
        while(True):
            sensorReadings = self.irsensor.readSensor();
            if(self.prevSensorReadings != sensorReadings):
                print sensorReadings
                self.prevSensorReadings = sensorReadings;
            if(sensorReadings == [0,0,0,0,0,0]):
                self.car.stop();
            #    print "stopping because, ", sensorReadings
            elif(sensorReadings == [0,0,1,1,1,1] or 
                    sensorReadings == [0, 0, 1, 0, 1, 1] or 
                    sensorReadings == [0, 0, 1, 0, 0, 1] #or 
             #       sensorReadings == [0, 0, 1, 0, 1, 0] #or
#                    sensorReadings == [0, 0, 1, 1, 0, 1] or 
#                    sensorReadings == [0, 0, 1, 1, 1, 0] or
                    ):
                print("\nHard Right Turn because\n");
                print sensorReadings
                self.hardRightTurn();
            elif(sensorReadings == [1,1,1,1,0,0] or 
                    sensorReadings == [1, 1, 1, 0, 0, 0] or
                    sensorReadings == [1, 0, 1, 0, 0, 0] #or 
          #          sensorReadings == [0, 1, 1, 0, 0, 0]# or
#                    sensorReadings == [1, 0, 1, 1, 0, 0] or 
#                    sensorReadings == [0, 1, 1, 1, 0, 0] or
                    ):
                print("\nHard Left Turn becase \n");
                print sensorReadings
                self.hardLeftTurn();
            elif(sensorReadings[2] == 1 or sensorReadings[3] == 1):
                self.car.forward();
            elif(sensorReadings[0] == 1 or sensorReadings[1] == 1):
                self.car.left();
            elif(sensorReadings[4] == 1 or sensorReadings[5] == 1):
                self.car.right();

    def __del__(self):
        self.stopSensorReadingThread();

robot = LineFollowerRobot();
robot.run();


