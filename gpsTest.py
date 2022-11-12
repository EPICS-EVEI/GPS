import time
from machine import UART, Pin
from lcd import initialize_lcd
import time
from polygon import Point, is_within_polygon

def initialize_gps():
    return UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))


def get_latitude(str_array, index):
    latDeg = float(str_array[index][0: 2])
    latMin = float(str_array[index][2: 10]) / 60
    return '%f' % (float(latDeg) + float(latMin))


def get_longitude(str_array, index2):
    longDeg = float(str_array[index2][1: 3])
    longMin = float(str_array[index2][3: 11]) / 60
    return '%f' % (float(longDeg) + float(longMin))


def get_current_location(gps_uart):
    while True:
        while not gps_uart.any():
            pass
        time.sleep_ms(30)
        str_array = gps_uart.readline()
        print(str_array)
        try:
            str_array = str_array.decode("utf-8")
            time.sleep_ms(30)
            str_array = str_array.split(",")
            print(str_array)
        except:
            pass
        
        if str_array[0] is '$GPGLL':
            #print(str_array)
            #str_array = str_array.split(",")
            print("in GPGLL")
            #lcd_uart.write("in GNGLL")
            latitude = get_latitude(str_array, 1)
            longitude = get_longitude(str_array, 3)
            print("in GPGLL2")
            #lcd_uart.write("in GNGLL2")

        elif str_array[0] is '$GPGGA':
            print("in GNPGA")
            #lcd_uart.write("in GNGGA")
            latitude = get_latitude(str_array, 2)
            longitude = get_longitude(str_array, 4)
            print("in GPGGA2")
            return latitude, longitude



if __name__ == '__main__':
    gps_uart = initialize_gps()
    lcd_uart = initialize_lcd(backlight_red=255, backlight_green=1, backlight_blue=255)
    
    lcd_uart.write("Connecting to GPS...")  # For 16x2 LCD
    polygon = [(40.430713, 86.915236),(40.430751, 86.915264),(40.430808, 86.915169),(40.430751, 86.915188)]
    if (is_within_polygon(polygon, (40.43120397177199, -86.91496015156082))):
        print("True")
    else:
        print("False")
    
    print("Hello")
    latitude, longitude = get_current_location(gps_uart)
    print("Hi")


    lcd_uart.write('|')  # Setting character
    lcd_uart.write('-')  # Clear display
    #print(lcd_text)
    time.sleep_ms(15)
    lcd_uart.write("     EPICS EVEI     ")  # For 16x2 LCD

    time.sleep_ms(15)
    lcd_uart.write("Current Location:   ")  # For 16x2 LCD
    time.sleep_ms(15)
    lcd_uart.write(latitude + " N   ")  # For 16x2 LCD
    time.sleep_ms(15)
    lcd_uart.write(longitude + " W   ")  # For 16x2 LCD
    time.sleep_ms(15)


    if is_within_polygon(polygon, Point(float(latitude), float(longitude))) is True:
        lcd_uart.write(" IN")  # For 16x2 LCD
        print("IN")
    else:
        lcd_uart.write("OUT")  # For 16x2 LCD
    print("OUT")


    while True:
        time.sleep_ms(300)
        latitude, longitude = get_current_location(gps_uart)
    # print(lcd_text)
        lcd_uart.write("     EPICS EVEI  ")  # For 16x2 LCD
        time.sleep_ms(15)
        if is_within_polygon(polygon, Point(float(latitude), float(longitude))) is True:
            lcd_uart.write(" IN")  # For 16x2 LCD
        else:
            lcd_uart.write("OUT")  # For 16x2 LCD
        time.sleep_ms(15)
        lcd_uart.write("Current Location:   ")  # For 16x2 LCD
        time.sleep_ms(15)
        lcd_uart.write("Lat:  " + latitude + " N   ")  # For 16x2 LCD
        time.sleep_ms(15)
        lcd_uart.write("Long: " + longitude + " W   ")  # For 16x2 LCD
        time.sleep_ms(15)
    
    lcd_uart.write("Before getlocation4")
    while True:
        while not gps_uart.any():
            pass
        time.sleep_ms(30)
        str_array = gps_uart.readline()
        print(str_array)
    #latitude, longitude = get_current_location(gps_uart)
    lcd_uart.write("After getlocation2")
    #print(latitude, longitude)
    print("returned")


