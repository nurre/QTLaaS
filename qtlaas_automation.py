import logging
from os import system
import get_ansible_workers
from novaclient import client
from os import environ as env
from keystoneauth1 import loading
from keystoneauth1 import session

# Setting up logging parameters
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up cloud configuration parameters
flavor = "ACCHT18.normal"
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"

loader = loading.get_plugin_loader('password')

# Authorizing user from global variables
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
logger.info("__ACC__: Successfully completed User Authorization.")
worker_name = "Group12_Worker"


# Simple function to print all Group12 relevant instances
def find_all_instances():
    relevant_instances = nova.servers.list(search_opts={"name":"Group12"}) #[0]
    for instance in relevant_instances:
        ip = instance.networks[private_net][0]
        name = instance.name
        if worker_name in name:
            print "Worker Instance: ", name, "Has the IP: ", ip
        else:
            print "Instance: ", name, "Has the IP: ", ip


# Simple function to update the file /etc/ansible/hosts
def update_ansible_hosts_file(lines):
    try:
        f_ansible = open("/etc/ansible/hosts", "r+")
    except:
        logger.error("__ACC__:Something went wrong while trying to open the file /etc/ansible/hosts. Make sure you "
                     "have permissions to open this file and try again. ")
        return False
    old = f_ansible.read()
    f_ansible.seek(0)
    f_ansible.write(lines + old)
    f_ansible.close()
    return True

# Responsible for detecting new relevant workers in the cloud, updating the hosts files with the correct IPs and names,
# and copying the id_rsa.pub from the master to the new workers' authorized_keys file
# Return:
#          False -> if no new workers were detected or an error occured.
#          True -> if new workers were detected and successfully updated.
def find_new_workers():
    logger.info("__ACC__: Looking for new workers...")
    workers_instances = nova.servers.list(search_opts={"name": worker_name})
    cluster_workers = get_ansible_workers.return_workers()
    if len(workers_instances) == len(cluster_workers):
        logger.info("__ACC__: No new workers found in Openstack.")
        return False
    else:
        try:
            f = open("/etc/hosts","a")
        except:
            logger.error("__ACC__:Something went wrong while trying to open the file /etc/hosts. Make sure you "
                         "have permissions to open this file and try again. ")
            return False
        try:
            f_ansible = open("/etc/ansible/hosts","a")
        except:
            logger.error("__ACC__:Something went wrong while trying to open the file /etc/ansible/hosts. Make sure you "
                         "have permissions to open this file and try again. ")
            return False
        logger.info("__ACC__:New worker(s) successfully detected in Openstack.")
        lines = ""
        for index in range(len(workers_instances)):
            try:
                worker_instance = workers_instances[index]
                name = worker_instance.name.lower()
                string_compare = "spark"+name[name.find("worker"):]
                if string_compare in cluster_workers:
                    continue
                else:
                    ip = worker_instance.networks[private_net][0]
                    line = ip + " " + string_compare + "\n"
                    f.write(line)
                    ansible_line = string_compare + " ansible_connection=ssh ansible_user=ubuntu\n"
                    f_ansible.write(ansible_line)
                    ansible_start_line = string_compare + " ansible_ssh_host=" + ip + "\n"
                    lines += ansible_start_line
                    try:
                        linux_cmd = 'ssh ubuntu@' + string_compare + \
                                    '"cat >> ~/.ssh/authorized_keys" < ~/.ssh/id_rsa.pub'
                        system(linux_cmd)
                    except:
                        logger.error("__ACC__:Something went wrong while adding the master's public key "
                                     "to the instance: " + string_compare + "'s Authorized_keys. "
                                                                            "Skipping this instance.")
                        logger.error('__ACC__: Try to run the command manually: '
                                    'ssh ubuntu@sparkworker2 "cat >> ~/.ssh/authorized_keys" < ~/.ssh/id_rsa.pub')
                        continue

            except:
                logger.error("__ACC__:Something went wrong while checking the instance: "+workers_instances[index] +
                             ". Skipping this instance.")
                continue
        f.close()
        f_ansible.close()
        return update_ansible_hosts_file(lines)

find_new_workers()
