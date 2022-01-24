import os
import signal
import threading
import time

import protocol_dock as proto
import mail_sending
from parse_input import get_input

def main():
    # init
    try:
        glob = get_input()
    except FileNotFoundError:
        print("Configuration file missing!")
        exit()
    print("Config loaded")

    deadzone = 3
    thread_pid_table = dict()
    sensors = glob["sensors"]
    cooldown = glob["check_cooldown"]
    sender = mail_sending.get_auto_sender(glob["send_alarm_to_mails"])
    timeout = glob["sensor_timeout"]
    sensor_count = len(sensors)
    alarms = [[False, False, False] for i in range(sensor_count)]
    #           low , high , timeout.

    def check_sensor(sensor_idx):
        thread_pid_table[sensor_idx] = os.getpid()
        sensor = sensors[sensor_idx]
        alarm_flags = alarms[sensor_idx]

        name, ip, min_temp, max_temp, protocol = sensor["name"], sensor["ip"], \
            float(sensor["min"]), float(sensor["max"]), sensor["protocol"]

        current_temp = proto.dock[protocol].get_data(ip)  # if sensor doesn't respond this thread will be killed here

        if alarm_flags[2]:
            # since we got here we know that the sensor has responded
            alarm_flags[2] = False
            # this sensor was unreachable previously, send e-mail about it coming back online
            sender(sensor, 2, 0)

        # print(current_temp)

        if alarm_flags[0]:
            if current_temp >= min_temp + deadzone:
                # Release low temp alarm
                alarm_flags[0] = False
                # Send mail no longer temp low.
                sender(sensor, 3, current_temp)
        else:
            if current_temp <= min_temp:
                # Begin low temp alarm
                alarm_flags[0] = True
                # Send email temp low.
                sender(sensor, 0, current_temp)

        if alarm_flags[1]:
            if current_temp <= max_temp - deadzone:
                # Release high temp alarm
                alarm_flags[1] = False
                # Send mail no longer temp high.
                sender(sensor, 4, current_temp)
        else:
            if current_temp >= max_temp:
                # Begin high temp alarm
                alarm_flags[1] = True
                # Send email temp high.
                sender(sensor, 1, current_temp)

    # begin looping
    running = True
    print("starting monitoring")
    while running:
        time.sleep(cooldown)
        threads = []
        for sensor_idx in range(sensor_count):
            t = threading.Thread(target=check_sensor, args=(sensor_idx,))
            t.daemon = True
            t.start()
            threads.append(t)

        time.sleep(timeout)
        if timeout == 0:
            continue

        for idx, thread in enumerate(threads):  # if we have unresponding sensors, give up waiting,
            if thread.is_alive():
                alarms[idx][2] = True
                #os.kill(thread_pid_table[idx], signal.SIGKILL)
                # send e-mail about losing access to sensors[idx]
                sender(sensors[idx], 2, 1)








if __name__ == "__main__":
    main()
