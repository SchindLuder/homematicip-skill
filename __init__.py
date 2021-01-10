import os
import re
import time
import subprocess
import time
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern
from mycroft import MycroftSkill, intent_file_handler, intent_handler

class Homematicip(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		
	def initialize(self):
		self.clientPath = self.settings.get('HmipClientPath')
		self.pixels = Pixels()
		self.pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
					
	@intent_handler('homematicip.get.temperature.intent')
	def handle_get_temperature(self, message):		
		self.pixels.think()
		room_type = message.data.get('room')
		if room_type is None:			
			return
		
		room_type = room_type.replace(" ","")
		
		#self.speak_dialog('wait.for', {'command': 'get the temperature for ' + room_type})

		# Option from WorkingRoom, BathRoom, DiningRoom, Kitchen, SleepingRoom, LivingRoom
		workingDirectory = os.path.dirname(os.path.abspath(self.clientPath))
		self.log.info('trying to run client command from: ' + self.clientPath + ' workingDir:' + workingDirectory)
		
		result = subprocess.run([self.clientPath, '--list-devices'], stdout=subprocess.PIPE, cwd=workingDirectory)
		resultString = str(result.stdout).lower()	
		split = resultString.split("\\n")
						
		room_dict = {
			"bathroom" : "wandthermostat bad",
			"restroom" : "wandthermostat bad",
			"workingroom" : "arbeitszimmer",
			"couchroom" :"couchzimmer", 
			"livingroom" :"couchzimmer", 			
			"cookingroom": "che heizung",
			"kitchen": "che heizung",			
			"kitchenroom": "che heizung",
			"diningroom": "balkonzimmer",
			"sleepingroom" :"schlafzimmer",
			"bedroom" :"schlafzimmer"
		}
		
		if room_type not in room_dict:
			self.speak_dialog('unknown.room', { 'room' : room_type });
			return
		
		desired_room = str(room_dict[room_type])
		
		for room in split:
			roomString = str(room)
						
			#self.log.info('analyzing')
			#self.log.info(roomString[1:30])
			
			match = re.search(r'actualtemperature\((?P<temp>[0-9]{1,}\.[0-9]{1,})\)', roomString)
			#r'actualtemperature\((?P<temp>[0-9]{1,}\.[0-9]{1,})\)'
			if match is None:
				#self.log.info('could not match')
				#self.log.info(roomString)
				continue
				
			if  desired_room in roomString:
				temperature = match.group('temp')
				self.pixels.speak()
				self.speak_dialog('say.temperature', {'room': room_type, 'temperature': temperature})
				self.pixels.off()
class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=AlexaLedPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        
        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()

				
def create_skill():
	return Homematicip()

