#! /bin/bash

TARGET=$1

sudo lxc-create -n $TARGET -t debian -- -r sid
sudo lxc-start -d -n $TARGET
sudo lxc-attach -n $ -- apt-get install -y python git vim sudo
sudo lxc-attach -n $ -- sed -i 's|ALL=(ALL:ALL) ALL|ALL=(ALL:ALL) NOPASSWD:ALL|' /etc/sudoers
PASSWD=$(pwgen 42 1)
SALT=$(pwgen 2 1)
CRYPTED=$(perl -e "print crypt(\"$PASSWD\", \"$SALT\"),\"\n\"")
sudo lxc-attach -n $TARGET -- useradd -U -G sudo -p $CRYPTED -m -s /bin/bash $USER
echo "Please run ssh-copy-id $USER@$TARGET and log in with $PASSWD before using ansible"
