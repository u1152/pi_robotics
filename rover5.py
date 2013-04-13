__author__ = 'Aleksandar'

from math import fabs
from time import sleep

#import wiringpi as wp
from pi_robotics.robot import base

class Robot(base.Robot):
    """Rover5 API"""

    def __init__(self, debug):
        base.Robot.__init__(self, debug)

        self.pins = {
            'pwm_tl_pin' : 7,
            'pwm_tr_pin' : 2,
            'pwm_bl_pin' : 0,
            'pwm_br_pin' : 3,
            
            'dir_tl_pin' : 1,
            'dir_tr_pin' : 4,
            'dir_bl_pin' : 5,
            'dir_br_pin' : 6,
            
            'turret_steps' : 8,
            'turret_dir' : 9,
            'pwm_range' : 100,
        }
        self.turretAngle = 0

        if not self.debug:
            wp.wiringPiSetup()
            wp.softPwmCreate(self.pins['pwm_tl_pin'], 0, self.pins['pwm_range'])
            wp.softPwmCreate(self.pins['pwm_tr_pin'], 0, self.pins['pwm_range'])
            wp.softPwmCreate(self.pins['pwm_bl_pin'], 0, self.pins['pwm_range'])
            wp.softPwmCreate(self.pins['pwm_br_pin'], 0, self.pins['pwm_range'])
            wp.pinMode(self.pins['dir_tl_pin'], wp.OUTPUT)
            wp.pinMode(self.pins['dir_tr_pin'], wp.OUTPUT)
            wp.pinMode(self.pins['dir_bl_pin'], wp.OUTPUT)
            wp.pinMode(self.pins['dir_br_pin'], wp.OUTPUT)
            wp.pinMode(self.pins['turret_dir'], wp.OUTPUT)
            wp.pinMode(self.pins['turret_steps'], wp.OUTPUT)

    @property
    def api(self):
        return {
            0x01: ('Move', 'BBBB'),
            0x02: ('Turret', '@I'),
        }

    def Move(self, pwmLeft, pwmRight, dirLeft, dirRight):
        print pwmLeft, " ", pwmRight

        if not self.debug:
            wp.softPwmWrite(self.pins['pwm_tl_pin'], pwmLeft)
            wp.softPwmWrite(self.pins['pwm_bl_pin'], pwmLeft)
            wp.softPwmWrite(self.pins['pwm_tr_pin'], pwmRight)
            wp.softPwmWrite(self.pins['pwm_br_pin'], pwmRight)
            print dirLeft, " ", dirRight
            wp.digitalWrite(self.pins['dir_tl_pin'], wp.HIGH if dirLeft else wp.LOW)
            wp.digitalWrite(self.pins['dir_bl_pin'], wp.HIGH if dirLeft else wp.LOW)
            wp.digitalWrite(self.pins['dir_tr_pin'], wp.HIGH if dirRight else wp.LOW)
            wp.digitalWrite(self.pins['dir_br_pin'], wp.HIGH if dirRight else wp.LOW)

    def stop(self):
        self.Move(0, 0, 0, 0)

    def getRightEncoder(self):
        pass

    def getLeftEncoder(self):
        pass

    def getSonarSensor(self):
        pass

    def getOpticalSensor(self):
        pass

    def Turret(self, newAngle):
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

    
        
