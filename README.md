# QTL as a Service

Project webpage: http://www.it.uu.se/research/project/ctrait/QTLaaS

## Summary
We have developed QTL as a Service (QTLaaS) using PruneDIRECT algorithm. QTLaaS automatically deploys an R cluster for using PruneDIRECT, or any statistical analysis in R, over your desired infrastructure.


Three files are required for this method: ansible_install.sh, setup_var.yml,spark_deployment.yml

1. Step 1: Install Ansible using the bash scrip in the file: ansible_install.sh. Configure Ansible hosts.
2. Step 2: Modify the environment variables available in the file: setup_var.yml, if needed.
3. Step 3: For setup deployment run: spark_deployment.yml as root which is the actual file that contains all the installation restructures for all the components of our architecture. For example # ansible-playbook -s spark_deployment.yml, where -s is the sudo flag. 

We will soon provide a demo through our project webpage using the SNIC cloud resources. Any user can try QTLaaS over a few nodes in our cloud setting. For larger computation, one can download QTLaaS from the github repository and it automatically deploys the desired number of nodes over an infrastructure.
