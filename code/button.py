import RPi.GPIO as GPIO
import time

# GPIO pin setup
BUZZER_PIN = 21
BUTTON_PINS = [26, 19, 13]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Set button pins as input with internal pull-down resistors
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def buzz(channel):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.2)  # Buzz for 0.2 seconds
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# Add event detection for each button
for pin in BUTTON_PINS:
    GPIO.add_event_detect(pin, GPIO.RISING, callback=buzz, bouncetime=200)

print("Waiting for button press... Press CTRL+C to exit.")

try:
    while True:
        time.sleep(0.1)  # Let the CPU chill

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
