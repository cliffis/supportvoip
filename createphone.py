import paramiko
from config import *
from pg_db import *

def create_mac(model, mac, number, tabnumber):
    print({model}, {mac}, {number}, {tabnumber})
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    # read the BASH script content from the file
    bash_script = ("/bin/bash /home/my/phone_config/T23G/create_conf_test")
    stdin, stdout, stderr = client.exec_command(bash_script + "\x20" + mac + "\x20" + number + "\x20" + tabnumber)
    # data = stdout.read() + stderr.read()
    # print(data)
    for line in stdout:
        print('... ' + line.strip('\n'))
    # print errors if there are any
    err = stderr.read().decode()
    if err:
        print(err)
    client.close()
    insert_log_phone(model, mac, number, tabnumber)
    return


# create_mac(model="SIP-21", mac="12:23:34:rt:yu:io", number="12345", tabnumber="1234567890")