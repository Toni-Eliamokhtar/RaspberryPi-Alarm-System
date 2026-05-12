import RPi.GPIO as GPIO
import time
import threading

# ================= CONFIG =================
LED_ROUGE = 21
LED_VERTE = 20

BTN_START = 23
BTN_VALID = 26

PIR = 18
BUZZER = 19

# ================= INIT =================
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_ROUGE, GPIO.OUT)
GPIO.setup(LED_VERTE, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.setup(BTN_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_VALID, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ================= VARIABLES =================
systeme_actif = False
running = True

# ================= FONCTIONS =================


def bip(duration=0.2):
    GPIO.output(BUZZER, 1)
    time.sleep(duration)
    GPIO.output(BUZZER, 0)


def detection_valide():
    count = 0
    for _ in range(5):
        if GPIO.input(PIR) == 1:
            count += 1
        time.sleep(0.05)
    return count >= 3


# ================= THREAD PIR =================


def thread_pir():
    global systeme_actif

    print("Initialisation PIR... (attends 30 sec)")
    time.sleep(30)

    while running:
        if systeme_actif and detection_valide():
            print("MOUVEMENT DETECTÉ (valide)")
            bip(0.5)
            time.sleep(1)

        time.sleep(0.1)


# ================= MAIN LOOP =================


def main():
    global systeme_actif

    t = threading.Thread(target=thread_pir)
    t.start()

    try:
        while True:

            # === bouton START ===
            if GPIO.input(BTN_START) == 0:
                systeme_actif = not systeme_actif
                print("SYSTEME:", "ACTIF" if systeme_actif else "OFF")
                time.sleep(0.3)

            # === LEDs ===
            if systeme_actif:
                GPIO.output(LED_VERTE, 1)
                GPIO.output(LED_ROUGE, 0)
            else:
                GPIO.output(LED_VERTE, 0)
                GPIO.output(LED_ROUGE, 1)

            # === bouton validation ===
            if GPIO.input(BTN_VALID) == 0:
                print("VALIDATION")
                bip(0.1)
                time.sleep(0.3)

            time.sleep(0.1)

    except KeyboardInterrupt:
        global running
        running = False
        t.join()
        GPIO.cleanup()


# ================= RUN =================
if __name__ == "__main__":
    main()
