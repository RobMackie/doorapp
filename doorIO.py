import time
import threading

logFile = open("doorapp.log", "a+", 1)   # 1 is line buffering

# For running on Raspberry Pi
try:
    import RPi.GPIO as GPIO
    TEST_ONLY = False
except:
    TEST_ONLY = True


def unlockIO(pin):
    if TEST_ONLY:
        print("Unlock test")
    else:
        # elif GPIO.input(pin) != GPIO.LOW:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(30)
        GPIO.output(pin, GPIO.HIGH)


class DoorGPIO(object):
    def __init__(self):
        self.pin = 11
        if not TEST_ONLY:
            print("GPIO Version: " + GPIO.VERSION)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            print("---- NO GPIO WORKING!!! ---- ")

    def __del__(self):
        if not TEST_ONLY:
            GPIO.cleanup()

    def unlock(self, user):
        logStr = time.asctime() + ": " + user + " unlocking door" + "\n"
        print ("--- " + logStr)
        logFile.write(logStr)
        t = threading.Thread(target=unlockIO, args=(self.pin,))
        t.start()


if __name__ == '__main__':
    door = DoorGPIO()
    door.unlock("command line test")