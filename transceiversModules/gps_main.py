import gc
from machine import UART
import utime
def get_gps_data():
    gps_module = UART(2, baudrate=9600)
    buff = bytearray(255)
    timeout = utime.time() + 16 
    fix_status = False
    latitude = ''
    longitude = ''
    satellites = ''
    gps_time = ''
    gps_data=''
    while True:
        buff = str(gps_module.readline('\r\n'))
        parts = buff.split(',')
        if buff is not "None":
            print(buff)
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            gps_time = parts[0][0:2] + parts[0][2:4] + parts[0][4:6]
            print("received GPGGA")
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                raw_as_float = float(parts[2])
                first_digits = int(raw_as_float / 100) 
                next_two_digits = raw_as_float - float(first_digits * 100) 
                converted = float(first_digits + next_two_digits / 60.0)
                converted = '{0:.6f}'.format(converted) 
                latitude = converted
                if (parts[3] == 'S'):
                    latitude = -latitude
                raw_as_float = float(parts[4])
                first_digits = int(raw_as_float / 100) 
                next_two_digits = raw_as_float - float(first_digits * 100) 
                converted = float(first_digits + next_two_digits / 60.0)
                converted = '{0:.6f}'.format(converted) 
                longitude = convert_to_degree(converted)
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                fix_status = False
            break
    if fix_status:
        gps_data = {"la": latitude,"lo": longitude,"gp": gps_time}
    else :
        gps_data = {"la": "","lo": "","gp": ""}
    print('done')
    return(gps_data)
print(get_gps_data())
