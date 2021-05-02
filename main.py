from thermistor_data import * 
import time

if __name__ == '__main__':
    # take user input highs and lows for temperature monitoring
    high = float(input('Enter the max temperature you will allow: '))
    low = float(input('Enter the min temperature you will allow: '))
    # get a start time to send periodic notifcations regardless
    start_time = time.time()
    while True:
        # get temp every loop iteration
        curr_temp = get_therm_data()
        # check if it is within bounds for user high and low
        if (curr_temp >= high + 1 or curr_temp <= low - 1): 
            send_therm_data(curr_temp, True)
        # check if enough time has passed if the temp is okay
        elif (time.time() - start_time >= 600):
            send_therm_data(curr_temp)
            start_time = time.time()
        time.sleep(60)