from math import *
import subprocess
import os
import pexpect
import yaml
import sys

def get_pid(device):

  output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+ device, stdout=subprocess.PIPE, shell=True)
  (out, err) = output.communicate()
  return(out.strip())



file_name=str(sys.argv[1]) +"_device_inventory.yml"

inventory_list = open(file_name, "r")
inventory=yaml.load(inventory_list)

VM_list=inventory['VMcontainer_names']
#print(VM_list)

pid_list=[]
for VMs in VM_list:
  output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+ VMs, stdout=subprocess.PIPE, shell=True)
  (out, err) = output.communicate()
  temp=[VMs,out.strip()]
  pid_list.append(temp)

#print(pid_list)

for VMs in pid_list:
  veth_pair="sudo ip link del  "+ VMs[0]
 # vm_veth_attach="sudo ip link set vm_veth1 netns "+ VMs[1]
  ovs_veth_attach="sudo ovs-vsctl del-port "+VMs[0][:5]+"-Br "+VMs[0]
  os.system(veth_pair)
#  os.system(vm_veth_attach)
  os.system(ovs_veth_attach)

#for VMs in pid_list:
#  set_veth_up="sudo ip link set "+VMs[0]+"  up"

##remove connectivity between south subnet bridge and south-subnet namespace####

NS_list=inventory['Namespace_names']
No_subnet=len(NS_list)-2
tenantNO=NS_list[0][0]
for i in range(No_subnet):
  subNO=i+1
  Base_name=str(tenantNO)+"-S-"+str(subNO)
  veth_pair="sudo ip link del "+Base_name+"-sub2"
  ovs_veth_attach="sudo ovs-vsctl del-port "+Base_name+"-Br "+Base_name+"-sub2"
  veth_pair1="sudo ip link del "+Base_name+"-S-sub2"
  ovs_veth_attach1="sudo ovs-vsctl del-port "+Base_name+"-southBr "+Base_name+"-S-sub2"
  os.system(veth_pair)
  os.system(ovs_veth_attach)
  os.system(veth_pair1)
  os.system(ovs_veth_attach1)




NS_list=inventory['Namespace_names']
No_subnet=len(NS_list)-2
tenantNO=NS_list[0][0]
for i in range(No_subnet):
  subNO=i+1
  Base_name=str(tenantNO)+"-S-"+str(subNO)
  FW1_PID=get_pid(Base_name+"-FW1")
  FW2_PID=get_pid(Base_name+"-FW2")
  veth_pair1="sudo ip link del "+Base_name+"-FW1-sub2"
  veth_pair2="sudo ip link del "+Base_name+"-FW2-sub2"
  ovs_veth_attach1="sudo ovs-vsctl del-port "+Base_name+"-southBr "+Base_name+"-FW1-sub2"
  ovs_veth_attach2="sudo ovs-vsctl del-port "+Base_name+"-southBr "+Base_name+"-FW2-sub2"
  os.system(veth_pair1)
  os.system(ovs_veth_attach1)

  os.system(veth_pair2)
  os.system(ovs_veth_attach2)
  
  veth_pair3="sudo ip link del "+Base_name+"-FW1-sub4"
  veth_pair4="sudo ip link del "+Base_name+"-FW2-sub4"
  ovs_veth_attach3="sudo ovs-vsctl del-port "+Base_name+"-southBr "+Base_name+"-FW1-sub4"
  ovs_veth_attach4="sudo ovs-vsctl del-port "+Base_name+"-southBr "+Base_name+"-FW2-sub4"

  bridge_name=str(tenantNO)+"-S-"+str(subNO)+"-northBr"
  veth_pair="sudo ip link del "+bridge_name+"-1"
  ovs_veth_attach="sudo ovs-vsctl del-port "+bridge_name+" "+bridge_name+"-2"
  os.system(veth_pair)
  os.system(ovs_veth_attach)






bridge_name=str(tenantNO)+"-OVS-s"
NS_name=str(tenantNO)+"-south"

veth_pair="sudo ip link del "+bridge_name+"-veth1"
ovs_veth_attach="sudo ovs-vsctl del-port "+bridge_name+" "+bridge_name+"-veth2"
os.system(veth_pair)
os.system(ovs_veth_attach)

bridge_name=str(tenantNO)+"-OVS-s"
bridge1_name=str(tenantNO)+"-OVS-n"

veth_pair1="sudo ip link del "+bridge_name+"-veth3"
veth_pair2="sudo ip link del "+bridge_name+"-veth5"
ovs_veth_attach1="sudo ovs-vsctl del-port "+bridge_name+" "+bridge_name+"-veth4"
ovs_veth_attach2="sudo ovs-vsctl del-port "+bridge_name+" "+bridge_name+"-veth6"
os.system(veth_pair1)
os.system(ovs_veth_attach1)
os.system(veth_pair2)
os.system(ovs_veth_attach2)


veth_pair1="sudo ip link del "+bridge1_name+"-veth3"
veth_pair2="sudo ip link del "+bridge1_name+"-veth5"
ovs_veth_attach1="sudo ovs-vsctl del-port "+bridge1_name+" "+bridge1_name+"-veth4"
ovs_veth_attach2="sudo ovs-vsctl del-port "+bridge1_name+" "+bridge1_name+"-veth6"
os.system(veth_pair1)
os.system(ovs_veth_attach1)
os.system(veth_pair2)
os.system(ovs_veth_attach2)


bridge_name=str(tenantNO)+"-OVS-n"

veth_pair="sudo ip link del "+bridge_name+"-veth1"
ovs_veth_attach="sudo ovs-vsctl del-port "+bridge_name+" "+bridge_name+"-veth2"
os.system(veth_pair)
os.system(ovs_veth_attach)

