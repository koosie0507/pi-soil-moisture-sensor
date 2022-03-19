try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("couldn't do it... can't do nice stuff with this pi")
    exit(4)

import time
from signal import signal, SIGINT, SIGHUP, SIGTERM

RUN_LOOP=True
SENSOR=11
ACTUATOR=15

def stop_loop(_, __):
    global RUN_LOOP
    RUN_LOOP=False
    print("Bye.")

for sig in [SIGINT, SIGHUP, SIGTERM]:
    signal(sig, stop_loop)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ACTUATOR, GPIO.OUT)

def show_status(channel):
    value = GPIO.input(channel)
    print("wet" if not value else "dry")
    GPIO.output(ACTUATOR, GPIO.HIGH if not value else GPIO.LOW)

GPIO.add_event_detect(SENSOR, GPIO.BOTH)
GPIO.add_event_callback(SENSOR, show_status)

while RUN_LOOP:
    time.sleep(1)
