from bluetooth import *
import threading
import sys
import json
from TurretController import TurretController
from DataLogger import DataLogger

tc = TurretController(pin_yaw=11, pin_pitch=12, pin_fire=13, debug=True)
server_sock=BluetoothSocket( RFCOMM )
decoder = json.JSONDecoder()
dl = DataLogger(debug=True)
client_sock = ""

def btAdvertise():
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]

	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

	advertise_service( server_sock, "SampleServer",
			   service_id = uuid,
			   service_classes = [ uuid, SERIAL_PORT_CLASS ],
			   profiles = [ SERIAL_PORT_PROFILE ],
	#                   protocols = [ OBEX_UUID ]
			    )

	print "Waiting for connection on RFCOMM channel %d" % port

	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info
	return client_sock

def process_command(json_data):
        command = json_data["command"]
        if  command == "Horizontal":
            power = json_data["Power"]
            if power > 0:
                tc.startYaw(1)
            elif power < 0:
                tc.startYaw(-1)
            else:
                tc.stopYaw()
        if  command == "Vertical":
            power = json_data["Power"]
            if power > 0:
                tc.startPitch(1)
            elif power < 0:
                tc.startPitch(-1)
            else:
                tc.stopPitch()
        if  command == "Fire":
            tc.pullTrigger()
            dl.writeLog(device_id="test-device-324325")

        if  command == "Logs":
            logs = dl.readLog()
            log_json = json.dumps(logs)
            client_sock.send(log_json)
            print "Send Firing Log"


def handleInput(client_sock):

	try:
	    while killThreads==False:
		data = client_sock.recv(1024)
		if len(data) == 0: break
		print "received [%s]" % data
                string_list = [e+"}" for e in data.split("}") if e!=""]
                for item in string_list:
                    print item
                    json_data = decoder.decode(item)
                    if ("command" in json_data):
                        print "Command in json"
                        process_command(json_data)


	except IOError:
	    print "disconnected, restarting service"
	    client_sock.close()
            server_sock.close()
	    handleInput(btAdvertise())

	sys.exit(0)

	#except KeyboardInterrupt:
	#    print "disconnected, quitting"
	#    client_sock.close()
	#    server_sock.close()
	#    sys.exit(0)

killThreads = False
handleInput(btAdvertise());


#listenerThread = threading.Thread(target=handleInput, args=(btAdvertise(),))
#listenerThread.start();
#while True:
#
#    try:
#   	pass
#
#   except KeyboardInterrupt:
#	    listenerThread.stop()
#	    print "disconnected, quitting"
#	    client_sock.close()
#	    server_sock.close()
#	    sys.exit(0)
#
#
#
#print "all done"
