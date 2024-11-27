import string

from django.core.exceptions import ValidationError

class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError('password must have lower and upper letter', code='password_no_letters')
    def get_help_text(self):
        return 'password must have lower and upper letter'
class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError('password must have number', code='password_no_number')
    def get_help_text(self):
        return 'password must have number'

class ContainsSpecialCharacterValidator:
    def validate(self, password, user=None):
        special_characters = string.punctuation  # Liste des caractères spéciaux
        if not any(char in special_characters for char in password):
            raise ValidationError('password must have special char', code='password_no_special_char')

    def get_help_text(self):
        return 'password must have special char'