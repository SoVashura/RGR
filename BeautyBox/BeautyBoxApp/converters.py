class FourDigitYearConverter:
    regex = "[0-9]{4}"
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return "%04d" % value

class SlugConverter:
    regex = '[-a-zA-Z0-9_]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
