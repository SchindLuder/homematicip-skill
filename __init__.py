from mycroft import MycroftSkill, intent_file_handler


class Homematicip(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('homematicip.get.temperature.intent')
    def handle_get_temperature(self, message):
        self.speak('Wait i will try to read the temperature')
        room_type = message.data.get('room')

        if room_type is None:
           self.speak('This room type is unknown to me')

	self.speak('I got the room. Here we go!')

    def converse(self, utterances,lang):
        self.log.info("converse of homematic skill called")
        return False

def create_skill():
    return Homematicip()

