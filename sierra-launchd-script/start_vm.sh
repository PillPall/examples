#! /bin/bash
#
# Startup script for MacOSx Sierra to start and stop a Virtual Machine
# everytime this scripts gots executed or receives a SIGTERM SIGKILL SIGINT SIGHUP Signal
#

# Variables
VM_ID=d9782aed-e997-42b1-96f8-1cdb1ee3d55c
Mount_PATH=/Users/mbloch/projects
NFS_IP=192.168.98.101
NFS_PATH=/data/projects
NFS_OPTS=noowners,nolockd,resvport,hard,intr,rw,tcp,nfc

StartVM()
{
        echo "Start VM"
        /usr/local/bin/VBoxManage startvm ${VM_ID} --type headless
        echo ${?}
	sleep 10
	MountNFS
	echo "All done"
	Background
}

StopVM()
{
	UmountNFS
        echo "shutdown VM"
        /usr/local/bin/VBoxManage controlvm ${VM_ID} acpipowerbutton
        echo ${?}
}

MountNFS()
{
	i=0
	err_nfs=1
	if mount |grep projects > /dev/null; then
		echo "Already mounted"
	else
		while [ ${i} -lt 120 ]; do
			if [ ${err_nfs} -gt 0 ]; then
				echo "Mount NFS"
				sudo /sbin/mount -t nfs -o ${NFS_OPTS} ${NFS_IP}:${NFS_PATH} ${Mount_PATH}
				err_nfs=$(echo $?)
				echo ${err_nfs}
				sleep 1
				i=$[$i+1]
			else
				echo "Mount done"
				i=256
			fi
		done
	fi
}

UmountNFS()
{
        if mount |grep projects > /dev/null; then
		echo "Unmount NFS"
                sudo /sbin/umount ${Mount_PATH}
        fi
}

Handler()
{
	echo $(date)
	#
	# Condition check if a VM with given VM ID is already running
	# Yes stop it, no start it
	#
	/bin/ps -Af|grep ${VM_ID}|grep -v grep
	err=$(echo $?)
	if [ ${err} -gt 0 ]; then
		StartVM
	else
		StopVM
	fi
}

Background()
{
	tail -f /dev/null &
	wait $!
}

trap StopVM SIGTERM SIGKILL SIGINT SIGHUP

Handler;
