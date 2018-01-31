import os
import sys
import time
import logging
import platform
import socket
import requests


timestr = time.strftime("%Y%m%d-%H%M%S")
newpath = r'/tmp/csd'
if not os.path.exists(newpath):
    os.makedirs(newpath)
    os.system('cd /tmp/csd')
logfilename = newpath + '/' + socket.gethostname() + '_linux_deploy_' + timestr + '.txt'
logging.basicConfig(filename=logfilename,level=logging.DEBUG, format='%(asctime)s %(message)s')

# Log env vars
logging.info('linux_deploy.py =====V0.1====== ')
for key in os.environ.keys():
    logging.info("%30s %s " % (key,os.environ[key]))

qsscript_count = 0
qsuname = ''
qspword = ''
qsexecute_command = ''
reservation_id = ''
resource_list = ''
ftpsrvr = ''
ftpuser = ''
ftppass = ''
ftphostkey = ''

# Load variables from env vars
try:
    qsscript_count = os.environ["qsscript_count"]
except:
    logging.warn("no env var found for qsscript_count")
try:
    qsuname = os.environ["qsuname"]
except:
    logging.warn("no env var found for qsuname")
try:
    qspword = os.environ["qspword"]
except:
    logging.warn("no env var found for qspword")
try:
    qsexecute_command = os.environ["qsexecute_command"]
except:
    logging.warn("no env var found for qsexecute_command")
try:
    reservation_id = os.environ["reservation_id"]
except:
    logging.warn("no env var found for reservation_id")
try:
    ftpsrvr = os.environ["ftpsrvr"]
except:
    logging.warn("no env var found for ftpsrvr")
try:
    ftpuser = os.environ["ftpuser"]
except:
    logging.warn("no env var found for ftpuser")
try:
    ftppass = os.environ["ftppass"]
except:
    logging.warn("no env var found for ftppass")
try:
    ftphostkey = os.environ["ftphostkey"]
except:
    logging.warn("no env var found for ftphostkey")
try:
    resource_list = os.environ["resource_list"]
except:
    logging.warn("no env var found for resource_list")

# Connect to share
try:
    newpath = r'/tmp/csd/RemoteLogs'
    if not os.path.exists(newpath):
        os.makedirs(newpath)    
    mountup = "chmod 775 /tmp/csd/RemoteLogs\n"
    mountup += "wuser='Qu@l!R0cks#@!'\n"
    mountup += "srusr='" + qspword + "'\n"
    mountup += "echo $wuser | sudo -S mount -t cifs -o username=L.CMFCS.01,password=$srusr,domain=et.lab," \
               "dir_mode=0777,file_mode=0777 //" + ftpsrvr + "/remotelogs/ /tmp/csd/RemoteLogs\n"
    mountup += "ls /tmp/csd/RemoteLogs\n"
    mountcmds = open('/tmp/csd/mnt.sh', 'w+')
    mountcmds.write(mountup)
    mountcmds.close()
    mountperm = os.system('chmod 775 /tmp/csd/mnt.sh')
    mountchk = os.popen('/tmp/csd/mnt.sh').read().replace('\n', ' ')
    logging.info("Connected to share.")
except:
    logging.error('Failed to connect to share. %s' % sys.exc_info()[0])
    raise Exception(sys.exc_info()[0])

# If Ubuntu, use curl.  Else for red hat and suse, install python pip, request_ntlm
whichLinux = platform.linux_distribution()
if not 'Ubuntu' in whichLinux[0]:
    # Red Hat or SuSE assumed
    try:
        newpath = r'/tmp/csd/py-files'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        logging.info('get-pip....')
        gets_pip  = os.system('cp /tmp/csd/RemoteLogs/ForLinux/get-pip.py /tmp/csd/py-files/')
        inst_pip  = os.system("echo 'Qu@l!R0cks#@!' | sudo -S python /tmp/csd/py-files/get-pip.py")
        logging.info('install requests_ntlm...')
        inst_ntlm = os.system("echo 'Qu@l!R0cks#@!' | sudo -S pip install requests_ntlm")
        logging.info('Libs installed...')
        from requests_ntlm import HttpNtlmAuth
        logging.info('Imports complete')
    except:
        logging.error('Failed to install libs. %s' % sys.exc_info()[0])
        raise Exception(sys.exc_info()[0])
    
