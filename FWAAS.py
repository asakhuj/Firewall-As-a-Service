import os
import sys
import sqlite3
import time
import paramiko
import json
import yaml
import iptc

def is_tenant_already_exists(tenant_name):

    with open("VPC_Database.txt","r") as fwrite:
        #print(fwrite.readline())
        temp=fwrite.readlines()

    if len(temp)==0:
        return(False)

    for tenants in temp:
        tenants=tenants.split(" ")
        if (tenants[0] == tenant_name):
            return(True)
    return(False)

def custom_rule(tenant_name,subnet):
    fname = tenant_name + "-" +str(subnet)+ "-FW.txt"
    val = 'custom'
    if(val == 'custom'):
	num = int(raw_input("Enter the number of rules you want to enter"))
        for i in range(0,num):
                pro = raw_input("Choose a protocol tcp/udp: ")

                port = raw_input("Choose a valid port number: ")

                source = raw_input("Enter a source address network: ")

                dest = raw_input("Enter a destination address network: ")

                rul = raw_input("Choose a action ACCEPT/DROP : ")
                r = "iptables -I INPUT"
                rule = iptc.Rule()
                rule.protocol = pro
                if(port != "0"):
                        rule.dport=port
                        r += " " + "--dport "+port
                if(source != "0"):
                        rule.src = source
                        r += " " + "-s " + source
                if(dest != "0"):
                        rule.dst = dest
                        r += " " + "-d " + dest
                if(rul != "0"):
                        rule.target = iptc.Target(rule, rul)
                        r += " " + "-j " + rul
                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                #print(rule)
                #print(r)
                with open(fname,"a") as f:
                        f.write(r)
                        f.write("\n")

def configFW(tenant_name,tenant_id,subnet_no,rule):
    FW_name1=str(tenant_id)+"-S-"+str(subnet_no)+"-FW1"
    FW_name2=str(tenant_id)+"-S-"+str(subnet_no)+"-FW2"
    if rule=='d':
        with open('defaultRules.txt','r') as rule:
            rules=rule.readlines()
            for i in rules:
                command="sudo docker exec "+FW_name1+"  " + i 
                os.system(command)
                command="sudo docker exec "+FW_name2+"  " + i
                os.system(command)
    elif rule=='s':
        with open('secureRules.txt','r') as rule:
            rules=rule.readlines()
            for i in rules:
                command="sudo docker exec "+FW_name1+"  " + i 
                os.system(command)
                command="sudo docker exec "+FW_name2+"  " + i
                os.system(command)
    
    elif rule=='c':
        file_name=tenant_name+"-"+str(subnet_no)+"-FW.txt"
        with open(file_name,'r') as rule:
            rules=rule.readlines()
            for i in rules:
                command="sudo docker exec "+FW_name1+"  " + i 
                os.system(command)
                command="sudo docker exec "+FW_name2+"  " + i
                os.system(command)


