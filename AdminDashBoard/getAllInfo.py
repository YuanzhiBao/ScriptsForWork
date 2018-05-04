#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

import subprocess,json


def convert_str2float(b):
    # b has to be a dict
    # [('lifeson',
    #   {'basic_info': {'product': ' PowerEdge 2970'}, 'disk_list': {'disk': 100.2, 'diskused': 5.6, 'diskfree': 97.1},
    #    'ram_list': {'ram': 31.0, 'ramused': 2.0, 'ramfree': 27.0},
    #    'cpu_list': {'cpuname': 'Quad-Core AMD Opteron(tm) Processor 2374 HE', 'physicalcpu': 2.0, 'cpucores': 4.0,
    #                 'virtualcpu': 8.0}, 'diskusedwidth': 5, 'diskfreewidth': 96, 'ramusedwidth': 6, 'ramfreewidth': 87}), (
    #  'vanhalen',
    #  {'basic_info': {'product': ' PowerEdge R515'}, 'disk_list': {'disk': 1057.9, 'diskused': 425.8, 'diskfree': 660.9},
    #   'ram_list': {'ram': 62.0, 'ramused': 61.0, 'ramfree': 1.0},
    #   'cpu_list': {'cpuname': 'AMD Opteron(tm) Processor 4280', 'physicalcpu': 2.0, 'cpucores': 4.0,
    #                'virtualcpu': 16.0}, 'diskusedwidth': 40, 'diskfreewidth': 62, 'ramusedwidth': 98, 'ramfreewidth': 1}), (
    #  'clapton',
    #  {'basic_info': {'product': ' PowerEdge R515'}, 'disk_list': {'disk': 1175.3, 'diskused': 473.3, 'diskfree': 781.7},
    #   'ram_list': {'ram': 62.0, 'ramused': 14.0, 'ramfree': 0.0},
    #   'cpu_list': {'cpuname': 'AMD Opteron(tm) Processor 4280', 'physicalcpu': 2.0, 'cpucores': 4.0, 'virtualcpu': 16.0},
    #   'diskusedwidth': 40, 'diskfreewidth': 66, 'ramusedwidth': 22, 'ramfreewidth': 0})]

    for item in b.items():
        # print(item[1]['basic_info'])
        # print(b[item[0]])
        for key, value in item[1].items():
            # print(key, value)
            # print(b[item[0]][key])
            try:
                for V in value.items():
                    # print(b[item[0]][key][V[0]])
                    try:
                        b[item[0]][key][V[0]] = float(b[item[0]][key][V[0]])
                    except (ValueError, TypeError) as e:
                        pass
            except AttributeError:
                pass
    return b

class VMhost():

    '''
    This class is used to get the basic infomation of the VMhost
    It includes basic information
    disk information
    ram information
    and cpu information
    return format is always like below
    basic information --> {"product: KVM"}
    disk information --> {'diskused': '5.7', 'diskfree': '18.7', 'disk': '21.6'}
    ram information --> {'ramused': '0', 'ram': '1', 'ramfree': '0'}
    cpu information --> {'physicalcpu': '2', 'cpuname': \
                        'AMD Opteron 23xx (Gen 3 Class Opteron)', 'cpucores': '1', 'virtualcpu': '2'}


    '''

    def __init__(self):

        baseCommend = "hostname | cut -d. -f1"
        output = subprocess.check_output(['bash','-c',baseCommend])
        hostname = output.strip()
        self.hostname = hostname


    def gethostname(self):

        return self.hostname

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

    def ram_list(self):
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

    def cpu_list(self):

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

        return cpu_list



class VMs():

    def __init__(self):

        baseCommend = "virsh list --all | awk -F' ' '{if(NR>2){print $2}}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        self.vm_list = []
        for item in output.split('\n'):
            if item != '':
                self.vm_list.append(item)

    def getStateInfo(self,vm):

        state_info = {}


        baseCommend = "virsh domstats %s | grep state.state | \
        sed  \"s#1#running#g\" | sed \"s#5#shut off#g\"| cut -d\".\" -f2" %vm
        output = subprocess.check_output(['bash', '-c', baseCommend])

        state_info[output.split("\n")[0].split("=")[0]] = output.split("\n")[0].split("=")[1]

        return state_info

    def getCPUInfo(self,vm):

        cpu_info = {}

        baseCommend = "virsh domstats %s | grep vcpu.current" % vm
        output = subprocess.check_output(['bash', '-c', baseCommend])
        cpu_info[output.split("\n")[0].split("=")[0].strip()] = output.split("\n")[0].split("=")[1].strip()

        baseCommend = "virsh domstats %s | grep vcpu.maximum" % vm
        output = subprocess.check_output(['bash', '-c', baseCommend])
        cpu_info[output.split("\n")[0].split("=")[0].strip()] = output.split("\n")[0].split("=")[1].strip()

        return cpu_info

    def getDiskInfo(self,vm):

        disk_info = {}

        baseCommend = "virsh domstats %s | egrep \"block.*.phy|block.*.path|block.*.cap\"" % vm
        output = subprocess.check_output(['bash', '-c', baseCommend])
        disk_info = self.format_vm_disk_info(output)

        return disk_info


    def format_vm_disk_info(self, diskString):

        disk_info = {}

        i = 3

        for item in diskString.split("\n"):
            if item == "":
                continue
            # print(i, item)
            if (i % 3) == 0:
                diskname = item.split('=')[1].strip()
                disk_info[diskname] = {}
            if (i % 3) == 1:
                diskvalue = float(item.split("=")[1]) / 1073741824
                disk_info[diskname]["LC"] = diskvalue
            if (i % 3) == 2:
                diskvalue = float(item.split("=")[1]) / 1073741824
                disk_info[diskname]["PC"] = diskvalue
            i += 1

        return disk_info

    def getVMInfo(self):

        self.vms_info = {}

        for vm in self.vm_list:
            state_info = self.getStateInfo(vm)
            cpu_info = self.getCPUInfo(vm)
            disk_info = self.getDiskInfo(vm)

            self.vms_info[vm] = {'state_info': state_info, 'cpu_info': cpu_info, 'disk_info': disk_info}

        global convert_str2float

        self.vms_info = convert_str2float(self.vms_info)

        return self.vms_info


if __name__ == "__main__":

    allinfo = {}

    VMhost = VMhost()

    hostname = VMhost.gethostname()

    basic_info = VMhost.basic_info()
    disk_list = VMhost.disk_list()
    ram_list = VMhost.ram_list()
    cpu_list = VMhost.cpu_list()

    ramusedwidth = int((float(ram_list["ramused"]) / float(ram_list["ram"])) * 100)

    ramfreewidth = int((float(ram_list["ramfree"]) / float(ram_list["ram"])) * 100)

    diskusedwidth = int((float(disk_list["diskused"]) / float(disk_list["disk"])) * 100)

    diskfreewidth = int((float(disk_list["diskfree"]) / float(disk_list["disk"])) * 100)

    allinfo[hostname] = {'basic_info': basic_info, 'disk_list': disk_list, 'ram_list': ram_list, \
                           'cpu_list': cpu_list, 'diskusedwidth': diskusedwidth, 'diskfreewidth': diskfreewidth, \
                           'ramusedwidth': ramusedwidth, 'ramfreewidthd': ramfreewidth}

    VMs = VMs()

    VMsInfo = VMs.getVMInfo()

    allinfo[hostname]['vms_info'] = VMsInfo


    allinfo = convert_str2float(allinfo)

    print(json.dumps(allinfo))










