# Download Scripts/Files
for scr_num in range(1, int(qsscript_count) +1):
    script_name = 'qsscript{0}_url'.format(str(scr_num))
    logging.info("Checking {0}".format(script_name))
    script_url = os.environ[script_name]
    if script_url != 'tbd' and not '.exe' in script_url:
        script_name = script_url.rsplit('/', 1)[-1]
        logging.info("Processing %s" % script_name)
        try:
            if not 'Ubuntu' in whichLinux[0]:
                session = requests.Session()
                session.auth = HttpNtlmAuth(qsuname,qspword)
                content = session.get(script_url)
                # save content to file
                save_to = open(("/tmp/csd/%s" % script_name), "w+")
                save_to.write(content.content)
                save_to.close()
            else:
                curlcmd = "curl --ntlm --user '%s':'%s' '%s' -o /tmp/csd/%s" % (qsuname, qspword, script_url, script_name)
                logging.info("curlcmd: %s" % curlcmd)
                curlgo = os.system(curlcmd)
                logging.info("curl result: %s " % curlgo)
                
            if script_name.endswith('.sh'):
                logging.info("Changing file permissions to 775")
                chmod = os.system('chmod 775 /tmp/csd/%s' % script_name)
                if chmod != 0:
                    logging.error("Could not chmod .sh script  %s" % script_name)
                    raise Execption(sys.exc_info()[0])
        except:
            logging.error('Failed to process file. %s' % sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

# Process Execute Command
try:
    logging.info('Executing %s ' % qsexecute_command)
    # exec_results = subprocess.call([qsexecute_command]) #
    exec_results = os.popen(qsexecute_command).read()
    logging.info(exec_results)
    logging.info('execution complete... did it work?')
except:
    logging.error('Failed to successfully execute command.  %s' % sys.exc_info()[0])
    raise Exception(sys.exc_info()[0])

# create metadatda file
try:
    metafile = open("/tmp/csd/rsvn-meta-data.txt","w+")
    metafile.writelines("rsvnId: %s \r\n" % reservation_id)
    metafile.writelines("ftp_srvr: %s \r\n" % ftpsrvr)
    metafile.writelines("ftp_user: %s \r\n" % ftpuser)
    metafile.writelines("ftp_pass: %s \r\n" % ftppass)
    metafile.writelines("ftp_hostkey: %s \r\n" % ftphostkey)
    metafile.writelines("resource_list: %s \r\n" % resource_list)
    metafile.close()
    logging.info("Meta-data file created")
except:
    logging.error('Failed to create meta-data file.  %s' % sys.exc_info()[0])
    raise Exception(sys.exc_info()[0])

# Push log remote using a mount to a windows share
if not reservation_id in mountchk:
    os.system('mkdir /tmp/csd/RemoteLogs/%s' % reservation_id)
mountup = "cp " + logfilename + ' /tmp/csd/RemoteLogs/' + reservation_id + '/\n'
mountup += "ls /tmp/csd/RemoteLogs/" + reservation_id + '/\n'
mountchk = os.popen(mountup).read().replace('\n', ' ')
if 'linux_deploy' in mountchk:
    logging.info("Pushed log %s" % mountchk)
else:
    logging.error("Failed to push log to server.")

# unmount share
try:
    unmount = "echo 'Qu@l!R0cks#@!' | sudo -S umount -f -l ./RemoteLogs"
    logging.info(unmount)
    unmrslt = os.popen(unmount).read()
    logging.info(unmrslt)
except:
    logging.error('Failed to unmont share. %s   %s' % (unmrslt, sys.exc_info()[0]))
    raise Exception(sys.exc_info()[0])

logging.info("End of Script")
