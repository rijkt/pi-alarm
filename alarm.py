#!/usr/bin/python3

import threading
import time
from gpiozero import TonalBuzzer
from rpi_TM1638 import TMBoards
from my_logger import get_logger

speaker = 2 #gpio
buzzer = TonalBuzzer(speaker)
tm_clock = 27
tm_diode = 17
tm_strobe = 22
default_buttons = [0, 0, 0, 0]

def start_alarm():
    buzzer.play("C4")
    logger = get_logger("start_alarm")
    logger.info("started playing")

def stop_alarm():
    buzzer.stop()
    buzzer.close()
    logger = get_logger("stop_alarm")
    logger.info("stopped playing")

def handle_input():
    brightness_max = 7
    tm_board = TMBoards(tm_diode, tm_clock, tm_strobe, brightness_max)
    i = tm_board.getData(None)
    logger = get_logger("handle_input")
    while i == default_buttons:
        i = tm_board.getData(None)
        logger.info(f"read i: [{0}]".format(" ".join(str(n) for n in i)))
        if i != default_buttons:
            stop_alarm()
        time.sleep(0.1)

if __name__ == "__main__":
    main_logger = get_logger("main")
    main_logger.info('started script')
    # todo: try out https://docs.python.org/3/library/asyncio.html
    alarm_t = threading.Thread(target=start_alarm)
    main_logger.info('instantiated thread')
    alarm_t.start()
    main_logger.info('started thread')
    handle_input()
    alarm_t.join()
    main_logger.info("done")
