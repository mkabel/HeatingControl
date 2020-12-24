from cryptography.fernet import Fernet


class Obfuscation:

    def __init__(self):
        return

    def initialise(self):
        self.writekey(self.createkey())
        return

    def encrypt(self, value2encrypt):
        f = Fernet(self.readkey())
        return f.encrypt(str.encode(value2encrypt))

    def decrypt(self, value2decrypt):
        f = Fernet(self.readkey())
        return f.decrypt(value2decrypt).decode()

    def createkey(self):
        return Fernet.generate_key()

    def writekey(self, key):
        file = open('./data/.token', 'wb')
        file.write(key)
        file.close()
        return

    def readkey(self):
        file = open('./data/.token', 'rb')
        key = file.read()
        file.close()
        return key
