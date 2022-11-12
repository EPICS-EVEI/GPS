from machine import UART, Pin


def initialize_lcd(backlight_red, backlight_green, backlight_blue):
    lcd_uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
    lcd_uart.write('|')  # write 5 bytes
    lcd_uart.write(b'\x18')  # write 5 bytes
    lcd_uart.write(b'\x08')  # contrast
    lcd_uart.write('|')  # Put LCD into setting mode
    lcd_uart.write(b'\x2B')  # Set green backlight amount to 0%
    lcd_uart.write(backlight_red.to_bytes(1, 'big'))  # Set green backlight amount to 0%
    lcd_uart.write(backlight_green.to_bytes(1, 'big'))  # Set green backlight amount to 0%
    lcd_uart.write(backlight_blue.to_bytes(1, 'big'))  # Set green backlight amount to 0%
    lcd_uart.write('|')  # Setting character
    lcd_uart.write('-')  # Clear display
    return lcd_uart

