#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

import subprocess,json


def basic_info(self):
    basic_info = {}

    baseCommend = "dmidecode | grep \"Product\" | awk -F':' '{if(NR==1){print \"product:\"$2}}'"

    output = subprocess.check_output(['bash','-c',baseCommend])

    basic_info[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()

    return basic_info

# for string output : "product: KVM"


def disk_list(self):
    disk_list = {}

    ## all space
    baseCommend = "df -h | awk -F' ' '{if(NR>1){print $2}}' |awk -F'G' '{print $1}' | sed -r 's#(.*)([M]$)#1#g' | \
                sed -r 's#(.*)([T]$)#1000#g'|awk '{sum+=$1}END{print \"disk:\"sum}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    disk_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()

    ## Used space
    baseCommend = "df -h | awk -F' ' '{if(NR>1){print $3}}' |awk -F'G' '{print $1}' | \
                sed -r 's#(.*)([M]$)#1#g' | awk '{sum+=$1}END{print \"diskused:\"sum}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    disk_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()

    ## free space
    baseCommend = "df -h | awk -F' ' '{if(NR>1){print $4}}' |awk -F'G' '{print $1}' | \
                sed -r 's#(.*)([M]$)#1#g' | awk '{sum+=$1}END{print \"diskfree:\"sum}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    disk_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()


    ## end of getting the disk information

    ## string output {'diskused': '5.7', 'diskfree': '18.7', 'disk': '21.6'}

    return disk_list

def ram_list():
    ## get the ram information starts

    ram_list = {}

    # cmd

    ##All space

    ## all space

    baseCommend = "free -mg | awk '{if (NR==2){print \"ram:\"$2}}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    ram_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]

    ##Used space
    baseCommend = "free -mg | awk '{if (NR==2){print \"ramused:\"$3}}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    ram_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]

    ##free space
    baseCommend = "free -mg | awk '{if (NR==2){print \"ramfree:\"$4}}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    ram_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]



    ## end of the getting the ram information

    return ram_list


###CPU info starts

def cpu_list():

    cpu_list = {}

    ##cpuname
    baseCommend = "cat /proc/cpuinfo | grep 'name' | head -1 | awk -F':' '{print $2}'|\
            sed 's/^ //g' | awk -F':' '{print \"cpuname:\"$1}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    cpu_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()


    ##physicalcpu
    baseCommend = "cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l| awk '{print \"physicalcpu:\"$1}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    cpu_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]

    ##cpucores
    baseCommend = "cat /proc/cpuinfo | grep \"cpu cores\" | uniq | awk -F: '{print $2}' | \
            sed 's/^ //g' | awk '{print \"cpucores:\"$1}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    cpu_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]


    ##virtualcpu
    baseCommend = "cat /proc/cpuinfo | grep 'processor' | wc -l | awk '{print \"virtualcpu:\"$1}'"
    output = subprocess.check_output(['bash','-c',baseCommend])
    cpu_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]



if __name__ == "__main__":

    allinfo = {}

    baseCommend = "hostname | cut -d. -f1"
    output = subprocess.check_output(['bash','-c',baseCommend])
    hostname = output.strip()


    basic_info = basic_info()
    disk_list = disk_list()
    ram_list = ram_list()
    cpu_list = cpu_list()

    ramusedwidth = int((float(ram_list["ramused"]) / float(ram_list["ram"])) * 100)

    ramfreewidth = int((float(ram_list["ramfree"]) / float(ram_list["ram"])) * 100)

    diskusedwidth = int((float(disk_list["diskused"]) / float(disk_list["disk"])) * 100)

    diskfreewidth = int((float(disk_list["diskfree"]) / float(disk_list["disk"])) * 100)

    allinfo[hostname] = {'basic_info': basic_info, 'disk_list': disk_list, 'ram_list': ram_list, \
                           'cpu_list': cpu_list, 'diskusedwidth': diskusedwidth, 'diskfreewidth': diskfreewidth, \
                           'ramusedwidth': ramusedwidth, 'ramfreewidth': ramfreewidth}

    print(allinfo)








































