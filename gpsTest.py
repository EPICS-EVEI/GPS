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

"""
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
"""

def get_current_location(gps_uart):
    latitude_avg = 0
    longitude_avg = 0
    for i in range(0, 10):
        latitude = 0
        longitude = 0
        
        while True:
            while not gps_uart.any():
                pass
            time.sleep_ms(30)
            str_array = gps_uart.readline()
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
                print("in GPGLL2: Latitude: ", latitude + "  Longitude: ", longitude)
                break
                #lcd_uart.write("in GNGLL2")

            elif str_array[0] is '$GPGGA':
                print("in GPGGA")
                #lcd_uart.write("in GNGGA")
                latitude = get_latitude(str_array, 2)
                longitude = get_longitude(str_array, 4)
                print("in GPGGA2: Latitude: ", latitude  + "  Longitude: ", longitude)
                break
            
        latitude_avg = float(latitude_avg) + float(latitude)
        longitude_avg = float(longitude_avg) + float(longitude)
        
    latitude_avg /= 10
    longitude_avg /= 10
    
    return latitude_avg, longitude_avg

if __name__ == '__main__':
    gps_uart = initialize_gps()
    lcd_uart = initialize_lcd(backlight_red=255, backlight_green=1, backlight_blue=255)
    
    lcd_uart.write("Connecting to GPS...")  # For 16x2 LCD
    
    polygon = [
    (40.430713, 86.915236),
    (40.430751, 86.915264),
    (40.430808, 86.915169),
    (40.430751, 86.915188)
    ]
    
    while True:
        time.sleep_ms(300)
        latitude_avg, longitude_avg = get_current_location(gps_uart)
        # print(lcd_text)
        lcd_uart.write("     EPICS EVEI  ")  # For 16x2 LCD
        time.sleep_ms(15)
        print("Latitude: ", str(latitude_avg) + "  Longitude: ", str(longitude_avg))
        if is_within_polygon(polygon, (float(latitude_avg), float(longitude_avg))) is True:
            lcd_uart.write(" IN")  # For 16x2 LCD
        else:
            lcd_uart.write("OUT")  # For 16x2 LCD
        time.sleep_ms(15)
        lcd_uart.write("Current Location:   ")  # For 16x2 LCD
        time.sleep_ms(15)
        lcd_uart.write("Lat:  " + str(latitude_avg) + " N   ")  # For 16x2 LCD
        time.sleep_ms(15)
        lcd_uart.write("Long: " + str(longitude_avg) + " W   ")  # For 16x2 LCD
        time.sleep_ms(15)
        break

 
