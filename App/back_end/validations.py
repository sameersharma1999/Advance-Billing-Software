from App.back_end.patterns import Patt


class Validate:
    def __init__(self):
        pass

    @staticmethod
    def basic_check(temp):
        k = []
        k.clear()
        for i in temp:
            k.append(i)
        if all(k) is "":
            return 'al'
        elif k[0] == "" or k[0] == " ":
            return 'fi'
        elif k[1] == "" or k[1] == " ":
            return 'la'
        elif k[2] == "" or k[2] == " ":
            return 'ad'
        elif k[3] == "" or k[3] == " ":
            return 'st'
        elif k[4] == "" or k[4] == " ":
            return 'ci'
        else:
            return -1

    @staticmethod
    def check(d):
        get_result = []
        app_keys = []
        app_keys.clear()
        get_result.clear()
        for k in d.values():
            app_keys.append(k)

        get_gst = Patt.v_gstin(app_keys[5].strip())
        get_result.append(get_gst)
        get_pan = Patt.v_pan(app_keys[7].strip())
        get_result.append(get_pan)
        get_addhar = Patt.v_addhar(app_keys[6].strip())
        get_result.append(get_addhar)
        get_phone = Patt.v_phone(app_keys[8].strip())
        get_result.append(get_phone)
        return get_result



