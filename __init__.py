from mycroft import MycroftSkill, intent_file_handler, intent_handler
class Homematicip(MycroftSkill):
	def __init__(self):
		MycroftSkill.__init__(self)
		
	def initialize(self):
		self.clientPath = self.settings.get('homematic_client_script')
		self.log.info(self.settings.get('homematic_client_script'))
		
	@intent_handler('homematicip.get.temperature.intent')
	def handle_get_temperature(self, message):
		self.speak('Wait i will try to read the temperature')
		room_type = message.data.get('room')

		self.log.info(self.clientPath)
		
		if room_type is None:
			self.speak('This room type is unknown to me')
		else:
			self.speak('I got the room. Here we go!')
			self.speak(str(room_type));
			
def create_skill():
	return Homematicip()