def creat_new_subnet():

    fromFile = json.load(open('VPC_details.json'))
    Tenant_name=raw_input("Please enter the name of the Tenant\n")
    subnet_name=raw_input("please enter the name of subnet\n")
    No_vm= input("Please enter the number of VM required in the subnet\n")
    need_internalFW=raw_input("Do you need internal FW for this subnet? \n press Y for YES \n press N for NO \n ")
    if need_internalFW =='y':
    	firewallType =raw_input("Please choose the firewall type : Custom (C) , Default (D), Secure (S)") 
    for start in fromFile:
      arr=fromFile[start]
      print(len(arr))
      #print('Array : ',arr)
      for m in range(len(arr)):
        #print(arr[m])
        for elem in arr[m] :
            if(elem == 'tenantName'):
		 nameOfTenant = fromFile['VPC'][m]['tenantName']
		 if nameOfTenant==Tenant_name:
                    fromFile['VPC'][m]['noOfSubnets']=fromFile['VPC'][m]['noOfSubnets']+1
                    for d in fromFile['VPC'][m]:
                        if d =='internalDetails':
                            for q in fromFile['VPC'][m]['internalDetails']:
                                #print( q )
                                array =[q]
                                newDetails = {}
                                #subnet_name=raw_input("please enter the name of subnet\n")
				newDetails['subnetName'] = subnet_name
                        	#No_vm= input("Please enter the number of VM required in the subnet\n")
                        	#for i in range(1,No_vm+1):
                            		#dct_str['VMcontainer_names'].append(tenantNumber+'-S-'+sub_no+'-V-'+str(i))
                        	newDetails['noOfVMs'] = No_vm
                        	#need_internalFW=raw_input("Do you need internal FW for this subnet? \n press Y for YES \n press N for NO\n")
                        	newDetails['internalFirewallNeeded'] = need_internalFW
                        	if need_internalFW =='y':
                                	#firewallType =raw_input("Please choose the firewall type : Custom (C) , Default (D), Secure (S) \n")
                                	#newDetails['firewallType'] = firewallType
                                	FW_fileName = "FW_"+Tenant_name+"_"+subnet_name+".txt"
                                	newDetails['FW_fileName'] = FW_fileName
                        	array.append(newDetails)
                		#newDetails['internalDetails'] = array
                		fromFile['VPC'][m]['internalDetails']= array
        print('---------------------')
	file = open('VPC_details.json', 'r+')
	file.truncate()

        with open('VPC_details.json', 'w') as outfile:
    			json.dump(fromFile, outfile)
                #inventoryFile = str(Tenant_name)+"_device_inventory.yml"
                #with open(inventoryFile, 'a+') as out_file:
                #        yaml.safe_dump(dct_str, out_file, indent=4,default_flow_style=False)
				

def Create_new_VM():
    with open("VPC_Database.txt","r") as fwrite:
    #print(fwrite.readline())
        temp=fwrite.readlines()
    tenant_name=raw_input("Please enter the name of the Tenant\n")
    tenant_no=0
    for tenant in temp:
        tenants=tenant.split(" ")
        tenant_no+=1
        if (tenants[0] == tenant_name):

            subnet_name=raw_input("Please input the name of the subnet\n")
            no_subnet=int(tenants[1])
            i=2
            y=0

            while (i<len(tenants)):
                y+=1
                if tenants[i]==subnet_name:
                    vmnumber=int(tenants[i+1])+1
                    os_commad="sudo ./CreateVM.sh " + str(tenant_no) + " " + str(y) + " " + str(vmnumber)
                    os.system(os_commad)
                    return
                i=i+3
                #print(new_subnet_name
    print("ERRORR")
    return()



