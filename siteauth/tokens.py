from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGen(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
            return f'{user.pk}{timestamp}{user.is_active}'

account_activation_token = TokenGen()