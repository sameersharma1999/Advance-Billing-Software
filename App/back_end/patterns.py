import re


class Patt:
    global g_patt
    @staticmethod
    def v_gstin(e):
        if e == '' or e == " ":
            return 'empty'
        pattern = re.compile("^([0][1-9]|[1-2][0-9]|[3][0-5])([a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}[1-9a-zA-Z]{1}[zZ]{1}[0-9a-zA-Z]{1})+$")
        if re.search(pattern, e):
            return 1
        else:
            return 0

    @staticmethod
    def v_phone(e):
        if e == '' or e == " ":
            return 'empty'
        pattern = re.compile('[9876]\d{9}')
        if re.search(pattern, e):
            return 1
        else:
            return 0

    @staticmethod
    def v_pan(e):
        if e == '' or e == " ":
            return 'empty'
        pattern = re.compile('^[A-Z]{5}[0-9]{4}[A-Z]{1}')
        if re.search(pattern, e) or e == '':
            return 1
        else:
            return 0

    @staticmethod
    def v_addhar(e):
        if e == '' or e == " ":
            return 'empty'
        pattern = re.compile('^\d{4}\s\d{4}\s\d{4}$')
        if re.search(pattern, e):
            return 1
        else:
            return 0

