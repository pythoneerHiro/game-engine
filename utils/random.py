import random
import string

randomStringGen = lambda length=6: ''.join(random.choices(string.ascii_letters, k=length))

randomNumGen = lambda range_=(1, 101): random.randint(range_)

randomFloatGen = lambda: random.random()
