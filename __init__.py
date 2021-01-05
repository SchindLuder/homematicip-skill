import os
import re
import time
import subprocess
from mycroft import MycroftSkill, intent_file_handler, intent_handler

class Homematicip(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		
	def initialize(self):
		self.clientPath = self.settings.get('HmipClientPath')
		
	@intent_handler('homematicip.get.temperature.intent')
	def handle_get_temperature(self, message):
		self.speak('Wait i will try to read the temperature')
		room_type = message.data.get('room')
		if room_type is None:
			self.speak('This room type is unknown to me')
			return

		# Option from WorkingRoom, BathRoom, DiningRoom, Kitchen, SleepingRoom, LivingRoom
		workingDirectory = os.path.dirname(os.path.abspath(self.clientPath))
		self.log.info('trying to run client command from: ' + self.clientPath + ' workingDir:' + workingDirectory)
		
		result = subprocess.run([self.clientPath, '--list-devices'], stdout=subprocess.PIPE, cwd=workingDirectory) #"/home/pi/mycroft-core/.venv/bin")
		
		resultString = str(result.stdout).lower()
		
		self.log.info(resultString)
				
		split = resultString.split("\\n")
		
		for room in split:
			roomString = str(room)
			self.log.info('analyzing')
			self.log.info(roomString)
			
			match = re.match('actualtemperature', roomString)
			#r'actualtemperature\((?P<temp>[0-9]{1,}\.[0-9]{1,})\)'
			if match is None:
				self.log.info('could not match')
				self.log.info(roomString)
				continue
				
			self.log.info('here is the match')
			self.log.info(str(match))

def create_skill():
	return Homematicip()

