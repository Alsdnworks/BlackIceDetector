#main.py SHOULD IMPORT BY boot.py AFTER INSPECTION
import I2C_BID
import gps_main
import urequests
import json
import random
import gc
from micropython import mem_info

def upload_data_to_firebase(data):
    url = 'https://blcs-368614-default-rtdb.firebaseio.com/BI.json'
    headers = {'Content-Type': 'application/json'}
    gc.collect()
    response = urequests.post(url, headers=headers, data=json.dumps(data))
    return response

def main():
    while True:
        gc.collect()
        print('Garbage collect free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
        print('-----------------------------')
        mem_info()
        print('-----------------------------')
        mem_info(1)
        lat,lon,gp=gps_main.get_gps_data()
        upload_data_to_firebase(str(random.randrange(1,9999999)))
        print('sendcpl')
main()
    #if '1'==I2C_BID.read_data():
    #try:
    #    fb.put(gp,{'LAT':lat, 'LON':lon, 'W_DATA':{'RH':rh, 'TMP':tmp, 'AP':ap}, 'BI': 0},bg=0)
    #except: #as DUMMY
    #    fb.put(gp,"0",bg=0)

