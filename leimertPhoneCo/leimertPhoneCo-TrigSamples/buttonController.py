from pyOSC3 import OSCClient, OSCMessage, OSCServer
from threading import Thread
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

'''
Button Setup
'''
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
def createClient(ip, port):
    client = OSCClient()
    client.connect((ip, port))
    return client

def createMessage(label):
    # adding the address
    msg = OSCMessage()
    address = "".join(["/", str(label)])

    msg.setAddress(address)
    msg.append(0)
    return msg

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
    server = OSCServer((address, port))
    # Register a handler for the desired address
    server.addMsgHandler("".join(["/", str(label)]), handler)
    # Start the server
    server.serve_forever()

if __name__ == "__main__":
    print("OSC CLIENT STARTING!")

    client = createClient("127.0.0.1", 57120)
    msg = createMessage("engine")
    
    print("OSC SERVER STARTING!")
    print()
    
    # Create a thread for the OSC server
    osc_thread = Thread(target=startServer, args=("127.0.0.1", 58110, "nowPlaying"))
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
