import serial
import OSC
import requests
#the serial connection (default /dev/ttyACM0 on Pi)
pc = serial.Serial('/dev/ttyACM0', 115200)
#OSC client object
client = OSC.OSCClient()
#set a UDP port to send OSC messages
my_port = int(raw_input("What UDP port shall I connect with?\n"))
#set a user ID (0-8) so we know what instrument to control
my_user = raw_input("What shall my user number be?\n")
#create an OSC address based on that
my_address = "/user/" + my_user
#set the IP of the 'brain' computer, which will receive all patterns and create music
brain_ip = raw_input("...and what is the brain's IP?\n")
#set url for DB logging
brain_url = 'http://%s:5000' % (brain_ip)
#attempt OSC connection
try:
    client.connect((brain_ip, my_port))
    print "Okay, I've connected via UDP to %s, using port %d, and I'm user %s" % (brain_ip, my_port, my_user)
except:
    print "Failed to connect via UDP"

try:
    db_check = requests.get(brain_url + "/db_check")
    logging = db_check.json().get('logging')
except:
    logging = False

if logging:
    print "Logging appears to be active"

print "Now awaiting cards!"
while True:
    card = pc.readline()
    if len(card) == 37:
        if card[0:3] == ":01":
            pattern = card[3:19]
            oscmsg = OSC.OSCMessage()
            oscmsg.setAddress(my_address)
            oscmsg.append(pattern)
            client.send(oscmsg)
            print "Sending "  + pattern
            if logging:
                log = requests.get('%s/log/%s/%s' % (brain_url, my_user, pattern))
                print log.content
    else:
        continue
