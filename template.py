# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from random import SystemRandom
import os
from bases.FrameworkServices.SimpleService import SimpleService
import math


target="8.8.8.8"

TRACE_COMMAND="traceroute -q 1 -I "+target


priority = 90000
update_every = 4

def rtts_and_ips(output):#output is the output of the traceroute command
    
    ips=[]#ips:the known IPs of te devices which consist the route. When the IP is not known, there is a *, as in in the traceroute command output
    rtts_str=[]#rtts_str: the RTTs as a string, when RTT is not known, there is a * , as in the traceroute command output
    #the lists: ips and rtts_str, are parallel
    
    annotations=['!X','!N','!P','!S','!F','!0','!1','!2','!3','!4','!5','!6','!7','!8','!9','!10','!11','!12','!13','!14','!15']
     
 

    for i in range(1,len(output)):

        line=output[i].strip()#Remove spaces at the beginning and at the end of the string.This line is optional.
        line=line.split(" ")#split the string to a list of strings ,where there is a space
        #print(line)
        if('*' not in line):#is there is no * we have the IP address and the RTT
            for word in line:
                digits = sum(characters.isdigit() for characters in word)#count the digits in a word
                letters=sum(characters.isalpha() for characters in word)
                #print(word)
                if (word.count('.')==3 and letters==0):#condition for the IP address
                    address=word
                    if ('(' in word or ')' in word) :
                        address=word[1:len(word)-1]
                    
                    
                    
                
                if ((word.count('.')==1 or word.count(',')==1) and (digits==5 or digits==4)):
                    time=word
                    if 'ms' in word:
                        time=word[:len(word)-2]
                    if(',' in time):#this conditiion means that we have infos about time, because ',' indicates there is a number in output
                        time=time.replace(',','.')#example:12,3ms-->12.3ms //useful for float convertion, because 
                                                     #python recognizes as floats values only with '.'
                    

                                                               
        else:     
            address='*'
            time='*'
        for annotation in annotations:
            if (annotation in line):
                address=address+annotation 
        
        ips.append(address)
        rtts_str.append(time)
        

    return [rtts_str,ips]#return the lists

class Route:

    def __init__(self,command):

        #self.command=TRACE_COMMAND
        self.command=command

    def exe_cmd(self):

        f=os.popen(self.command)

        output=f.read()

        return output.splitlines()


ORDER = [
'all_hops'
  
]


CHARTS = {       
  'all_hops': {

     'options': ["all_hops", "All RTT from each host which consists the path", "ms", "Traceroute to "+target, "Traceroute", "line"],

    'lines': [ ]

  }  
}



