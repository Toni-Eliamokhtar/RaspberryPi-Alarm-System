from gpiozero import LED, Button, Buzzer, MotionSensor
import RPi.GPIO as GPIO
import time
import threading
import moduleCapteurs.LCD1602 as LCD1602
import moduleCapteurs.KeypadGPIO5 as c


class Platine:

    def __init__(self, controleur):
        self.controleur = controleur

        # Leds
        self.led_rouge = LED(21)
        self.led_verte = LED(20)
        
        # Boutons
        self.btn_start = Button(23, pull_up=True)
        self.btn_valid = Button(26, pull_up=True)
        
        # capteur PIR (détection de mouvement)
        self.pir = MotionSensor(18)
        
        # Buzzer
        self.buzzer = Buzzer(19)


        # Keypad
        self.ROWS = 4
        self.COLS = 4
        self.touches = [
            '1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'
        ]
        self.lignes  = [27, 22,  5,  6]   # lignes   : IO27, IO22, IO5, IO6
        self.colonnes = [24, 25, 12, 16]  # colonnes : IO24, IO25, IO12, IO16
        self.clavier = c.Keypad(self.touches, self.lignes, self.colonnes, self.ROWS, self.COLS)
        self.clavier.setDebounceTime(50)

        # LCD
        LCD1602.init(0x27, 1)
        LCD1602.clear()

        # Callbacks boutons
        self.btn_start.when_pressed = self.btn_start_pressed
        self.btn_valid.when_pressed = self.btn_valid_pressed

        # État interne
        self.running = True
        self.last_pir = 0  # timestamp dernière détection PIR (cooldown)

        # Thread lecture PIR et keypad
        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.thread.start()


    # Gestion des Leds

    def set_led(self, actif):
        # Allume la LED verte si actif, rouge sinon
        if actif:
            self.led_verte.on()
            self.led_rouge.off()
        else:
            self.led_verte.off()
            self.led_rouge.on()

    def clignoter_verte(self, fois=3):
        # Fait clignoter la LED verte n fois (accès valide)
        def _blink():
            for _ in range(fois):
                self.led_verte.on()
                time.sleep(0.3)
                self.led_verte.off()
                time.sleep(0.3)
            self.led_verte.on()  # remet verte allumée après clignotement
        threading.Thread(target=_blink, daemon=True).start()

    def clignoter_rouge(self, fois=3):
        # Fait clignoter la LED rouge n fois (accès invalide)
        def _blink():
            for _ in range(fois):
                self.led_rouge.on()
                time.sleep(0.3)
                self.led_rouge.off()
                time.sleep(0.3)
            self.led_rouge.on()  # remet rouge allumée après clignotement
        threading.Thread(target=_blink, daemon=True).start()

    def clignoter_rouge_infini(self):
        # Fait clignoter la LED rouge indéfiniment (accès bloqué)
        def _blink():
            while self.controleur.acces_bloque:
                self.led_rouge.on()
                time.sleep(0.3)
                self.led_rouge.off()
                time.sleep(0.3)
        threading.Thread(target=_blink, daemon=True).start()


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
