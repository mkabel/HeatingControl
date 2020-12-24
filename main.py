import logging
import argparse
import pickle
from obfuscation import Obfuscation
from tadoHelper import TadoHelper

logging.basicConfig(filename='log/tado.log', format='%(asctime)s - %(message)s', level=logging.INFO)
_LOG_ = logging.getLogger(__name__)


def save_settings(content):
    file_handler = open('./data/settings', 'wb')
    pickle.dump(content, file_handler)
    file_handler.close()


def load_settings():
    file_handler = open('./data/settings', 'rb')
    content = pickle.load(file_handler)
    file_handler.close()
    return content


def encrypt_settings(email, pwd):
    Obfuscation().initialise()
    settings = {
        'email': Obfuscation().encrypt(email),
        'pwd': Obfuscation().encrypt(pwd)
    }
    return settings


def decrypt_settings(content):
    settings = {
        'email': Obfuscation().decrypt(content['email']),
        'pwd': Obfuscation().decrypt(content['pwd'])
    }
    return settings


def main():
    parser = argparse.ArgumentParser(description="Tado Assistant")
    parser.add_argument("-c", "--configure", action="store_true", help="Configure account settings")
    parser.add_argument("--email", help="Tado user id", default="user_id")
    parser.add_argument("--pwd", help="Tado password", default="password")
    parser.add_argument("--overlay", help="Configure overlay", default="reset")
    parser.add_argument("--temp", help="Set temperature", default="14")
    parser.add_argument("--zone", help="Set zone", default="Woonkamer")
    args = parser.parse_args()

    if args.configure:
        save_settings(encrypt_settings(args.email, args.pwd))
        print('Account settings configure')
        return

    settings = decrypt_settings(load_settings())
    my_tado = TadoHelper(settings['email'], settings['pwd'])

    if args.overlay == "reset":
        my_tado.resetOverlay(args.zone)
        return

    if args.overlay == "manual":
        my_tado.setOverlay(args.zone, args.temp)
        return

    print('No overlay action configured')
    return


if __name__ == '__main__':
    main()


