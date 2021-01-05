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
		
		self.speak('I got the room. Here we go!')
		self.speak(str(room_type));
		# Option from WorkingRoom, BathRoom, DiningRoom, Kitchen, SleepingRoom, LivingRoom

		self.log.info('trying to run client command from: ' + self.clientPath)
		
		result = subprocess.run([self.clientPath, '--list-devices'], stdout=subprocess.PIPE, cwd="/home/pi/mycroft-core/.venv/bin")
		self.log.info(result)
		
def create_skill():
	return Homematicip()

