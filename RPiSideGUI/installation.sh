#!/bin/bash

# Update and upgrade system packages
sudo apt update
sudo apt upgrade -y

# Install build-essential package
sudo apt install -y build-essential

# Install Rust using rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Rust to the PATH
source $HOME/.cargo/env

# Print Rust version
rustc --version

# Install required system packages for Python cryptography library
sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev 

# Install Python packages
pip3 install cryptography
pip3 install firebase-admin "grpcio <= 1.40.0"
