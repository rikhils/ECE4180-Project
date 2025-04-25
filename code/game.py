import RPi.GPIO as GPIO
import time
import random
import lcd
import threading

# GPIO pins
BUZZER_PIN = 21
SHORT_BTN = 26
LONG_BTN = 19
CLEAR_BTN = 13

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SHORT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LONG_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLEAR_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LCD init
lcd.lcd_init()

# Buzz patterns
def buzz_short():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)

def buzz_long():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.6)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)

def play_pattern_loop(pattern, stop_event):
    while not stop_event.is_set():
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Memorize Pattern", 2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string("                ", 2)
        for symbol in pattern:
            if stop_event.is_set():
                return
            if symbol == '.':
                buzz_short()
            else:
                buzz_long()
            time.sleep(0.3)
        time.sleep(2)  # Wait before replaying the pattern

def display_input(user_input):
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Your Input:", 2)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string(' '.join(user_input).ljust(16), 2)

def display_result(success):
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    if success:
        lcd.lcd_string("Correct!        ", 2)
    else:
        lcd.lcd_string("Wrong! Try Again", 2)
    time.sleep(2)

try:
    while True:
        # Generate random pattern
        pattern = [random.choice(['.', '-']) for _ in range(6)]
        print("Pattern:", ''.join(pattern))  # Debug

        # Start pattern playback in background
        stop_event = threading.Event()
        pattern_thread = threading.Thread(target=play_pattern_loop, args=(pattern, stop_event))
        pattern_thread.start()

        # Input handling
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

            # Check if full sequence entered
            if len(user_input) == 6:
                if user_input == pattern:
                    stop_event.set()
                    pattern_thread.join()
                    display_result(True)
                    break
                else:
                    user_input = []
                    display_result(False)
                    display_input(user_input)

        # Ready for next round
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Press any button", 2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string("to play again    ", 2)
        while GPIO.input(SHORT_BTN) == GPIO.LOW and GPIO.input(LONG_BTN) == GPIO.LOW:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting game...")

finally:
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Goodbye!        ", 2)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string("                ", 2)
    GPIO.cleanup()
