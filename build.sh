#!/usr/bin/env bash
# exit on error
set -o errexit

# create temporary directory to avoid permission issues
mkdir /tmp/apt && mkdir /tmp/apt/lists && mkdir /tmp/apt/archives && mkdir /tmp/apt/partial

# update and install packages
apt-get update -o Dir::Etc::sourcelist=/dev/null \
-o Dir::Etc::sourceparts=/tmp/apt/lists \
-o APT::Get::List-Cleanup='false'
apt-get install -y wget unzip libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

# download and install ChromeDriver
wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/local/bin/

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
