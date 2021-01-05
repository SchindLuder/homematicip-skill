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
				
		split = resultString.split("hmip")
		
		for room in split:
			self.log.info(room[0:15])
			self.log.info(room + 'analyzed')
						
			m = re.match(r'actualtemperature\(.{1,4}\)', room)
			#r'actualtemperature\((?P<temp>[0-9]{1,}\.[0-9]{1,})\)'
			if m is None:
				continue
			
			self.log.info(str(m))
		
def create_skill():
	return Homematicip()

