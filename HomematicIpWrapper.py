import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContact,HeatingThermostat
from homematicip.device import TemperatureHumiditySensorDisplay
from homematicip.group import HeatingGroup
from enum import Enum

class homematicIpStatusCode(Enum):
    Ok = 0
    MinTempExceeded = 1
    MaxTempExceeded = 2
    UnknownRoom = 3
    Error = 4

class HomematicIpWrapper():
    def __init__(self, loggingMethod, *args, **kwargs):
        self.log = loggingMethod
        config = homematicip.find_and_load_config_file()        
        self.home = Home()                
        self.home.set_auth_token(config.auth_token)
        self.home.init(config.access_point)       
        return super().__init__(*args, **kwargs)   

    def _getRoomByName(self,roomName: str) -> HeatingGroup :
        self.home.get_current_state()
        
        roomName = roomName.lower()

        for group in self.home.groups:
            if not isinstance(group, HeatingGroup): 
                continue

            label = group.label.lower()

            if roomName ==  label:
                return group

        self.log.info(f'could not find room with name \'{roomName}\'')
        return None

    _getRoomByName.__doc__ = "Returns HeatingGroup with matching label or None"

    def getRoomTemperature(self, roomName: str) -> (homematicIpStatusCode,float):
        self.home.get_current_state()

        room = self._getRoomByName(roomName)

        if room is None:
            self.log.info(f'Could not return temperature as no room was found for name \'{roomName}\'')
            return (homematicIpStatusCode.UnknownRoom, None)

        return (homematicIpStatusCode.Ok, room.actualTemperature)
    getRoomTemperature.__doc__ ="Gets temperature of the room. Return (homematicIpStatusCode, float)"

    def setRoomTemperature(self, roomName: str, temperature: float) -> homematicIpStatusCode:
        self.home.get_current_state()
        room = self._getRoomByName(roomName)

        if room is None:
            self.log.info(f'Could not set temperature as no room was found for name \'{roomName}\'')
            return homematicIpStatusCode.UnknownRoom, 

        if temperature > room.maxTemperature:
            return homematicIpStatusCode.MaxTempExceeded

        if temperature < room.minTemperature:
            return homematicIpStatusCode.MinTempExceeded

        retVal = room.set_point_temperature(temperature)

        if retVal is '': 
            # setting of temperature was successful
            return homematicIpStatusCode.Ok

        self.log.info(f'Could not set temperature: {retVal}')
        return homematicIpStatusCode.Error
    _getRoomByName.__doc__ = "Sets setPoint temperature for room and returns state"

    def activateBoost(self, roomame: str) -> (homematicIpStatusCode):
        room = self._getRoomByName(roomName)

        if room is None: 
            return homematicIpStatusCode.UnknownRoom

        retVal = room.set_boost()

        if retVal is None: 
            return homematicIpStatusCode.Ok

        return homematicIpStatusCode.Error

    def deactivateBoost(self, roomName: str) -> (homematicIpStatusCode):
        room = self._getRoomByName(roomName)

        if room is None: 
            return homematicIpStatusCode.UnknownRoom

        room.set_boost(False)
        


        
        

