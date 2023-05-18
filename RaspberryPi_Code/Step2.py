import RPi.GPIO as GPIO
import time
ledPin = 40 # define ledPin
def setup():
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW) # make ledPin output LOW level
    print ('using pin%d'%ledPin)

def loop():
    while True:
        GPIO.output(ledPin, GPIO.HIGH) # make ledPin output HIGH level to turn on led
        print ('shades turned on >>>') # print information on terminal
        time.sleep(5) # Wait for 1 second
        GPIO.output(ledPin, GPIO.LOW) # make ledPin output LOW level to turn off led
        print ('shades turned off <<<')
        time.sleep(5) # Wait for 1 second
def destroy():
    GPIO.cleanup() # Release all GPIO
if __name__ == '__main__': # Program entrance 
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
