import socket
import subprocess

import nmap
import pandas as pd


def get_devices_in_network():
    """Get the devices connected tothe gateway using arp table."""
    df_dict = {"name": [], "ipv4": [], "ipv6": [], "type": [], "interface": []}
    op = subprocess.getoutput(f"arp -a | grep 192.168.").split("\n")

    for i in op:
        line = i.split()
        nm = line[0] if line[0] != "?" else "Unknown Device"
        ipv4 = line[1][1:-1]
        ipv6 = line[3]
        tp = line[4][1:-1]
        interface = line[-1]

        if nm != "_gateway":
            df_dict["name"].append(nm)
            df_dict["ipv4"].append(ipv4)
            df_dict["ipv6"].append(ipv6)
            df_dict["type"].append(tp)
            df_dict["interface"].append(interface)

    return df_dict


def scan_ports():
    nm = nmap.PortScanner()

    devices_to_scan = get_devices_in_network()
    # print(devices_to_scan)
    exposed_ports_dict = {}

    for device in devices_to_scan["ipv4"]:
        # print(f"Getting report for = {device}")
        report = list(nm.scan(f"{device}/24")["scan"].values())[0]
        # print(report)
        ip = report["addresses"]["ipv4"]

        exposed_ports_dict[ip] = [port for port in report["tcp"]]

    return exposed_ports_dict


if __name__ == "__main__":
    print(scan_ports())
