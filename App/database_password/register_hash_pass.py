import hashlib
import uuid


class RegPass:

    @staticmethod
    def reg():
        password = input("enter pass: ")
        password = password.encode()

        salt = uuid.uuid4().hex.encode()
        hash_password = hashlib.sha512(password + salt).hexdigest()
        return [hash_password, salt]




