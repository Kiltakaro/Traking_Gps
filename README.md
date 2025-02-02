# Tracking GPS Microservice

This guide will help you set up and configure three virtual machines (VMs) with Ubuntu Server, Docker, and OpenSSH Server. We will create one VM and then clone it to create the other two.

## Summary

This document provides a comprehensive guide to setting up a Tracking GPS Microservice using three Ubuntu Server virtual machines. The guide is divided into several sections:

1. **Prerequisites**: Lists the necessary software and tools required before starting the setup ([see Prerequisites](#1-prerequisites)).
2. **VM Configuration**: Details the steps to create and configure the initial VM, including network and SSH settings ([see VM Configuration](#2-vm-configuration)).
3. **Install Docker and OpenSSH Server**: Instructions for installing Docker and OpenSSH Server on the VM ([see Install Docker and OpenSSH Server](#3-install-docker-and-openssh-server)).
4. **Clone the project repository**: Steps to generate SSH keys, add them to GitHub, and clone the project repository ([see Clone the project repository](#4-clone-the-project-repository)).
5. **Clone the VM**: Guide to cloning the initial VM to create two additional VMs ([see Clone the VM](#5-clone-the-vm)).
6. **Launch and manage the VMs**: Commands to start, stop, and manage the VMs and the microservice ([see To launch the VMs in the future](#6-to-launch-the-vms-in-the-future)).

By following these steps, you will have a fully functional Tracking GPS Microservice running on three virtual machines.

## 1. Prerequisites 

- VirtualBox or any other virtualization software
- Ubuntu Server [ISO image](https://ubuntu.com/download/server)

## 2. VM Configuration

1. **Create a New VM:**
    - **Name and Operating System**
        - Name: `broker` or whatever you prefer, it will be the broker VM.
        - ISO image location: Select the Ubuntu Server ISO image.
        - Type: `Linux` (already selected by default)
        - Subtype: `Ubuntu`
        - Version: `Ubuntu (64-bit)`
    - **Unattended Install**
        - Username and password: select your preferred username and password for the VM. (If it's a test VM, you can use `user` and `password`.)
    - **Hardware**
        - Base Memory (RAM): `2048 MB`
        - Processor: `1 CPU`
    - **Hard Disk**
        - Check `Create a virtual hard disk now` if it's not already checked
        - Size: `10 GB` will be enough. 
        - Hard Disk File Type and Variant: `VDI (VirtualBox Disk Image)`
        - Uncheck `Pre-allocated Full Size` if not already unchecked, to save space in a constrained environment.

    - Click Finish to create the VM. The VM will be created with the above settings and the Ubuntu Server ISO image will be attached to it.
2. **Install Ubuntu Server:**
    - After having clicked Finish, the VM will start.
    - Follow the installation prompts to install Ubuntu Server. (nothing to do here, really)

3. **Configure VM Settings:**
    - **Network:**
        - Adapter 1:
            - Attached to: `Bridged Adapter` and the rest will be automatically filled. This will allow the VM to get an IP address from the network and to be accessible from other devices (e.g., your host machine and other VMs).
    - **SSH Configuration:**
        - Install OpenSSH Server to allow remote access to the VM. 
        ```bash
        sudo apt install openssh-server
        sudo systemctl start ssh
        sudo systemctl enable ssh
        ```
        - Check the IP address of the VM using `ip a` and use it to connect to the VM from another device with an SSH client.
        ```bash
        ssh user@ip_address
        ```
        - You can also use the VM's hostname if you have a DNS server set up.

## 3. Install Docker and OpenSSH Server

1. **Update the package list:**
    ```sh
    sudo apt update
    ```
2. **Install Docker:**
    ```sh
    sudo apt install docker.io
    sudo apt install docker-compose
    ```
    Steps from 2. and 3. could be different, you may not need to enter all those commands to install Docker if you are prompted to install it, as well as with OpenSSH Server.

## 4. Clone the project repository

1. **Create a key pair for the VM:**
    ```sh
    ssh-keygen -t ed25519 -C "your email"
    ```
2. **Add the key to the SSH agent:**
    ```sh
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    ```
3. **Copy the public key to the clipboard:**
    ```sh
    cat ~/.ssh/id_ed25519.pub
    ```
4. **Add the public key to your GitHub account.**
5. **Clone the repository inside a directory of your choice:**
    ```sh
    git clone git@github.com:Kiltakaro/Traking_Gps.git
    ```

## 5. Clone the VM

1. **Shut down the VM.**
2. **In your virtualization software, clone the VM twice to create two additional.**
3. **Once the cloning is done, you can start the VMs in headless mode and then change the hostname of each VM to `broker`, `producer1` and `producer2` respectively.**

## 6. To launch the VMs in the future

1. **Start the VMs in headless start mode to save resources (small [icon](https://prnt.sc/SaN3VSw3tbKP) on the right of the VM in VirtualBox).**
2. **Navigate to the project directory and depending on the VM you are in, run the following command:**
    - **For the broker VM:** <br>
    To prepare the broker VM, run the following command:
    ```sh
    ./prepare-broker.sh <broker_ip>
    ```
    where `<broker_ip>` is the IP address of the broker VM.<br>
    Then, to start the broker VM, run the following command:
    ```sh
    ./start-broker.sh
    ```
    To stop the VM, run the following command:
    ```sh
    ./stop-broker.sh [-v]
    ```

    - **For the other two VMs:**
    ```sh
    ./prepare-producer.sh <id of the producer (1 or 2)>
    ```
    Then, to start the producer VM, run the following command:
    ```sh
    ./start-producer.sh <broker_ip>
    ```
    where `<broker_ip>` is the IP address of the broker VM.<br>
    To stop the VMs, run the following command:
    ```sh
    ./stop-producer.sh
    ```
If you need any help, you can add "--help" at the end of the command to get more information. Example:
```sh
./prepare-broker.sh --help
```

You may need to run the commands with `sudo` if you encounter permission issues. The website will be accessible at `http://<broker_ip>:8000` where `<broker_ip>` is the IP address of the broker VM.
<br>
WARNING: You should wait until the line 
```sh 
backend   | <DATE> - INFO - Setting newly assigned partitions {TopicPartition(topic='coordinates_topic', partition=0)} for group fastapi_consumer_group
```
 has been printed in the terminal before accessing the website (it should take less than a minute).