# Networking Commands

For more details, see: [LinuxCrashCourse](https://github.com/LinuxCrashCourse/LinuxCrashCourse)

```bash
ping ipaddress      #report round trip time and if reachable
traceroute ipaddress #see all the steps it took to get there
hostname            #display your computer's hostname
ip addr             # current: display your computers IP address(es)
ifconfig            #old command equivalent to ```ip addr```
netstat -r          #display routing table
nslookup google.com #look up the name and return the IP address
dhcpcd              #DHCP daemon runs on your computer to get IP address
sshd                #Allows remote login to this computer (dangerous)
ssh <ipaddr>        #login to another computer
ssh-keygen -t rsa   #generate a public/private RSA keypair
ssh-keygen -t ecc   #generate a public/private ECC keypair
scp <file> <ipaddr>:<file>  #copy a file to another computer
scp <ipaddr>:<file> <file>  #copy a file from another computer
wireshark           #Capture and analyze network traffic
iwslist             #List all network interfaces on this computer
sudo nmap -sP 192.168.1.0/24    #search for hosts on the network
ufw                 # A simple firewall for linux
wget <url>          #download a file from a URL
nmcli dev wifi list # show all wifi networks available
tcpdump             #Capture and analyze network traffic
```