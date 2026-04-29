import RPi.GPIO as GPIO


class Platine:

    def __init__(self, controleur):
        self.c = controleur

        self.LED_ROUGE = 21
        self.LED_VERTE = 20
        self.BTN = 23

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.LED_ROUGE, GPIO.OUT)
        GPIO.setup(self.LED_VERTE, GPIO.OUT)
        GPIO.setup(self.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def set_led(self, actif):
        GPIO.output(self.LED_VERTE, actif)
        GPIO.output(self.LED_ROUGE, not actif)

    def bouton_presse(self):
        return GPIO.input(self.BTN) == 0
