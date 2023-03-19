import math
air_temperature = 13  # Celsius
humidity = 71    # Percentage
atm_pressure = 1017.7 # hPa
alpha = 17.27
beta = 237.7
gamma = ((alpha * air_temperature) / (beta + air_temperature)) + math.log(humidity/100.0)
es = 6.112 * math.exp(gamma) * (atm_pressure/1013.25)**(1.0 - 0.00075 * air_temperature)
gamma_dp = math.log(es/6.112)
dew_point = (beta * gamma_dp) / (alpha - gamma_dp)
print("Dew Point Temperature: {:.2f} C".format(dew_point))