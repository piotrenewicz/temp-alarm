import inveo_get
import mail_sending
from parse_input import get_split_input


def main():
    sensors, mail_list = get_split_input()
    for sensor in sensors:
        name, ip, min_temp, max_temp = sensor["name"], sensor["ip"], float(
            sensor["min"]), float(sensor["max"])
        current_temp = inveo_get.get_data(ip)

        if min_temp <= current_temp <= max_temp:
            return
        else:
            # HERE HANDLE ALARM TRIGGERING
            pass


if __name__ == "__main__":
    main()
