import RPi.GPIO as GPIO

class IR6SensorModule():
    
    def __init__(self,pin1, pin2, pin3, pin4, pin5, pin6):
        
        self.irsensors = [pin1, pin2, pin3, pin4, pin5, pin6];
        self.sensorReadings = [0,0,0,0,0,0];
        
        GPIO.setmode(GPIO.BCM)
        for ir in self.irsensors:
            GPIO.setup(ir, GPIO.IN);

    def readSensor(self):
        for i in range(len(self.irsensors)):
            self.sensorReadings[i] = GPIO.input(self.irsensors[i]);

        return self.sensorReadings;

    def __del__(self):
        GPIO.cleanup();


