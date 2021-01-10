import os
import re
import time
import subprocess
import time
from pixels import pixels
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern
from mycroft import MycroftSkill, intent_file_handler, intent_handler

class Homematicip(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		
	def initialize(self):
		self.clientPath = self.settings.get('HmipClientPath')
		pixels.pattern = GoogleHomeLedPattern(show=pixels.show)
		
	#def leds_thinking():
	#	try:
	#		pixels.think()            
#			pixels.speak()
#      			pixels.off()
#		except KeyboardInterrupt:
#			return
					
	@intent_handler('homematicip.get.temperature.intent')
	def handle_get_temperature(self, message):		
		pixels.think()
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
				pixels.speak()
				self.speak_dialog('say.temperature', {'room': room_type, 'temperature': temperature})
				pixels.off()
				
def create_skill():
	return Homematicip()

