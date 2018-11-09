# QTL as a Service Group 12

Project webpage: http://www.it.uu.se/research/project/ctrait/QTLaaS

## Summary
We have developed a cluster that deploys QTL as a Service (QTLaaS) in an OpenStack Cloud. QTLaaS automatically deploys an R cluster for using PruneDIRECT, or any statistical analysis in R, over your desired infrastructure. Where we chose OpenStack as the base for the Infrastructure.
We create a RESTFUL API to create, resize and decommission the QTL platform on request in a horizontally scalable system. 

2 files are required for this project: `group12.pem` and `SNIC.sh`.
In order to start up the cluster please follow the Setup details.

## Setup details
We need to have at least one node up and running and acting as the master node and the server. Which is the point of this setup. Where at the end we will have a connected cluster with 1 Master node (acting as Flask server, Spark Master, and Ansible Master) and 1 Worker node.
1. Make sure of the following:
    * You have OpenStack installed on your local machine or that you are already inside a Virtual Machine inside OpenStack. And that you have access to the Infrastructure.
    * Your credentials for OpenStack's Cloud Project are available for authentication in your local machine with the name `SNIC.sh`.
    Which later you should have it copied into the Master node you can successfully ssh into the master node. You can copy it by running: `scp -i group12.pem SNIC.sh ubuntu@130.238.29.82:/home/ubuntu/`
    * Openstack's Cloud Project has a keypair with the name `goup12`. You can check using CLI command: `openstack keypair list`.  
    If you can't locate it, then you can simply create a new keypair using the CLI command `openstack keypair create group12`.
    Which later you should have it copied into the Master node you can successfully ssh into the master node. You can copy it by running: `scp -i group12.pem group12.pem ubuntu@130.238.29.82:/home/ubuntu`
2. Clone this repo on your machine using: 
    `git clone https://github.com/nurre/QTLaaS.git`.
3. Run the command following command to create a master node: 
    `python -c 'from qtlaas_automation import create_new_instance; create_new_instance(master_name="Group12_Master", master=True)'`
4. Assign a floating IP to the master node just created:
    * To list the floating IPs availalable run `openstack ip floating list` and locate the Floating IPs with `None` in the **"Fixed IP Address"** Column and **"Port"**.
    * Assign that IP to the new instance created using CLI:
        `nova add-floating-ip Group12_Master 130.xxx.xx.xx`.
5. SSH into the master node using the following commands:
    * `ssh-add group12.pem` (the same key referenced and/or created in step 1).
    * `ssh ubuntu@130.xxx.xx.xx` (the smae IP obtained from Step 3).
6. Clone this repo in the Master Node using:
    `git clone https://github.com/nurre/QTLaaS.git`.
7. `cd QTLaaS` to get into the project's directory and run `sudo chmod +x setup_master.sh` to  create an executable file from the `setup_master.sh` file.
9. Finally run `./setup_master.sh` to create a worker and setup the master node with spark cluster and ansible. => **This should be done with the REST API.**
10. Make sure the following ports are open on Spark Master node, 60060 for Jupyter Hub (external access), 7077 Spark Context (internal access), 8080 Spark Web UI (internal access).

Please note that steps 1 to 4 can be done manually using OpenStack's Horizon (Dashboard).
