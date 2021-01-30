#!/bin/bash
# File: android-interact.sh

PROG_NAME=`python -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$0"`
PROG_DIR=`dirname "$PROG_NAME"`
cd "$PROG_DIR"
echo "WeChat Chat Exporter. Fuck Zhang Xiaolong."
# Please check that your path is the same, since this might be different among devices
RES_DIR="/mnt/sdcard/Android/data/com.tencent.mm/MicroMsg"
#for LineageOS
MM_DIR="/data/data/com.tencent.mm"

echo "Starting rooted adb server..."
adb root

if [[ $1 == "db" || $1 == "res" ]]; then
	echo "Looking for user dir name..."
	sleep 1  	# sometimes adb complains: device not found
	# look for dirname which looks like md5 (32 alpha-numeric chars)
	#for some reason the user ID for the DB and resources are different. fuck you zhangxiaolong
	#this version forgoes support for multiple user.
	userList=$(adb ls /data/data/com.tencent.mm/MicroMsg | cut -f 4 -d ' ' | sed 's/[^0-9a-z]//g' \
		| awk '{if (length() == 32) print}')
	resourceUserList=$(adb ls /mnt/sdcard/Android/data/com.tencent.mm/MicroMsg | cut -f 4 -d ' ' | sed 's/[^0-9a-z]//g' \
		| awk '{if (length() == 32) print}')
	chooseUser=$(echo "$userList" | head -n1)
	numResourceUser=$(echo "$resourceUserList" | wc -l)
	resourceUser=$(echo "$resourceUserList" | head -n1)
	[[ -n $chooseUser ]] || {
		>&2 echo "Could not find user. Please check whether your resource dir is $RES_DIR"
		exit 1
	}
	echo "Found $numUser user(s). User chosen: $chooseUser"

	if [[ $1 == "res" ]]; then
		mkdir -p resource
    (
      cd resource || exit
      echo "Pulling resources... "
      for d in avatar image2 voice2 emoji video sfs; do
        echo "Trying to download $RES_DIR/$resourceUser/$d with busybox ..."
        adb shell "cd $RES_DIR/$resourceUser &&
                   busybox tar czf - $d 2>/dev/null | busybox base64" |
            base64 -di | tar xzf -
        [[ -d $d ]] && continue

        echo "Trying to download $RES_DIR/$resourceUser/$d with tar & base64 ..."
        adb shell "cd $RES_DIR/$resourceUser &&
                   tar czf - $d 2>/dev/null | base64" | base64 -di | tar xzf -
        [[ -d $d ]] && continue

        echo "Trying to download $RES_DIR/$resourceUser/$d with adb pull (slow) ..."
        mkdir -p $d
        (
          cd $d || exit
          adb pull "$RES_DIR/$resourceUser/$d"
        )

        [[ -d $d ]] || {
          echo "Failed to download $RES_DIR/$resourceUser/$d"
        }
      done
      echo "Resource pulled at ./resource"
      echo "Total size: $(du -sh | cut -f1)"
    )
	else
		echo "Pulling database and avatar index file..."
		adb pull $MM_DIR/MicroMsg/$chooseUser/EnMicroMsg.db
		[[ -f EnMicroMsg.db ]] && \
			echo "Database successfully downloaded to EnMicroMsg.db" || {
			>&2 echo "Failed to pull database by adb!"
			exit 1
		}
	fi
	#avatar.index does not exist
else
	echo "Usage: $0 <res|db>"
	exit 1
fi

