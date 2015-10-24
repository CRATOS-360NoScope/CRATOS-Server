import RPi.GPIO as GPIO
import time
import threading

class TurretController:

	GPIO_PIN_YAW   = 11
	GPIO_PIN_PITCH = 12
        GPIO_PIN_FIRE = 13
	pwm_yaw   = None
	pwm_pitch = None
	current_pitch = 7.5
	stopPitchFlag = False
	DEBUG = False
	pitchDelta = False
	pitchingActive = False
	pitchThread = None

	def __init__(self, pin_yaw, pin_pitch, pin_fire, debug=False):
		self.GPIO_PIN_YAW = pin_yaw
		self.GPIO_PIN_PITCH = pin_pitch
		self.GPIO_PIN_FIRE = pin_fire
                GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.GPIO_PIN_YAW, GPIO.OUT)
		GPIO.setup(self.GPIO_PIN_PITCH, GPIO.OUT)
		GPIO.setup(self.GPIO_PIN_FIRE, GPIO.OUT)
		self.pwm_yaw = GPIO.PWM(self.GPIO_PIN_YAW, 53)
		self.pwm_pitch = GPIO.PWM(self.GPIO_PIN_PITCH, 50)
		self.pwm_fire = GPIO.PWM(self.GPIO_PIN_FIRE, 50)
		self.pwm_yaw.start(7.5)
		self.pwm_pitch.start(7.5)
                self.pwm_yaw.ChangeDutyCycle(0)
                self.pwm_pitch.ChangeDutyCycle(0)
		self.DEBUG = debug
                self.triggerThread = threading.Thread(target=self.triggerWork)
		self.pitchThread = threading.Thread(target=self.pitchWorker)

	def __del__(self):
		self.pwm_yaw.stop()
		self.pwm_pitch.stop()
		GPIO.cleanup()


        def triggerWork(self):
            self.pwm_fire.ChangeDutyCycle(10) #pull trigger(not tested)
            time.sleep(2)
            self.pwm_fire.ChangeDutyCycle(7.5) #return to original spot
            print "Trigger Pulled"
            return

        def pullTrigger(self, sensitivity=1):
            self.pitchThread = threading.Thread(target=self.triggerWork)
            self.pitchThread.start()

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
		self.pwm_yaw.ChangeDutyCycle(0) #was 7.5 -> 0 is off

	def startPitch(self, direction, sensitivity=.1):
		self.pitchDelta = direction*sensitivity
		if self.DEBUG:
                        print "** startPitch **"
			print "pitchDelta: "+str(self.pitchDelta)
		if not self.pitchingActive:
			if self.DEBUG:
				print "pitchThread run"
		        self.pitchThread = threading.Thread(target=self.pitchWorker)
			self.stopPitchFlag = False
                        self.pitchThread.start()
			print "pitchThread running"

	def pitchWorker(self):
                while not self.stopPitchFlag:
                        self.current_pitch += self.pitchDelta
                        if self.current_pitch > 12.5:
                                self.current_pitch = 12.5
                                break
                        if self.current_pitch < 0:
                                self.current_pitch = 0
				break
                        print "Duty Cycle: "+str(self.current_pitch)
                        self.pwm_pitch.ChangeDutyCycle(self.current_pitch)
                        time.sleep(0.1)
		self.pitchingActive = False
                self.pwm_pitch.ChangeDutyCycle(0)
		print "pitchWorker exit"
		return

	def stopPitch(self):
		if self.DEBUG:
			print "** stopPitch **"
			print "currentPitch: "+str(self.current_pitch)
		self.stopPitchFlag = True

