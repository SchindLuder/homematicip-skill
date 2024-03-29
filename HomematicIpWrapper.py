import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContact,HeatingThermostat
from homematicip.device import TemperatureHumiditySensorDisplay
from homematicip.group import HeatingGroup
from homematicip.base.enums import *
from enum import Enum

class HomematicIpStatusCode(Enum):
    Ok = 0
    MinTempExceeded = 1
    MaxTempExceeded = 2
    UnknownRoom = 3
    CommandAlreadyActive = 4
    Error = 5

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

    def getRoomTemperature(self, roomName: str) -> (HomematicIpStatusCode,float):
        self.home.get_current_state()

        room = self._getRoomByName(roomName)

        if room is None:
            self.log.info(f'Could not return temperature as no room was found for name \'{roomName}\'')
            return (HomematicIpStatusCode.UnknownRoom, None)

        if room.actualTemperature is not None: 
            return (HomematicIpStatusCode.Ok, room.actualTemperature)

        #for some reason the room does not have a temperature
        for device in room.devices:
            #check for any wallmounted thermostat and retrieve actualTemperature
            if hasattr(device, 'actualTemperature') and device.actualTemperature is not None:
                return (HomematicIpStatusCode.Ok, device.actualTemperature)

            #check for any thermostat and get the valveActualTemperature
            if hasattr(device, 'valveActualTemperature') and device.valveActualTemperature is not None:
                return (HomematicIpStatusCode.Ok, device.valveActualTemperature)

        return (HomematicIpStatusCode.Error, None)                

        

    getRoomTemperature.__doc__ ="Gets temperature of the room. Return (HomematicIpStatusCode, float)"

    def setRoomTemperature(self, roomName: str, temperature: float) -> HomematicIpStatusCode:
        self.home.get_current_state()
        room = self._getRoomByName(roomName)

        temperature = float(temperature)

        if room is None:
            self.log.info(f'Could not set temperature as no room was found for name \'{roomName}\'')
            return HomematicIpStatusCode.UnknownRoom, 

        if temperature == room.setPointTemperature:
            return HomematicIpStatusCode.CommandAlreadyActive

        if temperature > room.maxTemperature:
            return HomematicIpStatusCode.MaxTempExceeded

        if temperature < room.minTemperature:
            return HomematicIpStatusCode.MinTempExceeded

        retVal = room.set_point_temperature(temperature)

        if retVal is '': 
            # setting of temperature was successful
            return HomematicIpStatusCode.Ok

        self.log.info(f'Could not set temperature: {retVal}')
        return HomematicIpStatusCode.Error
    _getRoomByName.__doc__ = "Sets setPoint temperature for room and returns state"

    def activateBoost(self, roomName: str) -> (HomematicIpStatusCode):
        room = self._getRoomByName(roomName)

        if room is None: 
            return HomematicIpStatusCode.UnknownRoom

        if room.boostMode is True:
            return HomematicIpStatusCode.CommandAlreadyActive

        retVal = room.set_boost()

        if retVal is '': 
            return HomematicIpStatusCode.Ok

        return HomematicIpStatusCode.Error

    def deactivateBoost(self, roomName: str) -> (HomematicIpStatusCode):
        room = self._getRoomByName(roomName)

        if room is None: 
            return HomematicIpStatusCode.UnknownRoom

        if room.boostMode is False:
            return HomematicIpStatusCode.CommandAlreadyActive

        retVal = room.set_boost(False)

        if retVal is '': 
            return HomematicIpStatusCode.Ok

        return HomematicIpStatusCode.Error

    def isWindowOpenInRoom(self, roomName: str) -> bool:                
        room = self._getRoomByName(roomName)

        if room is None:
            self.log.info(f'Could not check window state as no room was found for name \'{roomName}\'')
            return (HomematicIpStatusCode.UnknownRoom, None)

        if room.windowState == WindowState.CLOSED.value:
            return (HomematicIpStatusCode.Ok, False)

        if room.windowState == WindowState.OPEN.value:
            return (HomematicIpStatusCode.Ok, True)

        self.log.info(f'Window state of room \'{roomName}\' is \'{room.windowState}\'')

        return (HomematicIpStatusCode.Error, None)
    
    def getRoomsWithOpenWindows(self) -> {HomematicIpStatusCode, list}:
        self.home.get_current_state()

        roomsWithOpenWindows = list()

        try:
            for group in self.home.groups: 
                if not isinstance(group, HeatingGroup):
                    continue

                if group.windowState == WindowState.OPEN.value:
                    roomsWithOpenWindows.append(group.label)
                    continue
        except:
            return (HomematicIpStatusCode.Error, None)
        
        return (HomematicIpStatusCode.Ok, roomsWithOpenWindows)
    getRoomsWithOpenWindows.__doc__ = "Returns a list of all HeatingGroups with open windows. List is empty if no room has an open window"