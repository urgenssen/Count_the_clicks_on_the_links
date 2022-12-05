import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):

    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"

    headers = {"Authorization": "Bearer {}".format(token)}
    payload = {"long_url": url}

    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()

    bitlink = response.json()["link"]
    return bitlink


def clicks_count(token, bitlink):

    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"

    headers = {"Authorization": "Bearer {}".format(token)}

    no_scheme_bitlink = f"{urlparse(bitlink).hostname}{urlparse(bitlink).path}"

    total_clicks_url = f"{bitly_url}/{no_scheme_bitlink}/clicks/summary"

    response = requests.get(total_clicks_url, headers=headers)
    response.raise_for_status()

    total_clicks = response.json()["total_clicks"]
    return total_clicks


def is_bitlink(token, url):

    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/"
    no_scheme_url = f"{urlparse(url).hostname}{urlparse(url).path}"
    full_checked_url = f"{bitly_url}{no_scheme_url}"

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(full_checked_url, headers=headers)
    return response.ok


if __name__ == "__main__":

    load_dotenv()

    user_token = os.environ["BITLY_TOKEN"]
    user_input = input("Введите ссылку: ")

    if is_bitlink(user_token, user_input):
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
