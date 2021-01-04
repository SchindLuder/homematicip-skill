from mycroft import MycroftSkill, intent_file_handler, intent_handler
class Homematicip(MycroftSkill):
	def __init__(self):
		self.log.info('__init__')
		MycroftSkill.__init__(self)
		
	@intent_handler('homematicip.get.temperature.intent')
	def handle_get_temperature(self, message):
		self.log.info('get temperature intent detected')
		self.speak('Wait i will try to read the temperature')
		room_type = message.data.get('room')

		if room_type is None:
			self.speak('This room type is unknown to me')
		else:
			self.speak('I got the room. Here we go!')
			
def create_skill():
	return Homematicip()

