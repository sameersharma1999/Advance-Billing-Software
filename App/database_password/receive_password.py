import hashlib
from App.database_password.db_changes import MakeChanges


class ValPass:
    @staticmethod
    def receive(get):         # get = password
        re = MakeChanges.retrive()

        remake_hash = hashlib.sha512(get.encode() + re[1]).hexdigest()

        if re[0] == bytearray(remake_hash.encode()):
            return 1
        else:
            return 0



