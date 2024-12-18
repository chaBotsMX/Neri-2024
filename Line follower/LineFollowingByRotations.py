''' --------------------------------------------------
Line following by rotations.py
Made with Pybricks, for WRO Junior 2024

chaBots Neri 🇲🇽 chabots.com.mx  dojorobot.com
-Alfonso De Anda
---------------------------------------------------'''

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.tools import StopWatch, multitask, run_task, wait

prime_hub = PrimeHub()

#Setup sensors and motors. You may have to adjust these values
lineSensor = ColorSensor(Port.F)
rightMotor = Motor(Port.E, Direction.CLOCKWISE)
leftMotor = Motor(Port.D, Direction.COUNTERCLOCKWISE)

#Initialize variables
sensorBlack = 19 #Value of the sensor reflection at the black line.
sensorWhite = 100 #Value of the sensor reflection at the black line.
threshold = 0
error = 0
lastError = 0
integral = 0
iFix = 0
derivative = 0
dFix = 0
correction = 0
rotations = 0

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
async def followLineUntil(rotations, kP, kI, kD, speed, leftRight):
    global error, pFix, integral, iFix, derivative, lastError, dFix, correction
    await wait(1)
    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)
    rotations = 0
    while not rotations >= rotations:
        await wait(1)
        rotations = (leftMotor.angle() + rightMotor.angle()) / 2
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

    rightMotor.brake()
    leftMotor.brake()

#Example code for using the PID function
async def main():
    await setup()
    await followLineUntil(500, 0.01, 0, 0, 50, 0)

run_task(main())