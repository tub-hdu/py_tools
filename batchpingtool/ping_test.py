#-*- coding:utf-8 -*-
import subprocess
import re
import os,tempfile
import platform
from ipip import IP

_path = os.path.dirname(os.path.realpath(__file__))
while True:
    if os.path.isdir(_path):
        break
    else:
        _path = os.path.dirname(_path)
IP.load(os.path.join(_path,"17monipdb.dat"))
_temp_path = os.path.join(_path,"temp")
if not os.path.isdir(_temp_path):
    os.makedirs(_temp_path)

def ping_test(ip,now_os='',count=0):
    test_result = {}

    if not validate_ip(ip):
        return test_result

    if now_os == '':
        now_os = platform.system()

    now_os = now_os.lower()
    if now_os not in ["windows","linux"]:
        return test_result

    if count == 0:
        if now_os == "windows":
            count = 4
        elif now_os == "linux":
            count = 10

    # 得到一个临时文件对象， 调用close后，此文件从磁盘删除
    out_temp = tempfile.TemporaryFile(mode='w+',dir=_temp_path)
    # 获取临时文件的文件号
    fileno = out_temp.fileno()
    if(now_os=="windows"):
        p = subprocess.Popen("ping %s -n %s" % (ip,count),shell=True,stdout=fileno)
        p.wait()
        out_temp.seek(0)
        ping_message = "\n".join(out_temp.readlines())
        ping_result = ping_message.decode('cp936').encode('utf-8')

        try:
            time_pat_str = re.compile(r"最短\s*=\s*(\d+\.*\d*)ms\s*.*最长\s*=\s*(\d+\.*\d*)ms\s*.*平均\s*=\s*(\d+\.*\d*)ms")
            times = time_pat_str.search(ping_result).groups()
            test_result["min"] = times[0]
            test_result["max"] = times[1]
            test_result["avg"] = times[2]
        except:
            pass

        try:
            pkg_pat_str = re.compile(r"已发送\s*=\s*(\d+)\s*.*已接收\s*=\s*(\d+)\s*.*丢失\s*=\s*(\d+)\s*\(\s*(\d+%)\s*丢失\s*\)")
            pkgs = pkg_pat_str.search(ping_result).groups()
            test_result["trans"] = pkgs[0]
            test_result["recv"] = pkgs[1]
            test_result["loss"] = pkgs[2]
            test_result["loss_rate"] = pkgs[3]
        except:
            pass

        try:
            ip_pat_str = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*的\s*Ping\s*统计信息")
            ips = ip_pat_str.search(ping_result).groups()
            test_result["ip"] = ips[0]
            test_result["address"] = IP.find(ips[0]).strip().replace("\t","-")
        except:
            pass
    else:
        p = subprocess.Popen("ping %s -c %s" % (ip,count),shell=True,stdout=fileno)
        p.wait()
        out_temp.seek(0)
        ping_message = "\n".join(out_temp.readlines())
        ping_result = ping_message

        try:
            time_pat_str = re.compile(r"min\/avg\/max\S*\s*=\s*(\d+\.*\d*)\/(\d+\.*\d*)\/(\d+\.*\d*)")
            times = time_pat_str.search(ping_result).groups()
            test_result["min"] = times[0]
            test_result["avg"] = times[1]
            test_result["max"] = times[2]
        except:
            pass

        try:
            pkg_pat_str = re.compile(r"(\d+)\s*packets\s*transmitted\s*,\s*(\d+)\s*received\s*,\s*(\d+%)\s*packet\s*loss")
            pkgs = pkg_pat_str.search(ping_result).groups()
            test_result["trans"] = pkgs[0]
            test_result["recv"] = pkgs[1]
            test_result["loss_rate"] = pkgs[2]
            test_result["loss"] = int(pkgs[0]) - int(pkgs[1])
        except:
            pass

        try:
            ip_pat_str = re.compile(r"PING\s*\S+\s*\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)")
            ips = ip_pat_str.search(ping_result).groups()
            test_result["ip"] = ips[0]
            test_result["address"] = IP.find(ips[0]).strip().replace("\t","-")
        except:
            pass


    return test_result

def validate_ip(ip):
    if not ip:
        return False

    ip_format = re.compile(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$")
    if not ip_format.match(ip):
        return False

    return True


