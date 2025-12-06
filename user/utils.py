import random
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk)+text_type(timestamp)+text_type(user.is_active)
        )
        
account_activation_token = TokenGenerator()

def generate_otp():
    return str(random.randint(100000, 999999))