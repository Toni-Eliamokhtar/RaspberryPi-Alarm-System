import RPi.GPIO as GPIO
import time
import threading


class Platine:

    def __init__(self, controleur):
        self.c = controleur

        self.LED_ROUGE = 21
        self.LED_VERTE = 20
        self.BTN = 23
        self.PIR = 18

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.LED_ROUGE, GPIO.OUT)
        GPIO.setup(self.LED_VERTE, GPIO.OUT)
        GPIO.setup(self.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.running = True

        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def set_led(self, actif):
        GPIO.output(self.LED_VERTE, actif)
        GPIO.output(self.LED_ROUGE, not actif)

    def bouton_presse(self):
        return GPIO.input(self.BTN) == 0

    def loop(self):
        while self.running:
            if self.c.systeme_actif and GPIO.input(self.PIR):
                self.c.mouvement()
                time.sleep(1)
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.thread.join()
        GPIO.cleanup()
