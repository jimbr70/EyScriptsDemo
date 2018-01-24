import os, sys
import time
import logging
import socket
import requests


timestr = time.strftime("%Y%m%d-%H%M%S")
newpath = r'/tmp/csd'
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

# Download Scripts/Files
for scr_num in range(1, int(qsscript_count) +1):
    script_name = 'qsscript{0}_url'.format(str(scr_num))
    logging.info("processing {0}".format(script_name))
    script_url = os.environ[script_name]
    if script_url != 'tbd' and not '.exe' in script_url:
        script_name = script_url.rsplit('/', 1)[-1]
        logging.info("Processing %s" % script_name)
        try:
            getthis = "curl --ntlm --user '%s:%s' '%s' -o %s" % (qsuname, qspword, script_url, script_name)
            os.system(getthis)
            if script_name.endswith('.sh'):
                os.system('chmod 775 %s' % script_name)
        except:
            logging.error('Failed to process file. %s' % sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

# Process Execute Command
if qsexecute_command != 'none':
    try:
        logging.info('Executing %s ' % qsexecute_command)
        exec_results = os.system(qsexecute_command)
        logging.info(exec_results)
        logging.info('execution complete.')
    except:
        logging.error('Failed to successfully execute command.  %s' % sys.exc_info()[0])
        raise Exception(sys.exc_info()[0])

# create metadatda file
logging.info('Creating metadata file.')
metafile = open("/tmp/csd/rsvn-meta-data.txt","w+")
metafile.writelines("rsvnId: %s \r\n" % reservation_id)
metafile.writelines("ftp_srvr: %s \r\n" % ftpsrvr)
metafile.writelines("ftp_user: %s \r\n" % ftpuser)
metafile.writelines("ftp_pass: %s \r\n" % ftppass)
metafile.writelines("ftp_hostkey: %s \r\n" % ftphostkey)
metafile.writelines("resource_list: %s \r\n" % resource_list)
metafile.close()

# Push log remote using a mount to a windows share
logging.info('Mounting windows share')
mountup = "wuser='Qu@l!R0cks#@!'\n"
mountup += "srusr='" + qspword + "'\n"
mountup += "mkdir /tmp/csd/RemoteLogs\n"
mountup += "chmod 775 RemoteLogs\n"
mountup += "echo $wuser | sudo -S mount -t cifs -o username=L.CMFCS.01,password=$srusr,domain=et.lab,dir_mode=0777,file_mode=0777 //10.254.34.70/TestShell/ ./RemoteLogs\n"
mountup += "ls /tmp/csd/RemoteLogs\n"
mountfile = open('mountShare.sh', 'w+')
mountfile.write(mountup)
mountfile.close()
mountperm = os.system('chmod 775 mountShare.sh')
mountchk = os.popen('./mountShare.sh').read().replace('\n', ' ')

if not reservation_id in mountchk:
    os.system('mkdir ./RemoteLogs/%s' % reservation_id)

mountup = "cp " + logfilename + ' /home/wuser/RemoteLogs/' + reservation_id + '/\n'
mountup += "ls /home/wuser/RemoteLogs/' + reservation_id + '/\n"
mountchk = os.popen(mountup).read().replace('\n', ' ')
logging.info(mountchk)

# unmount share
umount = "wuser='Qu@l!R0cks#@!'\n"
umount += 'echo $wuser | sudo -S umount -f -l ./RemoteLogs/\n'
os.system(umount)

logging.info('Script Complete')
