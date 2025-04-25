import board
import digitalio
import time
import adafruit_character_lcd.character_lcd as character_lcd

lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D22)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_backlight = digitalio.DigitalInOut(board.D4)

lcd_rs.direction = digitalio.Direction.OUTPUT
lcd_en.direction = digitalio.Direction.OUTPUT
lcd_d7.direction = digitalio.Direction.OUTPUT
lcd_d6.direction = digitalio.Direction.OUTPUT
lcd_d5.direction = digitalio.Direction.OUTPUT
lcd_d4.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.D26)
led.direction = digitalio.Direction.OUTPUT

# lcd_rs        = 25 
# lcd_en        = 24
# lcd_d4        = 23
# lcd_d5        = 17
# lcd_d6        = 18
# lcd_d7        = 22
# lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.message = "Hello\nCircuitPython"

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)