class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS


    @staticmethod
    def check():
        return True

        

    def create_charts(self,ips,rtts,avg,best,worst,stdev):
        data=dict()
        for i in range(len((ips))):
            if (ips[i]!='*'):
                #Making the new chart for each new IP consnsists the path
                chart_name=ips[i]
                #We add the chart name in the ORDER list
                if chart_name not in ORDER:
                    ORDER.append(chart_name)
                    self.debug('Adding new chart in ORDER:',chart_name)
                #We create the chart.
                if chart_name not in self.charts:
                    CHARTS[chart_name]={'options': [chart_name,chart_name+'-Hop'+str(i+1),'ms','Traceroute to '+target, 'Traceroute', 'line']}
                    self.debug('Adding new chart in CHARTS:',chart_name)
                #Now we add the newly created chart to the charts to be displayed.
                params = [chart_name] + CHARTS[chart_name]['options']
                self.charts.add_chart(params)
                self.debug('add_charts has been executed')
                #Once the chart has been created we populate it with dimensions 
                dimension_id_last = ''.join(['RTT', '_',ips[i]])
                dimension_id_avg = ''.join(['average',ips[i]])
                dimension_id_best = ''.join(['best',ips[i]])
                dimension_id_worst = ''.join(['worst',ips[i]])
                dimension_id_stdev = ''.join(['standard_deviation',ips[i]])
                dimensions=[dimension_id_last,dimension_id_avg,dimension_id_best,dimension_id_worst,dimension_id_stdev]
                self.debug('dimensions',dimensions)
                #We add this dimsnsion to the chart that has been created
                #The last 1000 is divisor: This means that when the value is represented it will be divided by 1000
                for dimension in dimensions:
                    if dimension not in self.charts[chart_name]:
                        self.charts[chart_name].add_dimension([dimension,None,None,None,1000])
                    #We populate the data dictionary
                    #We add an entry into the data dictionary.
                    #The entry will be the value for the metric to be displayed. Since this value might be fractional
                    #and only integer values are collected we multiply this by 1000.
                    #That is why we had the 1000 divisor on the dimension creation
                data[dimension_id_last] = float(rtts[i])*1000
                data[dimension_id_avg] = float(avg[i])*1000
                data[dimension_id_best] = float(best[i])*1000
                data[dimension_id_worst] = float(worst[i])*1000
                data[dimension_id_stdev] = float(stdev[i])*1000
                #Making the chart where all the RTT for exery host at the path are shown together
                if(ips[i]!=target):
                    dimension_id_together=''.join(['hop'+str(i+1), '_',ips[i]])
                else:
                    dimension_id_together=''.join('final_hop')
                if dimension_id_together not in self.charts['all_hops']:
                    self.charts['all_hops'].add_dimension([dimension_id_together,None,None,None,1000])
                data[dimension_id_together] = float(rtts[i])*1000

        return data


    n=0
    
    all_ips=[]
    all_avg=[]
    all_avg_sq=[]
    all_best=[]
    all_worst=[]
    all_stdev=[]

    def get_data(self):
        data = dict()

        traceroute=Route(TRACE_COMMAND)
        output=traceroute.exe_cmd()
        self.debug('The execution of the command has finished')
        [rtts,ips]=rtts_and_ips(output)
        
        self.n=self.n+1

        self.debug('rtts',rtts)
        self.debug('ips',ips)
        best=[]
        worst=[]
        avg=[]
        stdev=[]


        for i in range(len(ips)):
            if(ips[i] not in self.all_ips and ips[i]!='*'):
                self.debug('new IP adress',ips[i])
                self.all_ips.append(ips[i])
                self.all_best.append(float(rtts[i]))
                self.all_worst.append(float(rtts[i]))
                self.all_avg.append(float(rtts[i]))
                self.all_avg_sq.append(float(rtts[i])**2)
                self.all_stdev.append(0.0)

                best.append(float(rtts[i]))  
                worst.append(float(rtts[i]))
                avg.append(float(rtts[i]))
                stdev.append(0.0)


            else:
                position=self.all_ips.index(ips[i])
                if (float(rtts[i])<self.all_best[position]):#finding best rtt
                    self.all_best[position]=float(rtts[i])
                if (float(rtts[i])>self.all_worst[position]):#finding worst rtt
                    self.all_worst[position]=float(rtts[i])
                #calculating average rtt|| old avg:μ=Σ/n-1-->with the new nth value x, the new mean is: μ'=(Σ+x)/n-->μ'=(n*μ+x)/n
                self.all_avg[position]=(self.all_avg[position]*(self.n-1)+float(rtts[i]))/self.n
                #variance:Var(x)=E(x^2)-E(x)^2
                self.all_avg_sq[position]=(self.all_avg_sq[position]*(self.n-1)+(float(rtts[i])**2))/self.n#E(x^2)
                variance=self.all_avg_sq[position]-self.all_avg[position]**2
                self.all_stdev[position]=math.sqrt(variance)#standard deviation
                
                best.append(self.all_best[position]) 
                worst.append(self.all_worst[position]) 
                avg.append(self.all_avg[position])
                stdev.append(self.all_stdev[position])

        self.debug('stats')
        self.debug('best=',best)
        self.debug('worst=',worst)
        self.debug('avg=',avg)
        self.debug('stdev=',stdev)
        

        data=self.create_charts(ips,rtts,avg,best,worst,stdev)
       


        return data

