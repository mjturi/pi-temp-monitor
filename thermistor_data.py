# This will read data from the ADS1115. This happens particularly with the 
# thermistor and by using a 330 Ohm resistor. The thermistro uses 3.3V,
# which uses a gain of 2 for the ADC.
import time
import numpy as np
import Adafruit_ADS1x15 # Imports the ADS1x15 module.
from twilio.rest import Client

adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance.
client = Client('AC448d1d3c1e315da5d4051479b0dab638', 'e7f8941327aa81310f21635650c5ea66')

# send the thermistor data through twilio api to user mobile
def send_therm_data(curr_temp, priority=False):
    # if the temp is out of user temp bounds, send an alert, otherwise send a normal message
    if (priority):
        client.api.account.messages.create(to='+19492357651', from_='+14159150063', body='ALERT:\nCurr temp is : ' + str(curr_temp) + '. Please check on your monitored area.')
    else:
        client.api.account.messages.create(to='+19492357651', from_='+14159150063', body='Your current monitored temp is: ' + str(curr_temp))
    
# Gets thermistor data in terms of sensed voltage
def get_therm_data():
    GAIN = 2
    value = adc.read_adc(0, gain=GAIN) # reads values only from ADS1115 channel 0
    
    # 3.3 is the input voltage for the thermistor
    # 65536 is 2^16 for the ADS1115 16-bit ADC

    VSense = (3.3/65536) * value # VSense is the Voltage seen by the ADC
    
    if VSense == 0: # To not divide by 0
        VSense = 1
    
    Resistance = 330 * (3.3 - VSense)/VSense # Resistance of thermistor
    
    if Resistance < 611:
        Temp = -0.9817224399*Resistance + 133.08
    elif Resistance < 987:
        Temp = -0.04576406337*Resistance + 101.03
    else:
        Temp = -0.02784125549*Resistance + 83.33
    
    TempF = 1.8*Temp + 32 # Converts to Fahrenheit
    
    return TempF

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gin to change the range of voltages that are read:
# - 2/3 = +/-6.144V
# -   1 = +/-4.096V
# -   2 = +/-2.048V
# -   4 = +/-1.024V
# -   8 = +/-0.512V
# -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        