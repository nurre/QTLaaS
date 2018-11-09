#!/usr/bin/env bash
source SNIC.sh
python -c 'from qtlaas_automation import create_worker_snapshot; create_worker_snapshot(instance_name="Group12_Worker1")'
python -c 'from qtlaas_automation import find_new_workers; find_new_workers()'
eval `ssh-agent -s`
ssh-add group12.pem
python run_linux_cmds.py