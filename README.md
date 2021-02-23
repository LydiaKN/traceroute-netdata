# traceroute-netdata
Display data from traceroute command at Netdata using Python Plugin

The template.py is the code when the data collection happens, while template.conf is the configuration file of the correspinding alarm.

The modify.py opens the template.py file and replaces the target IP with the destination IP and saves at the corresponding Python data collection directory. 
The intended IP is passed as an argument when the modify.py is executed.

Charm3 is a JUJU charm and it is used for creating actions allowing adding new trcaeroute-charts for new IPs. Takes the address as a parameter and either creates or
remove a chart. 
The charm3.py file uses the modify.py at a VNF instnance for creating new charts and corresponding alarms at netdata. 

The charm3_b.py file is used as a charm for removing charts from the VNF. 

Modify.py, template.py. template.conf are downloaded to the VDU(VM) of the instance via cloud-init file.
For the VDU a image with a pre-installed Netdata is used.
