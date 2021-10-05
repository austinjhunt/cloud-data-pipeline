#!/bin/bash

# Provision new local VM with necessary installations

# Install Ansible
# https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04

apt update
apt upgrade -y
apt install -y ansible



# Install Python requirements for the project (stored in /vagrant/ )
https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server
apt install -y python3-pip
apt install -y build-essential libssl-dev libffi-dev python3-dev
apt install -y python3-venv
pip install -r /vagrant/requirements.txt