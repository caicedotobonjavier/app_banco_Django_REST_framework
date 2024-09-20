#
import random
#
import string

#genero codigo de registro
def create_account(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))