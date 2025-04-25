import lcd
import time
from datetime import datetime

lcd.lcd_init()
lcd.lcd_clear()

try:
    while True:
        now = datetime.now()
        # lcd.lcd_clear()
        date_str = now.strftime("%b %d %Y")     # e.g. "Apr 20 2025"
        time_str = now.strftime("%H:%M:%S")     # e.g. "14:53:01"

        # Display date on line 1
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(date_str.center(16), 2)

        # Display time on line 2
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string(time_str.center(16), 2)

        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    lcd.GPIO.cleanup()
