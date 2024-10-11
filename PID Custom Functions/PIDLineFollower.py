''' --------------------------------------------------
PID line follower.py
Made with Pybricks, for WRO Junior 2024

chaBots Neri 🇲🇽    https://chabots.com.mx/    https://www.dojorobot.com/
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
lineFollowError = 0
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
    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)
    while not Button.RIGHT in prime_hub.buttons.pressed(): #Starts the program until the right button in the Spike hub is pressed
        await wait(1)

#PID Function for line following
''' Function arguments:
    kP: Constant multiplier for proportional value
    kI: Constant multiplier for integral value
    kD: Constant multiplier for derivative value
    SPEED: declares power percentage of the motors (0-100)
    LR: defines if the line will be followed from the left or the right. (0=Left, 1=Right) '''
async def PIDLineFollow(kP, kI, kD, SPEED, LR):
    global lineFollowError, pFix, integral, iFix, derivative, lastError, dFix, correction
    await wait(1)
    while True:
        await wait(1)
        lineFollowError = await lineSensor.reflection() - threshold
        pFix = lineFollowError * kP
        integral = integral + lineFollowError
        iFix = integral * kI
        derivative = lineFollowError - lastError
        lastError = lineFollowError
        dFix = derivative * kD
        correction = (pFix + iFix) + dFix
        if LR == 1:
            leftMotor.dc(SPEED + correction)
            rightMotor.dc(SPEED - correction)
        elif LR == 0:
            leftMotor.dc(SPEED - correction)
            rightMotor.dc(SPEED + correction)

#Example code for using the PID function
async def main():
    await setup()
    await PIDLineFollow(0.3, 0, 0.1, 90, 1)
