# QTL as a Service

Project webpage: http://www.it.uu.se/research/project/ctrait/QTLaaS

## Summary
We have developed QTL as a Service (QTLaaS) using PruneDIRECT algorithm. QTLaaS automatically deploys an R cluster for using PruneDIRECT, or any statistical analysis in R, over your desired infrastructure.
 
Three files are required for this method: `ansible_install.sh, setup_var.yml,spark_deployment.yml`

Note: Following commands have been tested on Ubuntu 16.04.  
  
1. Step 1: Install Ansible using the bash script, `ansible_install.sh`.
2. Step 2: Modify the environment variables available in the file: `setup_var.yml`, if needed.
3. Step 3: For setup deployment, execute: `spark_deployment.yml` as root which is the actual file that contains the installation setups for all the components of QTLaaS platform. Command: `# ansible-playbook -s spark_deployment.yml`, where `-s` is the sudo flag. 

We will soon provide a demo through our project webpage using the SNIC cloud resources. Any user can try QTLaaS over a few nodes in our cloud setting. For larger computation, one can download QTLaaS from the github repository and it automatically deploys the desired number of nodes over an infrastructure.

## Setup details

1. Setup up at least 3 nodes, one for the Ansible Master, one for the Spark Master, and at least one for the Spark Worker. 
2. Install Ansible using the bash script in the file: `ansible_install.sh`.
3. Add the IP-address/hostnames of Spark Master and Spark Worker to 
`/etc/hosts`
in Ansible Master node.
4. Generate a key and copy its public part to `~/.ssh/authorized_keys` in all the Spark nodes.

For more information: https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04 (Step-1 - 4)

5. Edit `/etc/ansible/hosts` using `example-hosts-file` available in the reprository. (Add `[sparkmaster]` followed by the name of sparkmaster node in the next line. Add `[sparkworker]` followed by the names of sparkworkers in the next lines, one per line).
6. Modify the environment variables available in the file: setup_var.yml, if needed.
7. Run `ansible-playbook -s spark_deployment.yml`, where `-s` is the sudo flag.
8. Make sure the following ports are open on Spark Master node, `60060` for Jupyter Hub, `7077` Spark Context, `8080` Spark Web UI.
9. Now you can access following services: 
`http://sparkmaster:60060`
`http://sparkmaster:8080`
10. Use `example-sparkR` file to make sure your setup is working. 

After all the steps above, Jupiter, Spark Master and R will be installed in Spark Master, and Spark Worker and R is installed in all Spark Workers.

##How to add nodes
In order to add new nodes to your already configured cluster, you should just add the new hosts to the Ansible hosts file, under [sparkworker] tag.

