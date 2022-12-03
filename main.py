import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


user_token = os.environ['TOKEN']
user_input = input("Введите ссылку: ")


def shorten_link(token, url):

    bitly = "https://api-ssl.bitly.com/v4/bitlinks"

    headers = {"Authorization": "Bearer {}".format(token)}
    payload = {"long_url": url}

    testing_url = requests.get(payload['long_url'], headers=headers)
    testing_url.raise_for_status()

    response = requests.post(bitly, headers=headers, json=payload)
    response.raise_for_status()

    bitlink = response.json()['link']
    return bitlink


def clicks_count(token, bitlink):

    headers = {"Authorization": "Bearer {}".format(token)}
    payload = {"long_url": bitlink}

    testing_url = requests.get(payload['long_url'], headers=headers)
    testing_url.raise_for_status()

    parsed = urlparse(bitlink)
    bitlink_short = parsed.hostname + parsed.path

    total_clicks_url = "https://api-ssl.bitly.com/v4/bitlinks/" + \
        f"{bitlink_short}/clicks/summary"

    response = requests.get(total_clicks_url, headers=headers)
    response.raise_for_status()

    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(url):

    parsed = urlparse(url)

    if parsed.hostname == "bit.ly":
        return True
    else:
        return False


if __name__ == '__main__':

    if is_bitlink(user_input):
        try:
            total_clicks = clicks_count(user_token, user_input)
            print("По вашей ссылке прошли: {} раз(а)".format(total_clicks))
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.MissingSchema,
                requests.exceptions.InvalidURL) as error:
            print("Can't get data from server.\nFor {0} is:\n{1}\n"
                  .format(user_input, error))
    else:
        try:
            bitlink = shorten_link(user_token, user_input)
            print("Битлинк: {}".format(bitlink))
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.MissingSchema,
                requests.exceptions.InvalidURL) as error:
            print("Can't get data from server.\nFor {0} is:\n{1}\n"
                  .format(user_input, error))
