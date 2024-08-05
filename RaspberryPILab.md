# Raspberry Pi Lab

In this lab, you will log into your Raspberry pi and get used to using
the computer. In Linux, there is a GUI like Windows, but much more
than Windows or MacOSX, in Linux use of the command line is pretty
typical. There are huge benefits to learning this older way of communicating

1. It's frequently faster (once you know what you are doing)
1. Sequences of commands can be automated by writing a script
1. Commands can be run not only on one computer, but on many at one time
1. requires much less overhead than a graphical user interface, good for low-end computers, or computers that are under stress.
1. Uses much less bandwidth to remotely manipulate the computer

## Instructions

1. Assemble the raspberry pi with the preformatted memory card in the slot
1. Log in. The predefined user is pi and the password is "raspberry"
1. Create an account for yourself
   ```bash
   sudo adduser yourid
   # don't have to do this: sudo passwd yourid  # choose something secure!
   sudo adduser guest  # let's create a guest account. You can pick a different id
   # change the password for the original user eventually for security.
   # we won't do it now so we can get in in case you forget your password
   ```
1. set up the wifi
   - I do not have the instructions in advance, TAs please figure out how to do this on the stevens network and create the commands here
1. Setup sshd so you can log into the Raspberry pi remotely
   - [https://raspberrypi-guide.github.io/networking/connecting-via-ssh]
   - [https://www.seeedstudio.com/blog/2021/01/25/three-methods-to-configure-raspberry-pi-wifi/?srsltid=AfmBOorm4PyGroZ5v0CHdPMGaaM5biQtFXlIR8p_Lguru9khSvrHiXZx]
1. Install packages we will be using in the course
   ```bash
   sudo apt install g++ python
   ```
1. Edit a test c++ file (call it hello.cpp)
   You can type this in, or write your own. You can also get in the browser on
   the pi and get to this page, then paste the code into your editor to save
   effort.
   ```bash
   #include <iostream>
   
   int main() {
     std::cout << "hello world\n";
     return 0;
   }
   ```
   Compile with
   ```bash
   g++ -g hello.cpp       # compiles the program and creates a.out
   ./a.out                # runs a.out in the current directory
   ```
1. Edit a python program, call it hello.py
   ```python
   print("Hello, World!")
   ```
   Execute the code with:
   ```bash
   python hello.py
   ```
1. Find out some information about the network
   ```bash
   hostname
   hostname -I
   #find out a partner's ip address, and see if you can reach them
   ping 155.246.___.____  # your partner's ip (it might not be 155.246)
   ```
1. Log into your neighbor's computer (if possible)
   Note: Stevens may actively prevent this on their network because they are worried about attacks
   What we need is a private wifi so we can "play" inside it.
   ```bash
   ssh guest@your-neighbor-ip   # this will ask you for the password. Then you will be on remotely!
   scp myfile guest@your-neighbor-ip:  # this will copy a file from your home directory to the remote one
   ```
1. Create a public/private keypair
   ```bash
   ssh-keygen -t rsa  # you will need to press enter 3 times...
   ```
   Now, in folder ```/home/yourid/.ssh``` you have files
   ```id_rsa``` and ```id_rsa.pub```
1. For security, consider whether you want to leave ssh remote login working after you leave the class.
   Remember that on any network, someone can try to ssh to your computer. It's safer to disable if you don't want this.
   If you are on your private network at home with a router, you're pretty safe.
## References

[Curated list of Linux Commands](github.com/LinuxCrashCourse/LinuxCrashCourse)

## Basic commands
```bash
ls		# list all files in the current directory
mkdir x		# create a directory named x
cd x            # go into the directory named x
cd              # go to your home directory, typically /home/youruserid
gedit test.txt  # edit a text file using the default gui editor
vi test.txt     # Use vi, a cryptic old text editor on every linux system
chmod 400 file  # permissions, I can read, not write or execute no one else
chmod 644 file  # default on most computers I can read/write, everyone else on my computer can read
```

## Installing software

Let's practice by installing some or all of the following
```bash
sudo apt update                # get the latest list of available software
sudo apt install gcc-toolchain # install c, c++ and all tools
sudo apt install python        # install python
sudo apt install emacs         # another ancient editor that i like!
sudo apt install code
sudo apt install openssl       # install the openssl toolkit
```

## Installing libraries in python

Once python is installed, you may still need to install libraries.
For cryptography, we will have to install

```bash
pip install cryptography
```

Networking commands

```bash
hostname

ping 192.168.1.1	# see if you can reach an ip address (this is typical local address, not at Stevens)
nslookup google.com     # look up the name in DNS and find out the corresponding IP address
ping google.com		# see if you can reach a known entity out of stevens
nmcli -f in-use,ssid,freq,bssid,signal,rate,bars  dev wifi  # list wifi
ssh remotecomputer      # log into a remote computer

sudo ssh-keygen -t rsa  # create a public/private keypair on your computer
```