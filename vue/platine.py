import RPi.GPIO as GPIO
import time
import threading


class Platine:

    def __init__(self, controleur):
        self.controleur = controleur

        self.LED_ROUGE = 21
        self.LED_VERTE = 20
        self.BTN_START = 23
        self.BTN_VALID = 26
        self.PIR = 18
        self.BUZZER = 19

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.LED_ROUGE, GPIO.OUT)
        GPIO.setup(self.LED_VERTE, GPIO.OUT)
        GPIO.setup(self.BUZZER, GPIO.OUT)

        GPIO.setup(self.BTN_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BTN_VALID, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.running = True

        # état précédent des boutons (anti spam)
        self.last_start = 1
        self.last_valid = 1

        # cooldown PIR
        self.last_pir_time = 0

        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def set_led(self, actif):
        GPIO.output(self.LED_VERTE, actif)
        GPIO.output(self.LED_ROUGE, not actif)

    def bip(self, d=0.2):
        GPIO.output(self.BUZZER, 1)
        time.sleep(d)
        GPIO.output(self.BUZZER, 0)

    def mouvement_detecte(self):
        count = 0
        for _ in range(5):
            if GPIO.input(self.PIR):
                count += 1
            time.sleep(0.02)
        return count >= 4

    def loop(self):
        time.sleep(10)  # stabilisation PIR

        while self.running:

            # ===== BOUTON START (anti-rebond) =====
            current_start = GPIO.input(self.BTN_START)
            if self.last_start == 1 and current_start == 0:
                self.controleur.toggle_systeme()
            self.last_start = current_start

            # ===== BOUTON JAUNE (juste feedback) =====
            current_valid = GPIO.input(self.BTN_VALID)
            if self.last_valid == 1 and current_valid == 0:
                print("Bouton jaune pressé")
                self.bip(0.1)
            self.last_valid = current_valid

            # ===== PIR avec cooldown =====
            if self.controleur.systeme_actif:
                now = time.time()
                if self.mouvement_detecte() and now - self.last_pir_time > 2:
                    self.last_pir_time = now
                    self.controleur.mouvement()

            time.sleep(0.05)

    def stop(self):
        self.running = False
        self.thread.join()
        GPIO.cleanup()
