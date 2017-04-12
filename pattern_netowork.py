import serial
import OSC

pc = serial.Serial('/dev/ttyACM0', 115200)

client = OSC.OSCClient()
my_port = int(raw_input("What UDP port shall I connect with?\n"))
my_user = raw_input("What shall my user number be?\n")
my_address = "/user/" + my_user
brain_ip = raw_input("...and what is the brain's IP?\n")
try:
    client.connect((brain_ip, my_port))
    print "Okay, I've connected to %s, using port %d, and I'm user %s" % (brain_ip, my_port, my_user)
except:
    print "Failed to connect"

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
    else:
        continue
