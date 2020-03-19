import curses
import time

doGPIO = False

leftTrack = 7.1
rightTrack = 7.1
headLights = False
tailLights = False

switch1 = False
switch2 = False

if doGPIO:

    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    channelList = [
        23,
        24,
        27,
        17 # , add comma if elements below
        # XX, switch1
        # XX, switch 2
    ]

    GPIO.setup(channelList,GPIO.OUT)

    pwmLeftTrack = GPIO.PWM(23,50)
    pwmRightTrack = GPIO.PWM(24,50)

    pwmLeftTrack.start(leftTrack)
    pwmRightTrack.start(rightTrack)

screen = curses.initscr()

lineIndex = 0

curses.noecho() 
curses.cbreak()
screen.keypad(True)

screen.scrollok(1)
screen.idlok(1)
screen.nodelay(1)
screen.addstr(0, 0, "Waiting... Type F V J N H T or Spacebar. Q to quit.")

termHeight,termWidth = screen.getmaxyx()
#screen.addstr(1, 0, str(height) + ' ' + str(width))
#screen.refresh()

lastKeyTime = time.time()
autoReset = False
# screen.addstr(1, 0, "Start Time " + str(lastKeyTime))

#screen.refresh()

def printToScreen(msg):
    
    global lineIndex, screen, termHeight

    lineIndex = lineIndex + 1

    if lineIndex >= termHeight-1:
        screen.scroll(1)
        lineIndex = termHeight-2

    screen.addstr(lineIndex, 0, '> ' + msg)
    screen.refresh()


def isKeyPressed(key):
    
    global char
    
    if char == ord(key):
        return True

    return False


def decrementValue(value):

    value = round(value - .1,1)

    if value < 6.2:
        value = 6.2

    return value


def incrementValue(value):

    value = round(value + .1,1)
    
    if value > 7.5:
        value = 7.5

    return value

def check30sFromLastInput():

    global lastKeyTime, autoReset

    now = time.time()

    difference = now - lastKeyTime
    # printToScreen("difference: " + str(difference))
    if difference >= 30:
        
        if not autoReset:
            autoReset = True
            return True

    return False

