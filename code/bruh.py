import RPi.GPIO as GPIO
import time
import random
import threading
from datetime import datetime
import lcd

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pins
BUZZER_PIN = 21
SHORT_BTN = 26
LONG_BTN = 19
CLEAR_BTN = 13

# Setup GPIO
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SHORT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LONG_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLEAR_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# LCD Setup
lcd.lcd_init()
time.sleep(0.1)
lcd.lcd_clear()


# Buzzer Patterns
def buzz_short():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)

def buzz_long():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)

def play_pattern_loop(pattern, stop_event):
        for symbol in pattern:
            if stop_event.is_set():
                return
            buzz_short() if symbol == '.' else buzz_long()
            time.sleep(0.3)
        time.sleep(2)

def display_input(user_input):
    lcd.lcd_clear()
    time.sleep(0.1)
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Your Input:", 2)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string(' '.join(user_input).ljust(16), 2)


def run_alarm_game():
    pattern = [random.choice(['.', '-']) for _ in range(5)]
    print("Alarm Pattern:", ''.join(pattern))

    stop_event = threading.Event()
    thread = threading.Thread(target=play_pattern_loop, args=(pattern, stop_event))
    thread.start()

    user_input = []
    display_input(user_input)

    while True:
        if GPIO.input(SHORT_BTN) == GPIO.HIGH:
            user_input.append('.')
            display_input(user_input)
            time.sleep(0.3)

        if GPIO.input(LONG_BTN) == GPIO.HIGH:
            user_input.append('-')
            display_input(user_input)
            time.sleep(0.3)

        if GPIO.input(CLEAR_BTN) == GPIO.HIGH:
            user_input = []
            display_input(user_input)
            time.sleep(0.3)

        if len(user_input) == 5:
            if user_input == pattern:
                stop_event.set()
                thread.join()
                break
            else:
                user_input = []
                display_input(user_input)

# Clock Loop
last_minute = -1
try:
    while True:
        now = datetime.now()
        date_str = now.strftime("%b %d %Y")
        time_str = now.strftime("%H:%M:%S")
        
        

        # Show current date/time
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(date_str.center(16), 2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string(time_str.center(16), 2)

        # Trigger alarm at start of new minute
        if now.minute != last_minute:
            last_minute = now.minute
            run_alarm_game()

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.cleanup()
    lcd.GPIO.cleanup()
