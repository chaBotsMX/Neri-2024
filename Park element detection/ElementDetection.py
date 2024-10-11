''' --------------------------------------------------
Element detection.py
Made with Pybricks, for WRO Junior 2024

chaBots Neri 🇲🇽 chabots.com.mx  dojorobot.com
-Alfonso De Anda
---------------------------------------------------'''

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

hub = PrimeHub()

rightMotor = Motor(Port.B, Direction.CLOCKWISE)
leftMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
elementSensor = ColorSensor(Port.D)
driveBase = DriveBase(leftMotor, rightMotor, 62.4, 220)

#Initialize variables
elementX = 0

#Set up code
async def setup():
    await wait(1)
    print('-[:]')
    print('UPLOADED |', 'BATTERY VOLTAGE: ', prime_hub.battery.voltage()) #Prints battery life
    if prime_hub.battery.voltage() <= 7600:
        print('LOW BATTERY')
        raise SystemExit
    while not Button.RIGHT in prime_hub.buttons.pressed(): #Starts the program until the right button in the Spike hub is pressed
        await wait(1)

#checking park elements. Goes straight until it detects something, defines what type of element it is. Stops when the combination is detected
async def checkElements():
    await wait(1)
    driveBase.settings(straight_speed=150)
    while True:
        await wait(1)
        if await elementSensor.reflection() > 3:
            await driveBase.straight(10, Stop.NONE)
            await isFlowerOrDuck()
            await driveBase.straight(10, Stop.NONE)
            if elementX == 6:
                print('COMBINATION DETECTED')
                break
            else:
                if elementX > 6:
                    elementX = 4
                elif elementX == 3:
                    elementX = 2
                else:
                    pass
        else:
            driveBase.drive(250, 0)
    rightMotor.hold()
    leftMotor.hold()

#defines the type of park element (tree or duck)
#should calibrate reflected light from the sensor to elements
async def isFlowerOrDuck(minTreeValue, maxTreeValue, minDuckValue, maxDuckValue):
    global elementX
    await wait(1)
    if await elementSensor.reflection() > minTreeValue and await elementSensor.reflection() <= maxTreeValue:
        elementX = elementX + 1
        print('TREE', ' ', await elementSensor.reflection(), ' ', elementX)
        await prime_hub.speaker.beep(200, 100)
    elif await elementSensor.reflection() >= minDuckValue and await elementSensor.reflection() < maxDuckValue:
        elementX = elementX + 4
        print('DUCK', ' ', await elementSensor.reflection(), ' ', elementX)
        await prime_hub.speaker.beep(550, 100)
    else:
        pass


#Example code for using the
async def main():
    await setup()
    await checkElements(3, 11, 12, 30)
    