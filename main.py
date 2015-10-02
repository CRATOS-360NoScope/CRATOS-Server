from TurretController import TurretController
import time

ctrl = TurretController(pin_yaw=11, pin_pitch=12, debug=True)

ctrl.startYaw(1)

time.sleep(2)

ctrl.stopYaw()

time.sleep(2)

ctrl.startYaw(-1)

time.sleep(2)

ctrl.stopYaw()

time.sleep(2)

ctrl.startYaw(1, True)

time.sleep(2)

ctrl.stopYaw()

time.sleep(2)

ctrl.startYaw(-1, True)

time.sleep(2)

ctrl.stopYaw()
