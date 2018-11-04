import logging
from os import system

# Setting up logging parameters
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_linux_cmds():
    system("eval `ssh-agent -s`")
    system("ssh-add group12.pem")
    f = open("linux_commands.txt","r")
    linux_cmds = f.readlines()
    for line in linux_cmds:
        command = line.strip()
        try:
            system(command)
        except:
            logger.error("__ACC__:Something went wrong while attempting to run: " + linux_cmds + "Skipping this instance")
            logger.error('__ACC__: Try to run the command manually.')
            continue
run_linux_cmds()

