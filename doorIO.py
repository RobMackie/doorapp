## For running on Raspberry Pi
try:
   import RPi.GPIO as GPIO
   TEST_ONLY = False
except:
   TEST_ONLY = True

def unlockIO(pin):
   if TEST_ONLY:
      print "Unlock test"
   elif GPIO.input(pin) != GPIO.HIGH:
      GPIO.output(pin, GPIO.HIGH)
      time.sleep(5)
      GPIO.output(pin, not GPIO.input(self.pin))


class DoorGPIO(object):
    def __init__(self):
        self.pin = 11;
        if not TEST_ONLY:
           print "GPIO Version: " + GPIO.VERSION
           GPIO.setmode(GPIO.BOARD)
           GPIO.setup(self.pin, GPIO.OUT)
        else:
           print "---- NO GPIO WORKING!!! ---- "

    def unlock(self, user):
        logStr = time.asctime() + ": " + user + " unlocking door" + "\n"
        print "--- " + logStr
        logFile.write(logStr)
        t = threading.Thread(target=unlockIO,args=(self.pin,))
        t.start()
