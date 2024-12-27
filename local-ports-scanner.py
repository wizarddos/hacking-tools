# Remote local port scanner/banner grabber
# usage: curl http://[Your IP]/[port]/local-ports-scanner.py | python3

import subprocess

def scan_port(port, command):
    try:
        banner = subprocess.run(command, stdout=subprocess.PIPE)
        print("[+] Command executed")
        print("\033[32m" + f"[+] 127.0.0.1:{port}" + "\033[0m")
        output = banner.stdout.decode("UTF-8")
        if output:
            print("\n" +banner.stdout.decode("UTF-8"))
            print("\n\n")
        else:
            print("[-] Nothing there!")
    except subprocess.CalledProcessError:
        print("[-] Something went wrong")

def craft_command(commandID, port):
    if commandID == 1:
        return ["curl", f"http://127.0.0.1:{port}"]
    elif commandID == 2:
        return ["nc", "127.0.0.1", port]
    elif commandID == 3:
        return ["nmap", "127.0.0.1", f"-p{port}"]
    else:
        return 0
        

running = subprocess.run(["netstat", "-tulpn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = running.stdout.decode("UTF-8")
processes = [line for line in output.split("\n") if "LISTEN" in line and "127.0.0.1" in line]
ports = []

processes.pop(0)
processes.pop(0)

for process in processes:
    separated = process.split("      ")
    try:
        ports.append(separated[2].split(":")[-1])
    except IndexError:
        print("[+] Out of range - exiting loop")

ports = list(dict.fromkeys(ports))

scanMethod = 1
methods = ["curl", "nc", "nmap"]

check_if_command_exists = subprocess.run(["which", methods[scanMethod-1]], stdout=subprocess.PIPE)
if "not found" in check_if_command_exists.stdout.decode("UTF-8"):
    print("[-] Method unavailable")

for port in ports:
    command = craft_command(scanMethod, port)
    scan_port(port, command)