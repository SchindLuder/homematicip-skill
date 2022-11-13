from HomematicIpWrapper import HomematicIpWrapper
from HomematicIpWrapper import HomematicIpStatusCode

class log(object):
	def info(self,message):
		print(message)

	def debug(self,message):
		print('debug: ' + message)

class selfMockup(object):
	def __init__(self): 
		self.log = log()

	def speak_dialog(self, dialogName, values):
		print('dialog: ' + dialogName)

	def speak(self,message):
		print('speak: ' + message)

	def ask_yesno(self,question):
		print('ask_yesno: '+ question)

self = selfMockup()

homematicIp = HomematicIpWrapper(self.log)

roomList = list()
roomList.append('Küche')
roomList.append('Bad')

readableRoomList = str(roomList).replace('\'','').lstrip('[').rstrip(']').replace(',',' und ')


a = readableRoomList
