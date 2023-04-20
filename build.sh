#!/usr/bin/env bash
# exit on error
set -o errexit

# create temporary directory for apt
mkdir -p /tmp/lists/partial
mkdir -p /var/lib/apt/lists/partial
mount --bind /tmp/lists/partial /var/lib/apt/lists/partial

# install dependencies
apt-get update
apt-get install -y wget unzip libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

# download and install ChromeDriver
wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/local/bin/

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# unmount temporary directory
umount /var/lib/apt/lists/partial
rm -rf /tmp/lists
