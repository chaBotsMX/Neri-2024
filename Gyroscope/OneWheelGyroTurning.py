''' --------------------------------------------------
One wheel gyro turning.py
Made with Pybricks, for WRO Junior 2024

chaBots Neri 🇲🇽 chabots.com.mx dojorobot.com
-Alfonso De Anda
---------------------------------------------------'''

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch, multitask, run_task, wait

hub = PrimeHub()

#Setup sensors and motors. You may have to adjust this
rightMotor = Motor(Port.B, Direction.CLOCKWISE)
leftMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)

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

#Proportional Acceleration decelaration function for accurate turning using the gyroscope by a given angle
async def oneWheelTurning(angle):
    await wait(1)
    if angle >= prime_hub.imu.heading():
        while prime_hub.imu.heading() <= angle:
            await wait(1)
            leftMotor.run((angle - prime_hub.imu.heading()) * 9 + 60)
    else:
        while prime_hub.imu.heading() >= angle:
            await wait(1)
            rightMotor.run((prime_hub.imu.heading() - angle) * 9 + 60)
        while prime_hub.imu.heading() <= angle:
            await wait(1)
            rightMotor.run((angle + prime_hub.imu.heading()) * 9 + 60)
    rightMotor.hold()
    leftMotor.hold()

#Example code for using the turning function
async def main():
    await setup()
    while True:
        await oneWheelTurning(0)

run_task(main())