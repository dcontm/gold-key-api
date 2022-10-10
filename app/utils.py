from random import randint

def gen_password(size=6):
    password = ''.join([str(randint(0,9)) for i in range(size)])
    return password

