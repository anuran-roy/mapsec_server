import socket
import subprocess

import nmap
import pandas as pd


def get_arp(regex: str = "") -> list:
    final_command = "arp -a"
    if len(regex) > 0:
        final_command += f" | grep {regex}"
    return subprocess.getoutput(final_command).split("\n")


def get_devices_in_network(include_self: bool = False):
    """Get the devices connected to the gateway using arp table."""
    df_dict = {"name": [], "ipv4": [], "ipv6": [], "type": [], "interface": []}
    op = get_arp(regex="wlp4s0")
    gateway_interface = ""
    self_device: str = subprocess.getoutput("hostname -I | awk '{print $1}'")
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

        if nm == "_gateway":
            gateway_interface = interface

    return df_dict, gateway_interface


def scan_ports(include_self: bool = False):
    nm = nmap.PortScanner()

    potential_devices_to_scan, gateway_interface = get_devices_in_network(
        include_self=include_self
    )
    devices_df = pd.DataFrame(potential_devices_to_scan)

    devices_to_scan = potential_devices_to_scan
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
