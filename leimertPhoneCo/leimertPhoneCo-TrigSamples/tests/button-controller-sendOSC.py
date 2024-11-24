import pyOSC3
import threading
from gpiozero import Button
from time import sleep

'''
button setup
'''

prevPressInc = False
prevPressDec = False
prevPressSendMessage = False

lowerLimit = 0
upperLimit = 5
count = 0
nowPlaying = False

buttonCountInc = Button(4)
buttonCountDec = Button(27)

sendMessage = Button(22)

def numberUp(upperLimit):
    global count
    count+=1
    if count > upperLimit:
        count = upperLimit

def numberDown(lowerLimit):
    global count
    count-=1
    if count < lowerLimit:
        count = lowerLimit
'''
OSC Client setup
'''

# create OSCClient
client = pyOSC3.OSCClient()
client.connect(('127.0.0.1', 57120))

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
        nowPlaying = False

def startServer():
    server = pyOSC3.OSCServer(('127.0.0.1', 58110))  # Listen on the specified IP and port
    # Register a handler for the desired address
    server.addMsgHandler("/nowPlaying", handler)
    # Start the server
    server.serve_forever()

if __name__ == "__main__":
    print("OSC SERVER STARTING!")
    print()
    
    # Create a thread for the OSC server
    osc_thread = threading.Thread(target=startServer)
    osc_thread.daemon = True  # Make the thread a daemon so it exits when the main thread exits
    osc_thread.start()

    print("OSC SERVER STARTED!")
    print()

    # monitor button input
    while True:
        if nowPlaying == False:
            if buttonCountInc.is_pressed:
                if prevPressInc == False:
                    numberUp(upperLimit)
                    sleep(0.1)
                    print(" ".join(["COUNT:", str(count)]))
                    prevPressInc = True
            elif buttonCountDec.is_pressed:
                if prevPressDec == False:
                    numberDown(lowerLimit)
                    sleep(0.1)
                    print(" ".join(["COUNT:", str(count)]))
                    prevPressDec = True
            elif sendMessage.is_pressed:
                if prevPressSendMessage == False:
                    msg[0] = count
                    client.send(msg)
                    nowPlaying = True
                    sleep(0.1)
                    prevPressSendMessage = True
            else:
                prevPressInc = False
                prevPressDec = False
                prevPressSendMessage = False
            sleep(0.1)
        pass
