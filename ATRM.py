import threading
import random

HOURS = 5
temperature_readings = [[] for _ in range(8)]
lock = threading.Lock()
hour_counter = 0

# Simulate temperature reading from a sensor
def sensor_thread(sensor_id):
    minute_count = 0
    while minute_count < HOURS * 60:
        temperature = random.uniform(-100, 70)
        with lock:
            temperature_readings[sensor_id].append(temperature)
        minute_count += 1

# Function to compile report
def report_thread():
    global hour_counter
    while hour_counter < HOURS:
        checker = 0
        for i in range(8):
            if len(temperature_readings[i]) >= (60 * hour_counter + 60):
                checker += 1
        if checker == 8:
            all_readings = []
            with lock:
                all_readings = [reading for sensor_readings in temperature_readings for reading in sensor_readings[60 * hour_counter:60 * hour_counter + 60]]
            sorted_readings = sorted(all_readings)
            top_5_highest = sorted_readings[-5:]
            top_5_lowest = sorted_readings[:5]
            max_difference = 0
            max_difference_interval = []
            for i in range(len(all_readings) - 10):
                difference = max(all_readings[i:i+10]) - min(all_readings[i:i+10])
                if difference > max_difference:
                    max_difference = difference
                    max_difference_interval = all_readings[i:i+10]
                    
            print("Hour", (hour_counter+1), "Report:")
            print("Top 5 highest temperatures:")
            for i in range(5):
                print("#" + str(i+1) + " - " + str(top_5_highest[4-i]))
            print("Top 5 lowest temperatures:")
            for i in range(5):
                print("#" + str(i+1) + " - " + str(top_5_lowest[i]))
            print("10-minute interval with the largest temperature difference:")
            for i in range(10):
                print("#" + str(i+1) + " - " + str(max_difference_interval[i]))
            
            hour_counter += 1

def main():
    sensor_threads = []
    for i in range(8):
        thr = threading.Thread(target=sensor_thread, args=(i,))
        thr.start()
        sensor_threads.append(thr)

    report_thr = threading.Thread(target=report_thread)
    report_thr.start()

    report_thr.join()

main()
