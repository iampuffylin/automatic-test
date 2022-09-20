from time import sleep
import sys
import os
import config

ssh_all = config.ssh_all

def main():
    print('main')

def reboot():
    for s in ssh_all:
        os.system(s + ' \ sudo reboot')
    print('*** Reboot all server done ***')

def clearlog():
    for s in ssh_all:
        os.system(s + ' \ rm irene/test_log/*')
    print('*** Clear Log done ***')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reboot':
        reboot()
    elif len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clearlog()
    else:
        main()