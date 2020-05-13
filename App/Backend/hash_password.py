import hashlib
import uuid
from App.Database.db_changes import UploadRetrievePassword


class Passwords:
    @classmethod  # here we receive hash from database and validate it
    def receive_hash(cls, get):         # get = password
        data = UploadRetrievePassword.retrieve_salt_pass()
        hashed = data[0]  # hash
        salt = data[1]

        remake_hash = hashlib.sha512(get.encode() + salt).hexdigest()

        if hashed == bytearray(remake_hash.encode()):
            return True  # matched
        else:
            return False  # not matched

    @classmethod
    def make_hash_salt(cls, pas):  # encrypt password
        password = pas
        password = password.encode()
        salt = uuid.uuid4().hex.encode()
        hash_password = hashlib.sha512(password + salt).hexdigest()
        return [hash_password, salt]
