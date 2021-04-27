from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import csv
import re


def dev_info(task):
    r = task.run(netmiko_send_command, command_string="show ip ssh")
    result = r.result
    match = re.search(r"SSH Enabled - version (\d.+)\n", r.result)
    ssh_version = ""
    if match:
        ssh_version = match.groups(1)[0]
        print(f"ssh Version is {ssh_version}")

    r = task.run(netmiko_send_command, command_string="show run | sec snmp")
    result = r.result
    match = re.search(r"snmp-server group SEC3GROUP v(\d+)\s", r.result)
    snmp_version = ""
    if match:
        snmp_version = match.groups(1)[0]
        print(f"snmp Version is {snmp_version}")

    r = task.run(netmiko_send_command, command_string="show version", use_genie=True)
    task.host["facts"] = r.result
    serial = task.host['facts']['version']['chassis_sn']
    hoster = task.host['facts']['version']['hostname']
    image = task.host['facts']['version']['system_image']
    im_type = task.host['facts']['version']['image_type']
    operating = task.host['facts']['version']['os']
    ver = task.host['facts']['version']['version']

    with open('NETWORK_INVENTORY.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        csvdata = (task.host.hostname, hoster, serial,
                   image, im_type, operating, ver, snmp_version, ssh_version)
        writer.writerow(csvdata)



def main() -> None:
    nr = InitNornir()
    result = nr.run(task=dev_info)

    print_result(result)


if __name__ == '__main__':
    main()
