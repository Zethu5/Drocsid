import ctypes


class SECItem(ctypes.Structure):
    """struct needed to interact with libnss
    """
    _fields_ = [
        ('type', ctypes.c_uint),
        ('data', ctypes.c_char_p),  # actually: unsigned char *
        ('len', ctypes.c_uint),
    ]

    def decode_data(self):
        _bytes = ctypes.string_at(self.data, self.len)
        return _bytes.decode("utf-8")


class PK11SlotInfo(ctypes.Structure):
    """Opaque structure representing a logical PKCS slot
    """


class NSS3NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class NSS3KeySlotCreationError(Exception):
    def __init__(self, message):
        self.message = message


class MasterPasswordDetected(Exception):
    def __init__(self, message):
        self.message = message