def CreateNewVPC():

    #conn = sqlite3.connect('Tenant_DB.db')
    #cur = conn.cursor()
    #arpita
    data = json.load(open('VPC_details.json'))
    for elem in data:
    	if elem == 'VPC':
		noOfTenants = len(data[elem])
        	print('Number of tenants ',noOfTenants)
                tenantNumber= str(noOfTenants+1)
        	dataToBeStored = {}
                dataToBeStored['tenantID'] = tenantNumber
    		Tenant_name=raw_input("Please enter the name of the tenant\n")
    		dataToBeStored['tenantName'] = Tenant_name
    		No_subnet= int(raw_input("How many subnets do you want in your VPC\n"))
    		dataToBeStored['noOfSubnets'] =  No_subnet
                array = []
                dct_str = {'FWcontainer_names':[tenantNumber+'-FW1',tenantNumber+'-FW2'], 
			    'VMcontainer_names':[], 'OVSbridge_names': [tenantNumber+'-OVS-n', tenantNumber+'-OVS-s'],
                             'Namespace_names':[tenantNumber+'-north', tenantNumber+'-south']	}
    		for sub_no in range(1,No_subnet+1):
                        sub_no =str(sub_no)
        		subnet_name=raw_input("please enter the name of subnet\n")
                        dct_str['OVSbridge_names'].append(tenantNumber+'-S-'+sub_no+'-southBr')
                        dct_str['OVSbridge_names'].append(tenantNumber+'-S-'+sub_no+'-northBr')
                        dct_str['OVSbridge_names'].append(tenantNumber+'-S-'+sub_no+'-Br')
                        dct_str['Namespace_names'].append(tenantNumber+'-S-'+sub_no+'-S')
                        #Creating FW containers
                        dct_str['FWcontainer_names'].append(tenantNumber+'-S-'+sub_no+'-FW1')
                        dct_str['FWcontainer_names'].append(tenantNumber+'-S-'+sub_no+'-FW2')

			internalDetails = {}
                        internalDetails['subnetName'] = subnet_name
                        internalDetails['subnetID'] = sub_no
                        No_vm= input("Please enter the number of VM required in the subnet\n")
                        for i in range(1,No_vm+1):
			    dct_str['VMcontainer_names'].append(tenantNumber+'-S-'+sub_no+'-V-'+str(i))
                        internalDetails['noOfVMs'] = No_vm
                        need_internalFW=raw_input("Do you need internal FW for this subnet? \n press Y for YES \n press N for NO\n")
                        internalDetails['internalFirewallNeeded'] = need_internalFW
                        if need_internalFW =='y':
                                firewallType =raw_input("Please choose the firewall type : Custom (C) , Default (D), Secure (S) \n")
                                internalDetails['firewallType'] = firewallType
                                FW_fileName = "FW_"+Tenant_name+"_"+subnet_name+".txt"
                                internalDetails['FW_fileName'] = FW_fileName
        		array.append(internalDetails)
     		dataToBeStored['internalDetails'] = array
     		data['VPC'].append(dataToBeStored)
    		file = open('VPC_details.json', 'r+')
    		file.truncate()

    	       	with open('VPC_details.json', 'w') as outfile:
    			json.dump(data, outfile)
	       	print("----")
               	inventoryFile = str(Tenant_name)+"_device_inventory.yml"
               	with open(inventoryFile, 'a+') as out_file:
    			yaml.safe_dump(dct_str, out_file, indent=4,default_flow_style=False)
	        command = "sudo ansible-playbook Make_network.yml --extra-vars \"tenant_name="+Tenant_name+"\""
                os.system(command)
                print('--------Executed Ansible script--------------')
                readFWChoice(Tenant_name)



def readFWChoice(tenantName):
	print('-------------------Entering firewall rules--------------------------')
	fromFile = json.load(open('VPC_details.json'))
	print('=========')
	for start in fromFile:
    	      arr =fromFile[start]
    	      for m in range(len(arr)):
        	for elem in arr[m] :
            		if(elem == 'tenantName'):
                		nameOfTenant = fromFile['VPC'][m]['tenantName']
                                #print("NameOfTenant", nameOfTenant)
				#print(tenantName)
                		if nameOfTenant==tenantName:
                    			internalDetails = fromFile['VPC'][m]['internalDetails']
                    			#print("Found tenant subnet size: ", len(internalDetails))
                    			for i in range(0,len(internalDetails)) :
                        			fwType =internalDetails[i]['firewallType'].lower()
						if(fwType =='c'):
						     print("----Calling custom rule----")
						     custom_rule(tenantName,internalDetails[i]['subnetID'])
	                                        print('--------Pushing FW rules---------------')   
	                                        configFW(tenantName,fromFile['VPC'][m]['tenantID'],internalDetails[i]['subnetID'],fwType)	



