# traceroute-netdata
A VNF that displays data from traceroute command at Netdata using Python Plugin.

The template.py is the code when the data collection happens, while template.conf is the configuration file of the correspinding alarm.

The modify.py opens the template.py file, copies its content to a new file and replaces the target IP with the destination IP. Then, the new file is saved at the corresponding Python data collection directory. 
In addition, modify.py opens the template.conf copies its content to a new file in orser to set an alert foe the new chart. Then, the new file is saved at the Netdata helath directory. 
The intended IP is passed as an argument when the modify.py is executed. 

Charm3 is a JUJU charm and it is used for creating actions allowing adding/removing trcaeroute-charts for new IPs. The actions take the address as a parameter and either creates or removes a chart. 
Charm3 belongs to the VNF package.

The coding part of the charm is located at the reactive file, while there other .yaml configuration files.
The charm3.py file uses the modify.py at a VNF instnance for creating new charts and corresponding alarms at netdata. 
The charm3_b.py file is used as a charm for removing charts from the VNF. 

The VNF package is uploaded as traceroute_vnfd.tar.gz
Modify.py, template.py. template.conf are downloaded to the VDU(VM) of the VNF instance via cloud-init file, which is also included at the VNF package.

For the VDU, which is mentioned at the VNFD, an image with a pre-installed Netdata is used.

NS package is also included, uploaded as traceroute_nsd.tar.gz. 


