from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

def uid_generate(user):
    return urlsafe_base64_encode(force_bytes(user.username))

def uid_decode(uidb64):
    return force_text(urlsafe_base64_decode(uidb64))

def token_generate(user):
    newGenerate = PasswordResetTokenGenerator()
    return newGenerate.make_token(user)

def token_check(user, token):
    newGenerate = PasswordResetTokenGenerator()
    return newGenerate.check_token(user, token)