def EditIPtables():
    print("-------------Please enter the correct values only , no exception handling is done---------------- ")
    choice = input('Where do you want to enter the firewall rule ? '
               '1 : Exterior '
               '2 : Interior\n');
    #print(choice)
    if choice==1:
        #print("Entered 1 : exterior\n")
        rule=raw_input("Enter the rule to be implemented. Please enter the exact rule WITHOUT SUDO : \n")
        hostname="192.168.2.2"
        ExternalFWrule(hostname,rule)
        hostname="192.168.2.3"
        ExternalFWrule(hostname,rule)

    elif choice==2:
        tenantNumberEntered = raw_input("Enter the tenant number where rule needs to be implemented : ")
        subnetNumberEntered = raw_input("Enter the subnet number of the tenant where rule needs to be implemented : ")
        with open("VPC_Database.txt","r") as fwrite:
            #print(fwrite.readline())
            temp=fwrite.readlines()

        tenantID=0
        SubnetID=0
        tempID=0
        for tenants in temp:
            tenants=tenants.split(" ")
            tenantID+=1
            if (tenants[0] == tenantNumberEntered):
                subnet_found=False
#                print(tenants[0])
                for t_i in range(len(tenants)):
                    tempID+=1

                    if tenants[t_i]==subnetNumberEntered:
#                        print(tenants[t_i])
                        subnet_found=True
                        print(tenants[t_i + 2])
                        if 'N' in tenants[t_i + 2]:
                            print("\n\n\n\nThis subnet doesnt have internal firewall\n\n\n\n")
                            return()
                        break

                if subnet_found:
                    SubnetID=int(tempID/3)
                    break
                else:
                    print("Invalid Subnet Name\n")
                    return()



        rule=raw_input("Enter the rule to be implemented. Please enter the exact rule WITHOUT SUDO : ")
        os.system("sudo ip netns exec "+str(tenantID)+"-S-"+str(SubnetID)+"-FW1 " +str(rule));
        os.system("sudo ip netns exec "+str(tenantID)+"-S-"+str(SubnetID)+"-FW2 " +str(rule));
    else :
        print('Incorrect value entered :(')
    return()


def deleteVM():

    with open("VPC_Database.txt","r") as fwrite:
        #print(fwrite.readline())
        temp=fwrite.readlines()

    tenantID=0
    SubnetID=0
    tempID=0
    tenantNumberEntered=raw_input("Please enter the tenant name\n")

    for tenants in temp:
        tenants=tenants.split(" ")
        tenantID+=1
        if (tenants[0] == tenantNumberEntered):
            subnetNumberEntered=raw_input("Please enter the name of the subnet\n")
            subnet_found=False
            #print(tenants[0])
            for t_i in range(len(tenants)):
                tempID+=1

                if tenants[t_i]==subnetNumberEntered:
                    #print(tenants[t_i])
                    subnet_found=True
                    SubnetID=int(tempID/3)
                    break
            break
    os_commad= "sudo ./deletevmfromsubnet.sh " + str(tenantID) + " " + SubnetID + " " + '1'
    os.system(os_commad)
    return()







def ExternalFWrule(hostname,rule):

    commands = [rule]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username='root', password='root')
    channel = client.invoke_shell()

    # clear welcome message and send newline
    time.sleep(1)
    channel.recv(9999)
    channel.send("\n")
    time.sleep(1)

    for command in commands:
        channel.send(command + "\n")
        while not channel.recv_ready(): #Wait for the server to read and respond
            time.sleep(0.1)
        time.sleep(0.1) #wait enough for writing
        output = channel.recv(9999) #read
        time.sleep(0.1)
        channel.send("root" + "\n")
    channel.close()
    return()




