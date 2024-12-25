import subprocess
import os
import pty

print("[+] Starting Server")
command = subprocess.run(["sudo", "/usr/bin/mosh-server"], stdout=subprocess.PIPE)
result = command.stdout.decode("UTF-8").split()

key = result[3]        
port = result[2]

print("[+] Server up")
print("[!] Execute:")
print(f"\t export MOSH_KEY="+key + f"; mosh-client 127.0.0.1 {port}")