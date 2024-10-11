''' --------------------------------------------------
PID line follower.py
Made with Pybricks, for WRO Junior 2024

chaBots Neri 🇲🇽 chabots.com.mx  dojorobot.com
-Alfonso De Anda
---------------------------------------------------'''

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.tools import StopWatch, multitask, run_task, wait

hub = PrimeHub()

lineSensor = ColorSensor(Port.A)
rightMotor = Motor(Port.B, Direction.CLOCKWISE)
leftMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)

#Initialize variables
sensorBlack = 19 #Value of the sensor reflection at the black line.
sensorWhite = 100 #Value of the sensor reflection at the black line.
threshold = 0
pFix = 0
error = 0
lastError = 0
integral = 0
iFix = 0
derivative = 0
dFix = 0
correction = 0

#Set up code
async def setup():
    global threshold
    await wait(1)
    print('-[:]')
    print('UPLOADED |', 'BATTERY VOLTAGE: ', prime_hub.battery.voltage()) #Prints battery life
    if prime_hub.battery.voltage() <= 7600:
        print('LOW BATTERY')
        raise SystemExit
    threshold = (sensorBlack + sensorWhite) / 2 #Gets average between black value and white value
    threshold = threshold + 3
    while not Button.RIGHT in prime_hub.buttons.pressed(): #Starts the program until the right button in the Spike hub is pressed
        await wait(1)

#PID Function for line following
''' Function arguments:
    kP: Constant multiplier for proportional value
    kI: Constant multiplier for integral value
    kD: Constant multiplier for derivative value
    speed: declares power percentage of the motors (0-100)
    leftRight: defines if the line will be followed from the left or the right. (0=Left, 1=Right) '''
async def lineFollow(kP, kI, kD, speed, leftRight):
    global error, pFix, integral, iFix, derivative, lastError, dFix, correction
    await wait(1)
    while True:
        await wait(1)
        error = await lineSensor.reflection() - threshold
        pFix = error * kP
        integral = integral + error
        iFix = integral * kI
        derivative = error - lastError
        lastError = error
        dFix = derivative * kD
        correction = (pFix + iFix) + dFix
        if leftRight == 1:
            leftMotor.dc(speed + correction)
            rightMotor.dc(speed - correction)
        elif leftRight == 0:
            leftMotor.dc(speed - correction)
            rightMotor.dc(speed + correction)

#Example code for using the PID function
async def main():
    await setup()
    await lineFollow(0.3, 0, 0.1, 50, 0)