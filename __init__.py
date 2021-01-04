from mycroft import MycroftSkill, intent_file_handler


class Homematicip(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('homematicip.intent')
    def handle_homematicip(self, message):
        self.speak_dialog('homematicip')


def create_skill():
    return Homematicip()

