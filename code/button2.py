import RPi.GPIO as GPIO
import time

BUZZER_PIN = 21
BUTTON_PIN = 19	

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def buzz(channel):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.2)  # Buzz for 0.2 seconds
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=buzz, bouncetime=200)

print("Waiting for button press... Press CTRL+C to exit.")

try:
    while True:
        time.sleep(0.1)  # Let the CPU chill

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()