try:

    while True:
        
        char = screen.getch()

        lastKeyCheck = check30sFromLastInput()
         
        if lastKeyCheck:
            char = 32
            printToScreen("30s from last key press, resetting rover")
        else: 
            if char < 0:
                continue
        
        if isKeyPressed('f'):

            lastKeyTime = time.time()
            autoReset = False

            leftTrack = decrementValue(leftTrack)

            printToScreen("F pressed, increase left track speed: " + str(leftTrack))
            
            if doGPIO:
                #pwmLeftTrack.ChangeFrequency(50)
                pwmLeftTrack.ChangeDutyCycle(leftTrack)


        if isKeyPressed('v'):

            lastKeyTime = time.time()
            autoReset = False

            leftTrack = incrementValue(leftTrack)

            printToScreen("V pressed, decrease left track speed: " + str(leftTrack))

            if doGPIO:
                #pwmLeftTrack.ChangeFrequency(50)
                pwmLeftTrack.ChangeDutyCycle(leftTrack)


        if isKeyPressed('j'):

            lastKeyTime = time.time()
            autoReset = False

            rightTrack = decrementValue(rightTrack)

            printToScreen("J pressed, increase right track speed: " + str(rightTrack))

            if doGPIO:
                #pwmRightTrack.ChangeFrequency(50)
                pwmRightTrack.ChangeDutyCycle(rightTrack)


        if isKeyPressed('n'):

            lastKeyTime = time.time()
            autoReset = False

            rightTrack = incrementValue(rightTrack)

            printToScreen("N pressed, decrease right track speed: " + str(rightTrack))

            if doGPIO:
                #pwmRightTrack.ChangeFrequency(50)
                pwmRightTrack.ChangeDutyCycle(rightTrack)

        
        if isKeyPressed('t'):

            lastKeyTime = time.time()
            autoReset = False

            if tailLights:

                printToScreen("T pressed, Turn tail lights off")

                if doGPIO:
                    GPIO.output(27,GPIO.HIGH)

            else:

                printToScreen("T pressed, Turn tail lights on")
                
                if doGPIO:
                    GPIO.output(27,GPIO.LOW)

            tailLights = not tailLights


        if isKeyPressed('h'):

            lastKeyTime = time.time()
            autoReset = False

            if headLights:
    
                printToScreen("H pressed, Turn head lights off")

                if doGPIO:
                    GPIO.output(17,GPIO.HIGH)
            
            else:
                
                printToScreen("H pressed, Turn head lights on")
                
                if doGPIO:
                    GPIO.output(17,GPIO.LOW)

            headLights = not headLights


        if isKeyPressed('3'):

            lastKeyTime = time.time()
            autoReset = False

            if switch1:
    
                printToScreen("3 pressed, Turn switch1 off")

                if doGPIO:
                    GPIO.output(XX,GPIO.HIGH)
            
            else:
                
                printToScreen("3 pressed, Turn switch1 on")
                
                if doGPIO:
                    GPIO.output(XX,GPIO.LOW)

            switch1 = not switch1


        if isKeyPressed('4'):

            lastKeyTime = time.time()
            autoReset = False

            if switch2:
    
                printToScreen("4 pressed, Turn switch2 off")

                if doGPIO:
                    GPIO.output(XX,GPIO.HIGH)
            
            else:
                
                printToScreen("4 pressed, Turn switch2 on")
                
                if doGPIO:
                    GPIO.output(XX,GPIO.LOW)

            switch2 = not switch2


        if isKeyPressed(' '):

            lastKeyTime = time.time()

            printToScreen("Spacebar pressed, Reset to stopped")
            
            leftTrack = 7.1
            rightTrack = 7.1
            
            if doGPIO:
                # pwmLeftTrack.ChangeFrequency(.1)
                # pwmRightTrack.ChangeFrequency(.1)
                pwmLeftTrack.ChangeDutyCycle(leftTrack)
                pwmRightTrack.ChangeDutyCycle(rightTrack)   
        
        if char == curses.KEY_UP:
            
            printToScreen("Up Key pressed")
            if doGPIO:
                leftTrack = 6.4
                rightTrack = 6.4
                pwmLeftTrack.ChangeDutyCycle(leftTrack)
                pwmRightTrack.ChangeDutyCycle(rightTrack)

        if char == curses.KEY_DOWN:
            printToScreen("Down Key pressed")
            if doGPIO:
                leftTrack = 7.3
                rightTrack = 7.3
                pwmLeftTrack.ChangeDutyCycle(leftTrack)
                pwmRightTrack.ChangeDutyCycle(rightTrack)

        if char == curses.KEY_LEFT:
            printToScreen("Left Key pressed")
            if doGPIO:
                leftTrack = 7.5
                rightTrack = 6.7
                pwmLeftTrack.ChangeDutyCycle(leftTrack)
                pwmRightTrack.ChangeDutyCycle(rightTrack)

        if char == curses.KEY_RIGHT:
            printToScreen("Right Key pressed")
            if doGPIO:
                leftTrack = 6.7
                rightTrack = 7.5
                pwmLeftTrack.ChangeDutyCycle(leftTrack)
                pwmRightTrack.ChangeDutyCycle(rightTrack)

        if isKeyPressed('q'):
            
            printToScreen("Shutting down")
            
            if doGPIO:
            
                leftTrack = 7.1
                rightTrack = 7.1
                pwmLeftTrack.ChangeDutyCycle(leftTrack)
                pwmRightTrack.ChangeDutyCycle(rightTrack)
                pwmLeftTrack.stop()
                pwmRightTrack.stop()
                GPIO.cleanup()
            
            time.sleep(1.5)

            break

finally:
    
    # Close down curses properly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
