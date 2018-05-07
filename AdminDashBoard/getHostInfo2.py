#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

import subprocess, json, urllib2


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
        output = subprocess.check_output(['bash', '-c', baseCommend])
        hostname = output.strip()
        self.hostname = hostname

    def gethostname(self):

        return self.hostname

    def getdiskTotal(self):
        ## all space
        baseCommend = "df -h | awk -F' ' '{if(NR>1){print $2}}' |awk -F'G' '{print $1}' | sed -r 's#(.*)([M]$)#1#g' | \
                    sed -r 's#(.*)([T]$)#1000#g'|awk '{sum+=$1}END{print \"disk:\"sum}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        # disk_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()

        key = "diskTotal"

        value = output.split("\n")[0].split(":")[1].strip()

        return value

    def getdiskUsed(self):

        baseCommend = "df -h | awk -F' ' '{if(NR>1){print $3}}' |awk -F'G' '{print $1}' | \
                    sed -r 's#(.*)([M]$)#1#g' | awk '{sum+=$1}END{print \"diskused:\"sum}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        # disk_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()

        key = "diskUsed"
        value = output.split("\n")[0].split(":")[1].strip()

        return value

    def getdiskRaw(self):

        baseCommend = "df -h"
        output = subprocess.check_output(['bash', '-c', baseCommend])

        output_json = json.dumps(output)

        return output_json

    def getoperatingSystem(self):

        baseCommend = "cat /etc/redhat-release"

        output = subprocess.check_output(['bash', '-c', baseCommend])

        key = "operatingSystem"

        value = output.strip()

        return value

    def getvms(self):

        vms = {}

        baseCommend = "virsh list --all  | tail -n +3 | awk -F'[ ]+' '{print $3\":\"$4,$5}' \
        | head -n -1"

        output = subprocess.check_output(['bash', '-c', baseCommend])

        out = output.split("\n")

        for item in out:
            if item:
                key = item.strip().split(":")[0]
                value = item.strip().split(":")[1]
                vms[key] = value

        return vms

    def getCpuInfo(self):

        cpuInfo = {}

        ##cpuname
        baseCommend = "cat /proc/cpuinfo | grep 'name' | head -1 | awk -F':' '{print $2}'|\
                        sed 's/^ //g' | awk -F':' '{print \"model:\"$1}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        cpuInfo[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1].strip()

        ##cpucores
        baseCommend = "cat /proc/cpuinfo | grep \"cpu cores\" | uniq | awk -F: '{print $2}' | \
                sed 's/^ //g' | awk '{print \"numberCores:\"$1}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        cpuInfo[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]

        # cpuMaxSpeed
        baseCommend = "dmidecode -t processor | grep 'Speed'| head -1"

        output = subprocess.check_output(['bash', '-c', baseCommend])

        key = "maxSpeed"

        value = output.split(":")[1].strip()

        cpuInfo[key] = value

        # cpuCurrentSpeed
        baseCommend = "dmidecode -t processor | grep 'Speed'| head -2 | tail -1"

        output = subprocess.check_output(['bash', '-c', baseCommend])

        # key = output.split(":")[0].strip()
        key = "curSpped"
        value = output.split(":")[1].strip()

        cpuInfo[key] = value

        # print(cpuInfo)

        return cpuInfo

    # coresAllocatedVM: Number, //Number of cores allocated / in use by virtual machines.

    def getcoresAllocatedVM(self):

        baseCommend = "virsh domstats | grep vcpu.current | awk -F'=' '{sum+=$2} END {print sum}'"

        output = subprocess.check_output(['bash', '-c', baseCommend])
        key = "coresAllocatedVM"
        value = output.strip()
        return value

    # ramUsed: Number, //Megs used (actual RSS)

    def getRamUsed(self):

        ##Used space
        baseCommend = "free -mg | awk '{if (NR==2){print \"ramused:\"$3}}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        # ram_list[output.split("\n")[0].split(":")[0]] = output.split("\n")[0].split(":")[1]

        key = "ramUsed"

        value = output.split("\n")[0].split(":")[1]

        return value

    def getamtRam(self):

        ## all space

        baseCommend = "free -mg | awk '{if (NR==2){print \"ram:\"$2}}'"
        output = subprocess.check_output(['bash', '-c', baseCommend])
        key = "amtRam"
        value = output.split("\n")[0].split(":")[1]

        return value

    def getdefault_address(self):

        baseCommend = "DEV=`route | grep \"default\" | awk '{print $NF}'`; ip a | grep -A 4 $DEV \
        | grep -m 1 \"inet\" | awk '{print $2}'"

        output = subprocess.check_output(['bash', '-c', baseCommend])
        key = "default_address"
        value = output.strip()
        return value

    def getipAddrs(self):

        baseCommend = "ip addr list | grep -oE \
        '((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])(/?[0-3]?[0-9]?)' \
        | tail -n +2"

        output = subprocess.check_output(['bash', '-c', baseCommend])
        output = output.strip().split("\n")

        return output

    def getAllInfo(self):

        hostinfo = {}

        hostinfo["name"] = self.gethostname()

        hostinfo["coresAllocatedVM"] = self.getcoresAllocatedVM()

        hostinfo["ramUsed"] = self.getRamUsed()

        hostinfo["amtRam"] = self.getamtRam()

        hostinfo["CpuInfo"] = self.getCpuInfo()

        hostinfo["diskTotal"] = self.getdiskTotal()

        hostinfo["diskUsed"] = self.getdiskUsed()

        # hostinfo["getdiskRaw"] = self.getdiskRaw()

        hostinfo["vms"] = self.getvms()

        hostinfo["default_address"] = self.getdefault_address()

        hostinfo["ipAddrs"] = self.getipAddrs()

        return hostinfo


# xinhaobaocunlenima

class push_API():
    '''
    This class is used to connect to API to push data to the API as well
    '''

    def __init__(self, data, audata = None, urlp = None, urla = None):
        self.data = data
        if not audata:
            self.audata = json.dumps({'name': 'apitest', 'pass': 'this_is_temporary'})
        else:
            self.audata = json.dumps(audata)
        if not urla:
            self.url_auth = "http://127.0.0.1:3000/auth"
        else:
            self.url_auth = urla
            # change the push url as needed
        if not urlp:
            self.url_push = "http://127.0.0.1:3000"
        else:
            self.url_push = urlp
        self.token = ""
        self.pulldata = []

    def authentication_Save_Token(self):
        req = urllib2.Request(self.url_auth, self.audata, {'Content-Type': 'application/json'})
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError:
            print("Authentication Failed")
            return
        response = json.loads(f.read())
        f.close()
        self.token = response["token"]

    def checkToken(self):

        req = urllib2.Request(self.url_push)
        req.add_header('x-access-token', self.token)

        req.add_data(self.data)
        f = urllib2.urlopen(req)

        token_response = json.loads(f.read())

        f.close()
        # change with the right response as needed
        if isinstance(token_response, (list,)):
            self.pulldata = token_response
        elif isinstance(token_response, (dict,)):
            if token_response["message"] and token_response["message"] == 'invalid signature':
                print("Invalid signature! Please try again")
                return

    def getData(self):
        if not self.token:
            self.authentication_Save_Token()

        self.checkToken()

        global littleInfo

        littleInfo = self.pulldata




if __name__ == "__main__":
    host = VMhost()

    AllInfo = host.getAllInfo()


    print(AllInfo)