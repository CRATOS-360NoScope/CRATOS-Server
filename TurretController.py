import RPi.GPIO as GPIO
import time
class TurretController:

	GPIO_PIN_YAW   = 11 
	GPIO_PIN_PITCH = 12
	pwm_yaw   = None
	pwm_pitch = None
	current_pitch = 7.5
	stopPitch = False
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
		self.pwm_pitch.start(7.5)
		self.DEBUG = debug		

	def __del__(self):
		self.pwm_yaw.stop()
		self.pwm_pitch.stop()
		GPIO.cleanup()
	
	# direction +1 for clockwise, -1 for reverse
	def startYaw(self, direction, sensitivity=1):
		modifier = 2.5*sensitivity
		if self.DEBUG:
			print "** startYaw **"
			print "Direction: "+str(direction)
			print "Sensitivity: "+str(sensitivity)
			print "Duty Cycle: "+str(7.5+(modifier*direction))
		self.pwm_yaw.ChangeDutyCycle(7.5+(modifier*direction))

	def stopYaw(self):
		if self.DEBUG:
			print "** stopYaw **"
		self.pwm_yaw.ChangeDutyCycle(7.5)

	# TODO: Auto stop for limit +60 or -30
	def startPitch(self, direction, sensitivity=.1):
		self.stopPitch = False
		if self.DEBUG:
			print "** startPitch **"
		print "Direction: "+str(direction)
		while (not self.stopPitch):
			self.current_pitch += direction*sensitivity
			if (self.current_pitch > 12.5):
				self.current_pitch = 12.5
				self.stopPitch = True
				break
			if (self.current_pitch < 0):
				self.current_pitch = 0
				self.stopPitch = True
				break
			print "Duty Cycle: "+str(self.current_pitch)
			self.pwm_pitch.ChangeDutyCycle(self.current_pitch)
			time.sleep(0.001)
			

	def stopPitch(self):
		if self.DEBUG:
			print "** stopPitch **"
		self.stopPitch = True