def deleteTenant():
        fromFile = json.load(open('VPC_details.json'))
        #print('Existing tenants',fromFile)
	#print(fromFile)
	print('=========')
        toDelete = raw_input("Please enter the name of the tenant to delete \n")
	for start in fromFile:
    		arr =fromFile[start]
    		for m in range(0,len(arr)-1):
        		for elem in arr[m] :
            			if(elem == 'tenantName'):
                			nameOfTenant = fromFile['VPC'][m]['tenantName']
                			if nameOfTenant==toDelete :
                    				del fromFile['VPC'][m]
                    				print("Deleted tenant : " +nameOfTenant)

	#print('data left is', fromFile)

	file = open('VPC_details.json', 'r+')
	file.truncate()

	with open('VPC_details.json', 'w') as outfile:
    		json.dump(fromFile, outfile)

	command = "sudo ansible-playbook deleteTenant.yml --extra-vars \"tenant_name="+toDelete+"\""
        os.system(command)
        #command2= "sudo rm "+toDelete+"_device_inventory.yml"
	#os.system(command2)

def viewTenantDetails() :
    fromFile = json.load(open('VPC_details.json'))
    print('=========')
    for start in fromFile:
        arr =fromFile[start]
        for m in range(len(arr)):
            for elem in arr[m] :
                if(elem == 'tenantName'):
                    nameOfTenant = fromFile['VPC'][m]['tenantName']
                    tenantID = fromFile['VPC'][m]['tenantID']
                    print("Tenant name : " +nameOfTenant+ " , Tenant ID : " + tenantID)

def fetchTenantID(tenantName):
	fromFile = json.load(open('VPC_details.json'))
	print('=========')
	for start in fromFile:
    	 	arr =fromFile[start]
    		for m in range(len(arr)):
        		for elem in arr[m] :
            			if(elem == 'tenantName'):
                			nameOfTenant = fromFile['VPC'][m]['tenantName']
                			if nameOfTenant==tenantName:
                                                #print(tenantName)
				     		return fromFile['VPC'][m]['tenantID']
	return "none"
def alertLogging():
       print('alert')
       tenantName= raw_input("Enter the tenant name for applying alert logs \n")
       tenant_id = fetchTenantID(tenantName)
       if tenant_id == "none":
		print("Invalid tenant name")
		return
       sourceIP = raw_input("Please enter the source IP you want to track \n")
       FW_name1=str(tenant_id)+"-FW1"
       FW_name2=str(tenant_id)+"-FW2"
       rule = "iptables -I INPUT -s "+sourceIP +"  -j NFLOG --nflog-group 0 "
       command="sudo docker exec "+FW_name1+"  " + rule
       os.system(command)
       command="sudo docker exec "+FW_name2+"  " + rule
       os.system(command)

def main():


    print("Welcome")


    print("")

    while True:
        a="""#####################################################################################################################
             #                                                                                                                   #
             #       Press 1: Create A new VPC                                                                                   #
             #       Press 2: Add a new Subnet to existing network                                                               #
             #       Press 3: Add VM to existing Subnet                                                                          #
             #       Press 4: Edit Firewall rules to Internal/External Firewall                                                  #                                                        #
             #       Press 5: Delete a VM from a Subnet                                                                          #
             #       Press 6: Delete a subnet from a Tenant                                                                      #                                                                                                     #
             #       Press 7: Delete a tenant                                                                                    #
             #       Press 8: To EXIT
	     #       Press 9: Use Alert logging feature
                     Press 10 : View Tenant names and ID                                                                             #
             #                                                                                                                   #
             #####################################################################################################################"""
        print("WELCOME........Please choose the Task\n\n\n")
        print(a)

        task_name=int(raw_input("\n\n\n\n\n\n\n"))

        if task_name==1:
            CreateNewVPC()
        elif task_name==2:
            creat_new_subnet()
        elif task_name==3:
            Create_new_VM()
        elif task_name==4:
            EditIPtables()
        elif task_name==5:
            print("Service unavilable right now")
        elif task_name==6:
            print("Service unavilable right now")
        elif task_name==7:
            deleteTenant()
        elif task_name==8:
            break
        elif task_name==9:
	    alertLogging()
        elif task_name==10:
             viewTenantDetails()
        else:
            print("INVALID ENTRY\n")
    return()


if __name__ == "__main__":
    main()

