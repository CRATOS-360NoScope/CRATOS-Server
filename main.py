from TurretController import TurretController
from subprocess import call
import time

#call("hciconfig hci0 piscan")

ctrl = TurretController(pin_yaw=11, pin_pitch=12, debug=True)
time.sleep(2)

ctrl.startPitch(1)
print "Done 1"
time.sleep(2)
print "HI"
ctrl.startPitch(-1)
print "Done 2"
time.sleep(2)
ctrl.startYaw(1)

time.sleep(2)

ctrl.stopYaw()

time.sleep(2)

ctrl.startYaw(-1)

time.sleep(2)

ctrl.stopYaw()

time.sleep(2)

ctrl.startYaw(1, .2)

time.sleep(2)

ctrl.stopYaw()

time.sleep(2)

ctrl.startYaw(-1, .2)

time.sleep(2)

ctrl.stopYaw()