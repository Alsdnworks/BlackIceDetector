def read_data():
    import machine
    import time
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

    data = i2c.readfrom(0x08, 4)
    return str(data)
    
