#!/usr/bin/env bash
source SNIC.sh
python -c 'from qtlaas_automation import create_new_instance; create_new_instance(instance_name="Group12_Worker1")'
python -c 'from qtlaas_automation import find_new_workers; find_new_workers()'
eval `ssh-agent -s`
ssh-add group12.pem
python run_linux_cmds.py