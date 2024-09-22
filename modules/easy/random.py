import random, bcrypt


class Randomizer:
    @staticmethod
    def randint(start, finish):
        return random.randint(start, finish)
    
class Hasher:
    @staticmethod
    def hash(string):
        return bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt())
    
    @staticmethod
    def check(string1, string2):
        return bcrypt.checkpw(string1, string2)