import requests


def get_data(ip: str):
    url = "https://{0}/temp1.txt".format(ip)
    response = requests.request("GET", url)
    return float(response.text)
