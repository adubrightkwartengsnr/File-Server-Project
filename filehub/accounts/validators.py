import re
from django.core.exceptions import ValidationError
        
class SpecialCharacterValidator(object):
    def validate(self,password,user=None):
         if not re.findall('[()[\]{\}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                message=("The password must contain at least 1 special character: " +
                  "()[]{\}|`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return(
            "Your password must contain at least 1 special character: " +
            "()[]{\}|`~!@#$%^&*_-+=;:'\",<>./?"
        )     