import RPi.GPIO as GPIO

class TurretController:

	GPIO_PIN_YAW   = 11 
	GPIO_PIN_PITCH = 12
	pwm_yaw   = None
	pwm_pitch = None
	DEBUG = False

	def __init__(self, pin_yaw, pin_pitch, debug=False):
		self.GPIO_PIN_YAW = pin_yaw 
		self.GPIO_PIN_PITCH = pin_pitch
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.GPIO_PIN_YAW, GPIO.OUT)
		GPIO.setup(self.GPIO_PIN_PITCH, GPIO.OUT)
		self.pwm_yaw = GPIO.PWM(self.GPIO_PIN_YAW, 53)
		self.pwm_pitch = GPIO.PWM(self.GPIO_PIN_PITCH, 50)
		self.pwm_yaw.start(7.5)
		self.DEBUG = debug		

	def __del__(self):
		self.pwm_yaw.stop()
		self.pwm_pitch.stop()
		GPIO.cleanup()
	
	# direction +1 for clockwise, -1 for reverse
	def startYaw(self, direction, fine=False):
		modifier = 0.1 if fine else 2.5
		if self.DEBUG:
			print "** startYaw **"
			print "Direction: "+str(direction)
			print "Fine: "+str(fine)
			print "Duty Cycle: "+str(7.5-(modifier*direction))
		self.pwm_yaw.ChangeDutyCycle(7.5-(modifier*direction))

	def stopYaw(self):
		if self.DEBUG:
			print "** stopYaw **"
		self.pwm_yaw.ChangeDutyCycle(7.5)

	# TODO: Auto stop for limit +60 or -30
	def startPitch(self, direction, fine=False):
		modifier = 10 if fine else 49
                self.pwm_pitch.start(50-(modifier*direction))

	def stopPitch(self):
		self.pwm_pitch.stop()
