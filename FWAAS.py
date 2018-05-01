import os
import sys
import sqlite3
import time
import paramiko


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


def creat_new_subnet():
    with open("VPC_Database.txt","r") as fwrite:
    #print(fwrite.readline())
        temp=fwrite.readlines()
    tenant_name=raw_input("Please enter the name of the Tenant\n")
    tenant_no=0
    for tenant in temp:
        tenants=tenant.split(" ")
        tenant_no+=1
        if (tenants[0] == tenant_name):

            new_subnet_name=raw_input("Please input the name of the new subnet\n")
            no_subnet=int(tenants[1])
            i=2;

            while (i<len(tenants)):
                if tenants[i]==new_subnet_name:
                    print("Subnet already exists\n\n Aborting...\n")
                    return
                i=i+3
                #print(new_subnet_name)

            no_of_vm=raw_input("How many VMs do you want in this subnet\n")
            internal_FW=raw_input("Is internal FW required for this subnet\n")

            new_sub_string=new_subnet_name+" "+str(no_of_vm)+" "+internal_FW+" "
            #print(new_sub_string)
            new_tenant_list=""
            for j in range(len(tenants)):
                if (j!=1):

                    if (j==(len(tenants)-1)):
                        new_tenant_list+=str(tenants[j]).rstrip('\n')
                    else:
                        new_tenant_list+=str(tenants[j]).rstrip('\n')
                        new_tenant_list+=" "
                else:
                    no_subnet+=1
                    new_tenant_list+=str(no_subnet)
                    new_tenant_list+=" "


                    #s=str(tenants[j]).rstrip("\n")
                    #ew_tenant_list+=s
                    #new_tenant_list+=" "
            new_tenant_list+=new_sub_string
            #new_tenant_list+="\n"
            #print(new_tenant_list)
            #print("end")
            #print(new_tenant_list.split(" "))
            os_command="sudo ./CreateSubnet.sh "+ str(no_subnet) + " " + str(tenant_no) + " " + tenant_name + " " + no_of_vm
            os.system(os_command)
            return()

    print("No such Tenant found")
    return()


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

    TenantDB_list=[]
    with open("VPC_Database.txt","a") as fwrite:
        pass
    with open("VPC_Database.txt","r") as fwrite:
        #print(fwrite.readline())
        temp_var=fwrite.readlines()
    tenant_number=len(temp_var)+1
    Tenant_name=raw_input("Please enter the name of the VPC\n")

    if (is_tenant_already_exists(Tenant_name) == True):
        print("Tenant name already exists\n")
        return()
    TenantDB_list.append(Tenant_name)
    No_subnet= int(raw_input("How many subnets do you want in your VPC\n"))
    TenantDB_list.append(str(No_subnet))

    subnet_list=[]
    s1="sudo ./CreateBase.sh " + Tenant_name + " wlp3s0 "
    os.system(s1)
    for sub_no in range(No_subnet):
        subnet_name=raw_input("please enter the name of subnet\n")
        while (subnet_name in subnet_list):
            print("subnet_name already exists, Please re-enter the name\n")
            subnet_name=raw_input("please enter the name of subnet\n")


        No_vm=raw_input("Please enter the number of VM required in the subnet\n")
        need_internalFW=raw_input("Do you need internal FW for this subnet? \n press Y for YES \n press N for NO\n")

        TenantDB_list.append(subnet_name)
        TenantDB_list.append(No_vm)
        TenantDB_list.append(need_internalFW)

        temp_sub_no= str(sub_no+1)
        s2=" sudo ./CreateSubnet.sh  " + temp_sub_no + " " +str(tenant_number)+ " " + Tenant_name + " " + str(No_vm)
        os.system(s2)


    TenantDB_string=' '.join(TenantDB_list)
    #c.execute('CREATE TABLE {tn} ({nf} {ft})'.format(tn=table_name1, nf=new_field, ft=field_type))
    with open("VPC_Database.txt","a") as fwrite:
        fwrite.write(TenantDB_string)
        fwrite.write("\n")


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

        for tenants in temp:
            tenants=tenants.split(" ")
            if (tenants[0] == tenantNumberEntered):

                for t_i in range(len(tenants)):

                    if tenants[t_i]==subnetNumberEntered:

                        if (tenants[t_i + 2])=='N':
                            print("\n\n\n\nThis subnet doesnt have internal firewall\n\n\n\n")
                            return()
        rule=raw_input("Enter the rule to be implemented. Please enter the exact rule WITHOUT SUDO : ")
        os.system("sudo ip netns exec "+str(tenantNumberEntered)+"-S-"+str(subnetNumberEntered)+"-FW1 " +str(rule));
        os.system("sudo ip netns exec "+str(tenantNumberEntered)+"-S-"+str(subnetNumberEntered)+"-FW2 " +str(rule));
    else :
        print('Incorrect value entered :(')
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
             #       Press 7: Delete a Tenant                                                                                    #
             #       Press 8: To EXIT                                                                                            #
             #                                                                                                                   #
             #####################################################################################################################"""
        print("WELCOME........Please choose the Task\n\n")
        print(a)

        task_name=int(raw_input(""))

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
            print("Service unavilable right now")
        elif task_name==8:
            break
        else:
            print("INVALID ENTRY\n")
    return()


if __name__ == "__main__":
    main()
