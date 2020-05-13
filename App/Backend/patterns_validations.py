import re


class PatternsValidations:
    """Below are all the regular expressions"""
    @classmethod
    def v_gst(cls, e):
        if e == '':
            return True
        pattern = re.compile(
            '^([0][1-9]|[1-2][0-9]|[3][0-5])([a-zA-Z]{5}[0-9]{4}[a-zA-Z][1-9a-zA-Z][zZ][0-9a-zA-Z])+$')
        if re.search(pattern, e):
            return True
        else:
            return False

    @classmethod
    def v_phone(cls, e):
        if e == '':
            return True
        pattern = re.compile('[9876]\d{9}')
        if re.search(pattern, e):
            return True
        else:
            return False

    @classmethod
    def v_pan(cls, e):
        if e == '':
            return True
        pattern = re.compile('^[A-Z]{5}[0-9]{4}[A-Z]')
        if re.search(pattern, e) or e == '':
            return True
        else:
            return False

    @classmethod
    def v_addhar(cls, e):
        if e == '':
            return True
        pattern = re.compile('^\d{4}\s\d{4}\s\d{4}$')
        if re.search(pattern, e):
            return True
        else:
            return False

    """Here we validate the expressions"""
    @classmethod
    def validate(cls, gst, addhar,  ph_no, pan):
        if not cls.v_gst(gst):
            return 'wrong_gst'
        elif not cls.v_addhar(addhar):
            return 'wrong_addhar'
        elif not cls.v_phone(ph_no):
            return 'wrong_phone_no'
        elif not cls.v_pan(pan):
            return 'wrong_pan'
        else:
            return 'Right'
