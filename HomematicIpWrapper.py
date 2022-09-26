import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContact,HeatingThermostat
from homematicip.device import TemperatureHumiditySensorDisplay
from homematicip.group import HeatingGroup

class HomematicIpWrapper():
    def __init__(self, *args, **kwargs):
        config = homematicip.find_and_load_config_file()
        self.home = Home()                
        self.home.set_auth_token(config.auth_token)
        self.home.init(config.access_point)       
        return super().__init__(*args, **kwargs)

    def getThermostates(self):
        self.home.get_current_state()

        thermostates = []

        for device in self.home.devices:
            if isinstance(device,HeatingThermostat):
                thermostates.append(device)

        return thermostates

    def getRoomByName(self,roomName):
        self.home.get_current_state()
        
        roomName = roomName.lower()

        for group in self.home.groups:
            if not isinstance(group, HeatingGroup): 
                continue

            label = group.label.lower()

            if roomName ==  label:
                return group
                
