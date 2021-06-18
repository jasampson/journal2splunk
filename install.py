#!/usr/bin/env python3

import os
import shutil
from getpass import getuser


def main():
    """
    This script installs journal2splunk on Ubuntu systems.  has not been tested on other distros.
    """
    # service account user
    service_account = 'j2splunk'

    # make sure we're root
    if getuser() != 'root':
        raise RuntimeError('You must run this script as root.')

    # create j2splunk user if needed
    with open('/etc/passwd', 'r') as passwd:
        passwd = passwd.readlines()
    if service_account not in [x.split(':')[0] for x in passwd]:
        print('Creating user ' + service_account)
        os.system('useradd -d /nonexistent -s /bin/false -M -G systemd-journal ' + service_account)
        os.system('passwd -l ' + service_account)

    # copy files to appropriate places
    print('Copying service files')
    shutil.copyfile('journal2splunk.conf', '/etc/journal2splunk.conf')
    shutil.copyfile('journal2splunk', '/usr/bin/journal2splunk')
    shutil.copymode('journal2splunk', '/usr/bin/journal2splunk')
    shutil.copyfile('journal2splunk.service', '/etc/systemd/system/journal2splunk.service')

    # enable and start service
    print('Enabling and starting journal2splunk service.')
    os.system('systemctl enable journal2splunk.service')
    os.system('systemctl start journal2splunk.service')


if __name__ == "__main__":
    main()
