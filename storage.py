import time
import threading
import uuid
from abc import ABC, abstractmethod
from cryptography.fernet import Fernet


class StorageAbstract(ABC):
    @abstractmethod
    def save(self, password: str, key: str = None):
        # save password
        ...

    @abstractmethod
    def get(self, key: str) -> str:
        # get password
        ...


class Storage(StorageAbstract):
    """
    Thread-safe password storage. Designed to securely transfer passwords to users.
    Passwords are stored encrypted.
    Use the save() method to save the password, and the get() method to extract.

    Example:
        storage = Storage()
        password = "Password1234"
        public_key, private_key = storage.save(password, 86400)
        original_password = storage.get(public_key, private_key)
        print(original_password)

    """

    def __init__(self):
        self.__passwords = {}
        self._lock = threading.Lock()
        threading.Thread(target=self._cleaning_by_timeout, daemon=True).start()

    @staticmethod
    def _sync_threads(func):
        # A decorator for working in different threads with a single instance of the class

        def wrapper(*args, **kwargs):
            self = args[0]
            with self._lock:
                return func(*args, **kwargs)

        return wrapper

    def _cleaning_by_timeout(self):
        while True:
            with self._lock:
                cleaning = [key for key in self.__passwords if time.time() >= self.__passwords[key]['timeout']]
                for pub_key in cleaning:
                    self.__passwords.pop(pub_key)
            time.sleep(1)

    def _generate_public_key(self):
        public_key = str(uuid.uuid4())
        for _ in range(20):
            if public_key not in self.__passwords:
                return public_key
        else:
            IndexError("Failed to generate index")

    @_sync_threads
    def save(self, password: str, timeout_second: int, public_key: str = None) -> tuple:
        """
        :param password: password to save
        :param timeout_second: the time in seconds after which the password will be deleted
        :param public_key: a unique public key, if None will be generated automatically
        :return: (public_key, private_key), private_key - the key that decrypts the password
        """

        assert isinstance(timeout_second, int), "timeout_second must be int"
        assert isinstance(password, str), "password must be str"

        if public_key:
            assert isinstance(public_key, str), "public_key must be str"
            if public_key in self.__passwords:
                raise KeyError("public_key already exists")
        else:
            public_key = self._generate_public_key()

        password = password.encode()
        cipher_key = Fernet.generate_key()
        cipher = Fernet(key=cipher_key)
        cipher_password = cipher.encrypt(password)

        self.__passwords[public_key] = {"password": cipher_password, "timeout": timeout_second + time.time()}
        return public_key, cipher_key.decode()

    @_sync_threads
    def get(self, public_key: str, private_key: str) -> str:
        """
        :param public_key: the key returned in the save method
        :param private_key: the key returned in the save method
        :return: password
        """

        assert isinstance(private_key, str), "private_key must be str"
        if public_key not in self.__passwords:
            raise KeyError("public_key not found")

        cipher_key = private_key.encode()
        cipher = Fernet(key=cipher_key)
        cipher_password = self.__passwords.pop(public_key)['password']

        return cipher.decrypt(cipher_password).decode()