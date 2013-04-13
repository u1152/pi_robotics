from server_settings import robot_api

__author__ = 'Aleksandar'

import wiringpi as wp
from math import fabs
from time import sleep

class Rover5(object):
    """Rover5 API"""

    def __init__(self):
        self.pins = robot_api
        self.turretAngle = 0
        wp.wiringPiSetup()
        wp.softPwmCreate(self.pins['pwm_tl_pin'], 0, self.pins['pwm_range'])
        wp.softPwmCreate(self.pins['pwm_tr_pin'], 0, self.pins['pwm_range'])
        wp.softPwmCreate(self.pins['pwm_bl_pin'], 0, self.pins['pwm_range'])
        wp.softPwmCreate(self.pins['pwm_br_pin'], 0, self.pins['pwm_range'])
        wp.pinMode(robot_api['dir_tl_pin'], wp.OUTPUT)
        wp.pinMode(robot_api['dir_tr_pin'], wp.OUTPUT)
        wp.pinMode(robot_api['dir_bl_pin'], wp.OUTPUT)
        wp.pinMode(robot_api['dir_br_pin'], wp.OUTPUT)
        wp.pinMode(robot_api['turret_dir'], wp.OUTPUT)
        wp.pinMode(robot_api['turret_steps'], wp.OUTPUT)

    def setSpeed(self, pwmLeft, pwmRight):
        print pwmLeft, " ", pwmRight
        wp.softPwmWrite(self.pins['pwm_tl_pin'], pwmLeft)
        wp.softPwmWrite(self.pins['pwm_bl_pin'], pwmLeft)
        wp.softPwmWrite(self.pins['pwm_tr_pin'], pwmRight)
        wp.softPwmWrite(self.pins['pwm_br_pin'], pwmRight)

    def setDirection(self, dirLeft, dirRight):
        print dirLeft, " ", dirRight
        wp.digitalWrite(self.pins['dir_tl_pin'], wp.HIGH if dirLeft else wp.LOW)
        wp.digitalWrite(self.pins['dir_bl_pin'], wp.HIGH if dirLeft else wp.LOW)
        wp.digitalWrite(self.pins['dir_tr_pin'], wp.HIGH if dirRight else wp.LOW)
        wp.digitalWrite(self.pins['dir_br_pin'], wp.HIGH if dirRight else wp.LOW)

    def stop(self):
        self.setSpeed(0, 0)
        self.setDirection(0, 0)

    def getRightEncoder(self):
        pass

    def getLeftEncoder(self):
        pass

    def getSonarSensor(self):
        pass

    def getOpticalSensor(self):
        pass

    def turnTurret(self, newAngle):
        print self.turretAngle, " " , newAngle

	oldAngle = self.turretAngle
        self.turretAngle = newAngle

        steps = 0
        direction = 0

        if newAngle < 0:
            newAngle = newAngle + 200

        if oldAngle < 0:
            oldAngle = oldAngle + 200

        newAngle = newAngle - oldAngle
                   
        steps = fabs(newAngle) if fabs(newAngle)<=100 else 200-fabs(newAngle)

        if newAngle >= 0:
            direction = wp.LOW if fabs(newAngle) <= 100 else wp.HIGH
        else:           
            direction = wp.HIGH if fabs(newAngle) <= 100 else wp.LOW

	self.__turnProcess(direction, int(steps))

    def __turnProcess(self,direction, steps):
        print 'steps = ', steps, 'dir = ', direction
        sleep_time = 0.005
        wp.digitalWrite(self.pins['turret_dir'], direction)
        
        for i in range(steps):
            sleep(sleep_time)
            wp.digitalWrite(self.pins['turret_steps'], wp.HIGH)
            sleep(sleep_time)
            wp.digitalWrite(self.pins['turret_steps'], wp.LOW)

    
        
