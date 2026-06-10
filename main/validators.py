import re
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class PhoneNumberValidator:
    message = "Номер телефону повинен мати формат: +**(***)***-**-**!"
    code = "phone"
    pattern = r"^\+\d{2}\(\d{3}\)\d{3}-\d{2}-\d{2}$"

    def __init__(self, message=None, code=None, pattern=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if pattern is not None:
            self.pattern = pattern

    def __call__(self, value):
        prog = re.compile(self.pattern)
        result = re.match(prog, value)
        if not result:
            raise ValidationError(
                message=self.message, code=self.code, params={"value": value}
            )

    def __eq__(self, other):
        return (
            isinstance(other, PhoneNumberValidator)
            and (self.message == other.message)
            and (self.code == other.code)
            and (self.pattern == other.pattern)
        )
