import pyOSC3
import threading
from gpiozero import Button, LED
from time import sleep

'''
Controller setup
'''
prevPressInc = False
prevPressDec = False
prevPressSendMessage = False

lowerLimit = 0
upperLimit = 6
selection = 0
nowPlaying = False

buttonCountInc = Button(27)
buttonCountDec = Button(4)

sendMessage = Button(22)

nowPlayingLED = LED(23)
runningLED = LED(24)

def numberUp(upperLimit):
    global selection
    selection+=1
    if selection > upperLimit:
        selection = upperLimit

def numberDown(lowerLimit):
    global selection
    selection-=1
    if selection < lowerLimit:
        selection = lowerLimit


'''
OSC Client setup
'''
# create OSCClient
client = pyOSC3.OSCClient()
client.connect(("127.0.0.1", 57120))

# adding the address
msg = pyOSC3.OSCMessage()
address = ''.join(["/", "engine"])

# constructing the message
msg.setAddress(str(address))
msg.append(0)


'''
OSCServer setup
'''
def handler(addr, tags, stuff, source):
    global nowPlaying
    if stuff[0] == "FALSE":
        print("PLAYBACK IS DONE!")
        print("MAKE ANOTHER SELECTION!")
        nowPlayingLED.off()
        nowPlaying = False

def startServer(address, port, label):
    server = pyOSC3.OSCServer((address, port))
    # Register a handler for the desired address
    server.addMsgHandler("".join(["/", str(label)]), handler)
    # Start the server
    server.serve_forever()


if __name__ == "__main__":
    print("OSC SERVER STARTING!")
    print()
    
    # Create a thread for the OSC server
    osc_thread = threading.Thread(target=startServer, args=("127.0.0.1", 58110, "nowPlaying"))
    osc_thread.daemon = True  # Make the thread a daemon so it exits when the main thread exits
    osc_thread.start()

    print("OSC SERVER STARTED!")
    print()

    runningLED.on()
    
    # monitor button input
    while True:
        if buttonCountInc.is_pressed:
            if prevPressInc == False:
                numberUp(upperLimit)
                sleep(0.1)
                print(" ".join(["Selection:", str(selection)]))
                prevPressInc = True
        elif buttonCountDec.is_pressed:
            if prevPressDec == False:
                numberDown(lowerLimit)
                sleep(0.1)
                print(" ".join(["Selection:", str(selection)]))
                prevPressDec = True
        elif sendMessage.is_pressed:
            if prevPressSendMessage == False:
                if nowPlaying == False:
                    msg[0] = selection
                    client.send(msg)
                    nowPlayingLED.on()
                    nowPlaying = True
                    sleep(0.1)
                    prevPressSendMessage = True
                elif nowPlaying == True:
                    print("WAIT UNTIL PLAYBACK IS DONE TO PLAY ANOTHER SELECTION!")
        else:
            prevPressInc = False
            prevPressDec = False
            prevPressSendMessage = False
        sleep(0.1)
        pass
