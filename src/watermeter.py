#!/bin/usr/env python3
import datetime
import json
import time
from enum import Enum

import paho.mqtt.client as mqtt

from eemconvert import EEMConvert

MQTT_ADDRESS = "emqx"
MQTT_CLIENT_ID = "Watermeter_Groundfloor"
MQTT_PORT: int = 1883
USB_DEVICE = "/dev/ttyUSB0"


class Watertype(Enum):
    COLD = 1
    WARM = 2


class Watermeter:
    """Read cold an warm water meter from EEMConvert.

    Args:
        * convert (int): port name
        * serial (str): slave address in the range 1 to 247

    """

    def __init__(self, convert: EEMConvert, watertype: Watertype, meterid: int, pulse_per_unit=100) -> None:
        self.convert = convert
        self.meterid = meterid
        self.watertype = watertype
        self.pulse_per_unit = pulse_per_unit
        self.convert.set_pulse_per_unit(meterid, pulse_per_unit)
        return

    def __str__(self) -> str:
        water = {"Total": self.convert.get_counter(self.meterid), "Type": self.watertype.name}
        data = {"Time": datetime.now(), "WATER": water}
        return json.dumps(data)


def main():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.connect(MQTT_ADDRESS, MQTT_PORT)

    instrument = EEMConvert(USB_DEVICE, 1)  # port name, slave address (in decimal)
    instrument.debug = True

    coldwater = Watermeter(instrument, Watertype.COLD, 1)
    warmwater = Watermeter(instrument, Watertype.WARM, 2)

    time.sleep(30)

    client.loop_start()

    while True:
        client.publish("/places/our place/groundfloor/water", warmwater)
        client.publish("/places/our place/groundfloor/water", coldwater)
        time.sleep(30)


if __name__ == "__main__":
    print("watermeter: start")
    main()
