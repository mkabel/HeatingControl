import logging
from PyTado.interface import Tado

_LOG_ = logging.getLogger(__name__)


class TadoHelper:

    def __init__(self, account, pwd):
        self.my_tado = Tado(account, pwd)

    def checkWindowState(self):
        zones = self.my_tado.getZones()
        self.getClimate()

        for index, zone in enumerate(zones):
            # climate = self.my_tado.getClimate(zone['id'])
            if self.windowOpen(zone['id']):
                _LOG_.info('window open')
                self.my_tado.setOpenWindow(zone['id'])
            else:
                _LOG_.debug('window closed')

    def getClimate(self):
        zones = self.my_tado.getZones()

        for index, zone in enumerate(zones):
            capabilities = self.my_tado.getCapabilities(zone['id'])
            if capabilities['type'] == 'HEATING':
                climate = self.my_tado.getClimate(zone['id'])
            _LOG_.info(f'Temperature: {climate["temperature"]}, Humidity: {climate["humidity"]}')

    def windowOpen(self, zone_id):
        window_open = self.my_tado.getOpenWindowDetected(zone_id)
        return window_open['openWindowDetected']

    def resetOverlay(self, zoneName):
        zones = self.my_tado.getZones()

        for index, zone in enumerate(zones):
            if zone['name'] == zoneName:
                _LOG_.info(f'Reset overlay for {zoneName}')
                self.my_tado.resetZoneOverlay(zone['id'])
                return

    def setOverlay(self, zoneName, temp):
        zones = self.my_tado.getZones()

        for index, zone in enumerate(zones):
            if zone['name'] == zoneName:
                _LOG_.info(f'Overlay {zoneName} to {temp}')
                self.my_tado.setZoneOverlay(zone['id'], 'MANUAL', temp)
                return
