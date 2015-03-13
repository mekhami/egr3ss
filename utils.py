
WARN = '\033[93m\033[1m[!] \033[0m'
GOOD = '\033[92m\033[1m[+] \033[0m'
INFO = '\033[94m\033[1m[*] \033[0m'

FORMAT_STRING = "{0} [" + time.strftime("%x") + " - " + time.strftime("%X") + "] {1}"

def info(message):
    print FORMAT_STRING.format(INFO, message)

def warn(message):
    print FORMAT_STRING.format(WARN, message)

def good(message):
    print FORMAT_STRING.format(GOOD, message)

