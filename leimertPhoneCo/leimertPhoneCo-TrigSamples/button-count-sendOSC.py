import pyOSC3
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
OSC setup
'''

# create OSCClient
client = pyOSC3.OSCClient()
client.connect(('127.0.0.1', 57120))

# adding the address
msg = pyOSC3.OSCMessage()
address = ''.join(["/", "engine"])

# constructing the message
msg.setAddress(str(address))
msg.append(1)

while True:
    if buttonCountInc.is_pressed:
        if prevPressInc == False:
            numberUp(upperLimit)
            sleep(0.1)
            print(" ".join(["count is", str(count)]))
            prevPressInc = True
    elif buttonCountDec.is_pressed:
        if prevPressDec == False:
            numberDown(lowerLimit)
            sleep(0.1)
            print(" ".join(["count is", str(count)]))
            prevPressDec = True
    elif sendMessage.is_pressed:
        if prevPressSendMessage == False:
            # OSC below
            #print(" ".join(["sending message:", str(count)]))
            
            msg[0] = count
            client.send(msg)
            sleep(0.1)
            prevPressSendMessage = True
    else:
        prevPressInc = False
        prevPressDec = False
        prevPressSendMessage = False
    sleep(0.1)
