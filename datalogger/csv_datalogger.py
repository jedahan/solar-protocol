# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
import time
import datetime
import random
import csv
import os
import signal
import sys
from logging import info
from solar_common import fieldnames

# code originally generated by chatGPT with the prompt:
# "Write some python code that determines if it is running on a Raspberry Pi computer"
import platform

RASPBERRY_PI = platform.machine().startswith("armv")
# end code generated by chatGPT

if RASPBERRY_PI:
    from pymodbus.client import ModbusSerialClient


def writeOrAppend(row):
    """
    create a new file daily to save data or append if the file already exists
    """
    fileName = f"/data/traces/{datetime.date.today()}.csv"
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow(row)

    info(f"csv writing: {datetime.datetime.now()}")

def randomReadable(start: int, end: int):
    return round(random.uniform(start, end))


def readFromRandom():
    return {
        "timestamp": time.time(),
        "PV voltage": randomReadable(9, 30),
        "PV current": randomReadable(0, 2),
        "PV power L": randomReadable(28, 34),
        "PV power H": randomReadable(0, 1),
        "battery voltage": randomReadable(11, 15),
        "battery current": randomReadable(2, 3),
        "battery power L": randomReadable(28, 32),
        "battery power H": randomReadable(0, 1),
        "load voltage": randomReadable(12, 16),
        "load current": randomReadable(0, 1),
        "load power": randomReadable(3, 5),
        "battery percentage": randomReadable(0, 1),
    }


def readFromDevice():
    controller = client.read_input_registers(0x3100, 16, unit=1)
    battery = client.read_input_registers(0x311A, 2, unit=1)

    if controller.isError():
        error(controller)
    if battery.isError():
        error(battery)
    if battery.isError() or controller.isError():
        return

    def toPercent(number):
        return float(number / 100.0)

    registers = controller.registers.map(toPercent)

    data = dict(zip(fieldnames, registers[0:10]))
    data["timestamp"] = time.time()
    data["battery percentage"] = toPercent(battery)
    return data


read = readFromRandom

if RASPBERRY_PI:
    client = ModbusSerialClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
    client.connect()
    read = readFromDevice


def handle_exit(sig, frame):
    if RASPBERRY_PI:
        client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)

while True:
    writeOrAppend(read())
    time.sleep(60 * 2)
