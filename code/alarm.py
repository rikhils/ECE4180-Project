import lcd
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

# --- LCD Setup ---
lcd.lcd_init()
lcd.lcd_clear()

# --- Buzzer Setup (GPIO 23) ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer_pin = 21
GPIO.setup(buzzer_pin, GPIO.OUT)

# --- Alarm Clock Loop ---
last_minute = -1

try:
    while True:
        now = datetime.now()
        date_str = now.strftime("%b %d %Y")
        time_str = now.strftime("%H:%M:%S")

        # Update LCD
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(date_str.center(16), 2)

        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string(time_str.center(16), 2)

        # Beep at the start of each new minute
        if now.minute != last_minute:
            last_minute = now.minute
            GPIO.output(buzzer_pin, GPIO.HIGH)
            sleep(1)
            GPIO.output(buzzer_pin, GPIO.LOW)

        sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.cleanup()
    lcd.GPIO.cleanup()
