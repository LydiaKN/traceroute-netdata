#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def new_chart_alarm(address):
    #NEW CHART PART
    source = open("/home/ubuntu/template.py")#opening the original source file

    string_list_src = source.readlines()#split the file to list of strings,every line of the file is 
                                        #an elemment of the string_list_src
    string_list_dest=string_list_src#this will be the content of the modified file

    string_list_dest[9]='target="'+address+'"'#modification to the specific line of th source file
                                              #where the target IP is configured 

    address=address.replace('.','_')
    #ADDING THE REAL PATH LATER
    dest=open("/usr/libexec/netdata/python.d/dest"+address+".chart.py","w")#opening 
                                                                           #the new file named, 
                                                                           # dest<IP>.chart.py

    new_file_contents = "".join(string_list_dest)#this command converts a string-list to a single string
                                                 #this convertion is used for writing the string to
                                                 # the new file 

    dest.write(new_file_contents)#writing the new file

    source.close()#closing the source file
    dest.close()#closing the new file

    src_alarm = open("/etc/netdata/health.d/rtt.conf")#opening the .conf file of the initial alarm

    string_src_alarm = src_alarm.readlines()#split the file to list of strings,every line of the file is 
                                            #an elemment of the string_src_alarm

    string_dest_alarm=string_src_alarm#this will be the content of the modified .conf file


    string_dest_alarm[1]='    on: dest'+address+'.all_hops\n'#modification to the specific line of th source 
                                                            #.conf file
                                                            #changing th on: line 

    string_dest_alarm[10]='    on: dest'+address+'.all_hops\n'#modification to the specific line of th source 
                                                            #.conf file
                                                            #changing th on: line 
                                                            #seting the 1st alarm

    dest_alarm=open("/etc/netdata/health.d/rtt"+address+".conf","w")#opening 
                                                                    #the new file named, 
                                                                    # rttX_X_X_X.chart.py,where X.X.X.X is the 
                                                                    #IP adress
                                                                    #setting the 2nd alarm

    new_alarm_contents = "".join(string_dest_alarm)#this command converts a string-list to a single string
                                                    #this convertion is used for writing the string to
                                                    # the new .conf file 


    dest_alarm.write(new_alarm_contents)#writing the new .conf file

    src_alarm.close()#closing the source .conf file
    dest_alarm.close()#closing the new .conf file
    

if len(sys.argv) > 1:
    address = sys.argv[1]
else:
    print('Usage: python modify.py <address>')
    sys.exit(1)

new_chart_alarm(address)



