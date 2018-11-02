import get_ansible_workers
from os import environ as env
from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ACCHT18.normal"
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."
worker_name = "Group12_Worker"

def find_all_instances():
    relevant_instances = nova.servers.list(search_opts={"name":"Group12"}) #[0]
    for instance in relevant_instances:
        ip = instance.networks[private_net][0]
        name = instance.name
        if worker_name in name:
            print "Worker Instance: ", instance.name, "Has the IP: ", instance.networks[private_net][0]
        else:
            print "Instance: ", instance.name, "Has the IP: ", instance.networks[private_net][0]

def update_ansible_hosts_file(lines):
    f_ansible = open("/etc/ansible/hosts","r+")
    old = f_ansible.read()  # read everything in the file
    f_ansible.seek(0)  # rewind
    f_ansible.write(lines + old)
    f_ansible.close()

def find_new_workers():
    workers_instances = nova.servers.list(search_opts={"name": worker_name})
    cluster_workers = get_ansible_workers.return_workers()
    if len(workers_instances) == len(cluster_workers):
        print "No new workers found in Openstack"
        return False
    else:
        f = open("/etc/hosts","a")
        f_ansible = open("/etc/ansible/hosts","a")
        lines = ""
        print "New worker(s) found in Openstack"
        for index in range(len(workers_instances)):
            worker_instance = workers_instances[index]
            name=worker_instance.name.lower()
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
        f.close()
        f_ansible.close()
        update_ansible_hosts_file(lines)
        return True

find_new_workers()
