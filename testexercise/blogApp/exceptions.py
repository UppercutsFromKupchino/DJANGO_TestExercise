"""
ValidationError - класс, осуществляющий проверку пароля на минимальную длину 8 символов, наличие хотя бы
одного символа верхнего и нижнего регистра.
"""
import re


class ValidationError:

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

    @staticmethod
    def validate(pattern, password):
        if re.match(pattern, password) is None:
            return True
        else:
            pass
