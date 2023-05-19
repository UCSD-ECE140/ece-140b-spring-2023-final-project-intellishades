import RPi.GPIO as GPIO
import time
onPin = 40 # define ledPin 
dimPin =38
def setup():
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(onPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(onPin, GPIO.LOW) # make ledPin output LOW level

    GPIO.setup(dimPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(dimPin, GPIO.LOW) # make ledPin output LOW level
 
    print (f'using pins: {onPin}, {dimPin}')

def on(): 
        GPIO.output(onPin, GPIO.HIGH) # makes shades go transparent
        GPIO.output(dimPin, GPIO.LOW)
        print ('shades turned on >>>') # print information on terminal
def off():  
        GPIO.output(dimPin, GPIO.HIGH)
        GPIO.output(onPin, GPIO.HIGH) # makes shades go opaque
        print ('shades turned off <<<')
def dim(): 
        GPIO.output(onPin, GPIO.LOW)
        GPIO.output(dimPin, GPIO.HIGH) # makes shades go into dim state
        print ('shades dimmed vvv')

def loop():
    while True: 
        on()
        time.sleep(5)
        dim()
        time.sleep(5) # Wait for 5 seconds
        off()
        time.sleep(5) # Wait for 5 seconds
        

def destroy():
    GPIO.cleanup() # Release all GPIO 

if __name__ == '__main__': # Program entrance 
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
