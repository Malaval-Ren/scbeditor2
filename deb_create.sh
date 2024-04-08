#!/bin/bash
#
# create a xxxx.deb file for project application installation
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Create a xxxx.deb file for project application installation
#
# Copyright (C) 2020-2024 Renaud Malaval <renaud.malaval@free.fr>
# 
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Special thank's to :
# from :
#		http://sdz.tdct.org/sdz/creer-un-paquet-deb.html
#		https://alp.developpez.com/tutoriels/debian/creer-paquet/
#		https://forum-francophone-linuxmint.fr/viewtopic.php?t=13312
#		https://wiki.visionduweb.fr/index.php?title=Programmer_un_paquet_logiciel_pour_Debian#Cr.C3.A9er_le_sous_dossier_DEBIAN
#		https://betterprogramming.pub/how-to-create-a-basic-debian-package-927be001ad80
#
# .rpm
#		Problem not solved to convert script 'preinst'
#		https://stackoverflow.com/questions/54480244/how-to-easily-convert-debian-script-to-rpm-script

version='1.45'

# definition all colors and styles to use with an echo

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

# Underline
UBlack='\033[4;30m'       # Black
URed='\033[4;31m'         # Red
UGreen='\033[4;32m'       # Green
UYellow='\033[4;33m'      # Yellow
UBlue='\033[4;34m'        # Blue
UPurple='\033[4;35m'      # Purple
UCyan='\033[4;36m'        # Cyan
UWhite='\033[4;37m'       # White

# Background
On_Black='\033[40m'       # Black
On_Red='\033[41m'         # Red
On_Green='\033[42m'       # Green
On_Yellow='\033[43m'      # Yellow
On_Blue='\033[44m'        # Blue
On_Purple='\033[45m'      # Purple
On_Cyan='\033[46m'        # Cyan
On_White='\033[47m'       # White

# High Intensity
IBlack='\033[0;90m'       # Black
IRed='\033[0;91m'         # Red
IGreen='\033[0;92m'       # Green
IYellow='\033[0;93m'      # Yellow
IBlue='\033[0;94m'        # Blue
IPurple='\033[0;95m'      # Purple
ICyan='\033[0;96m'        # Cyan
IWhite='\033[0;97m'       # White

# Bold High Intensity
BIBlack='\033[1;90m'      # Black
BIRed='\033[1;91m'        # Red
BIGreen='\033[1;92m'      # Green
BIYellow='\033[1;93m'     # Yellow
BIBlue='\033[1;94m'       # Blue
BIPurple='\033[1;95m'     # Purple
BICyan='\033[1;96m'       # Cyan
BIWhite='\033[1;97m'      # White

# High Intensity backgrounds
On_IBlack='\033[0;100m'   # Black
On_IRed='\033[0;101m'     # Red
On_IGreen='\033[0;102m'   # Green
On_IYellow='\033[0;103m'  # Yellow
On_IBlue='\033[0;104m'    # Blue
On_IPurple='\033[0;105m'  # Purple
On_ICyan='\033[0;106m'    # Cyan
On_IWhite='\033[0;107m'   # White

#
# how to do a if of numeric or string
#            Shell Script
#Boolean Operator     Numeric     String
#===================  =======     ======
#Equals                 -eq        =
#Not Equals             -ne        !=
#Greater Than           -gt        >
#Less Than              -lt        <
#Greater or Equals      -ge        >=
#Less Than or Equals    -le        <=


#define exit value 0 succes, other failed
NO_ERROR=0

ERROR_SH=9
ERROR_GIT=49
ERROR_DEBUG=199

ERROR_SH_param=$(($ERROR_SH+1))
ERROR_SH_deprend=$(($ERROR_SH+2))
ERROR_SH_reorg=$(($ERROR_SH+3))
ERROR_SH_folder=$(($ERROR_SH+4))
ERROR_SH_OS=$(($ERROR_SH+5))
ERROR_SH_FILE=$(($ERROR_SH+6))
ERROR_SH_FAILED=$(($ERROR_SH+7))

ERROR_GIT_init=$(($ERROR_GIT+1))

aError=$NO_ERROR

# How to install package 
# sudo apt-get install ./scbeditor2_2.2.9-27_amd64.deb
#
# How to uninstall package
# sudo apt-get remove ./scbeditor2_2.2.9-27_amd64.deb

# How to uninstall package manualy
# sudo rm -r /usr/bin/scbeditor2
# sudo rm -r /usr/share/applications/scbeditor2.desktop
# sudo rm -r /usr/share/icons/scbeditor2.png

# if problem
# sudo dpkg -i ./scbeditor2_2.2.9-27_amd64.deb
# sudo dpkg -r scbeditor2

#Clear the terminal screen
# printf "\033c"
pyInstall_Name=$(basename "$PWD")
pyInstall_getVersion="StringStruct(u'ProductVersion', u'"
pyInstall_version=""
user_name=$USERNAME

echo -e $BGreen "Project name        :" "$pyInstall_Name" $Color_Off
echo
echo -e $Green "Get version from    :" "./"$pyInstall_Name"_version.txt" $Color_Off
echo
arch=$(uname -m)
if [[ $arch == "x86_64" ]]
then
	# Convert Architecture to avoid non compatibility with tool "dpkg-deb"
	arch="amd64"
fi
echo -e $Green "Architecture        :" "$arch" $Color_Off

pyInstall_fileVersion="./""$pyInstall_Name""_version.txt"
if [ -f "$pyInstall_fileVersion" ]
then
	# echo
    # echo -e $Green "getVersion          :" "$pyInstall_getVersion" $Color_Off
    # echo -e $Green "fileVersion         :" "$pyInstall_fileVersion" $Color_Off
	# echo
    temp=$(grep -F "$pyInstall_getVersion" "${pyInstall_fileVersion}")
    # echo -e $Green "grep result         :" "$temp" $Color_Off
    tempNoSpace=$(echo $temp | tr -d ' ')

    temp=${tempNoSpace: -1}
    hex="$(printf '%s' "$temp" | xxd -pu)"
    if [[ "$hex" == "0d" ]]
    then
        # remove this char '\r' at end of string
        refLineLen=${#tempNoSpace}
        refLineLen=$(($refLineLen - 1))
        tempNoSpace=${tempNoSpace:0:refLineLen}
    fi

    # echo -e $Green "result no space     :" "$tempNoSpace" $Color_Off
    refLineLen=${#pyInstall_getVersion}
    # echo -e $Green "getVersion len      :" "$refLineLen" $Color_Off
    refLineLen=$(($refLineLen - 1))
	tempNoSpaceLen=${#tempNoSpace}
    # echo -e $Green "tempNoSpaceLen len  :" "$tempNoSpaceLen" $Color_Off
	calcVersionLen=$(($tempNoSpaceLen - $refLineLen))
	calcVersionLen=$(($calcVersionLen - 4))
    # echo -e $Green "calcVersionLen len  :" "$calcVersionLen" $Color_Off
	# echo -e $Green  "tempNoSpace         :" "$tempNoSpace"":""$refLineLen"":""$calcVersionLen" $Color_Off
    versionTemp=${tempNoSpace:refLineLen:calcVersionLen}
    # echo -e $Green "result filter       :" "$tversionTemp" $Color_Off

    versionLen=${#versionTemp}
    # echo -e $Green "len result filter   :" "$versionLen" $Color_Off
    if [ $versionLen -eq $calcVersionLen ]
    then
        pyInstall_version="_v""$versionTemp"
        echo -e $Green "Version found is    :" "$pyInstall_version" $Color_Off
    else
        pyInstall_version=""
        echo -e $BYellow "Version is no available" $Color_Off 
    fi
    echo
else
	echo
    echo -e $BRed "File version not found    :" "$pyInstall_fileVersion" $Color_Off
    exit $ERROR_SH_FILE
fi

if [[ "$pyInstall_version" == "" ]]
then
    echo -e $BRed "Version not found in file :" "$pyInstall_fileVersion" $Color_Off
    exit $ERROR_SH_FILE
fi

if [[ ! -d ./dist ]]
then
	mkdir ./dist
fi

if [[ ! "$OSTYPE" == "linux-gnu"* ]]
then
    echo -e $BRed "This script is only to run on Linux" $Color_Off
    exit $ERROR_SH_FAILED
fi

versionLen=${#versionTemp}
versionLen=$(($versionLen + 1))
counter=-1
lastChar='@'
while [ $lastChar != '.' ]
do
	lastChar=${versionTemp:$counter:1}
	counter=$(($counter - 1))
	# echo -e $Green "charracter #""$counter"" is :" "$lastChar" $Color_Off
	if (("$counter" > 10)) || (("$counter" < -10))
	then
	    echo -e $BRed "ERROR versionTemp is not compatible :" "versionTemp" $Color_Off		
		exit $ERROR_SH_FAILED
	fi
done
# replace last char . by a -
counter=$(($counter + 1))
versionIndex=$(($versionLen + $counter))
# echo ${versionTemp:versionIndex-1}-${versionTemp:versionIndex}
versionTemp="${versionTemp:0:versionIndex-1}-${versionTemp:versionIndex}"
echo -e $Green "Package version is  :" "$versionTemp" $Color_Off

if [[ "$pyInstall_version" != "" ]]
then
	# Linux Mint
	echo -e $BGreen "Generating .deb file" $Color_Off
	# set name to lower case
	appName=$(echo "${pyInstall_Name,,}")
    # display $appName
    echo -e $Green "appName             :" "$appName" $Color_Off
    refLineLen=${#appName}
    echo -e $Green "len (appName)       :" "$refLineLen" $Color_Off
    # Replace character _ by -
    if [[ "$appName" == *" "* ]]
    then
        pkgAppName="${appName:0:8-1}-${appName:8}"
        pkgAppName="${pkgAppName:0:13-1}-${pkgAppName:13}"
    else
        pkgAppName="$appName"
    fi
	# Naming : Use the package-name_VersionNumber-RevisionNumber_DebianArchitecture
	packageSrcBase="./""$pkgAppName""_""$versionTemp""_""$arch"
	echo -e $Green "packageSrcBase      :" "$packageSrcBase" $Color_Off
	cd ./dist
    # ls -alg
	if [[ -d "$packageSrcBase" ]]
	then
		rm -R $packageSrcBase
	fi
	mkdir $packageSrcBase
	mkdir $packageSrcBase/usr
	mkdir $packageSrcBase/usr/bin
	mkdir $packageSrcBase/usr/share/
	mkdir $packageSrcBase/usr/share/applications/
	mkdir $packageSrcBase/usr/share/icons/
	srcName="../""$appName"".desktop"
	destopSize=$(stat -c %s $srcName)
	cp -fp $srcName $packageSrcBase/usr/share/applications/
	echo -e $Green "desktop             :" "$srcName" $Color_Off
	srcName="../""$appName""_T_256x256.png"
	iconSize=$(stat -c %s $srcName)
	cp -fp $srcName $packageSrcBase/usr/share/icons/$appName".png"
	echo -e $Green "icon                :" "$srcName" $Color_Off

	# echo
	# echo $PWD
	# echo
	srcName="./""$pyInstall_Name""$pyInstall_version"
	# srcName="./""$pyInstall_Name"
	echo -e $Green "srcName             :" "$srcName" $Color_Off
	echo -e $Green "dstName             :" $packageSrcBase"/usr/bin/" $Color_Off

	cp -fpr $srcName $packageSrcBase/usr/bin/
    if [ $? -ne 0 ]
    then
        echo -e $BRed "ERROR Failed to do copy of" "$srcName" "to" "$packageSrcBase""/usr/bin/" $Color_Off
        exit $ERROR_SH_FILE
    fi
	srcName="$packageSrcBase""/usr/bin/""$pyInstall_Name""$pyInstall_version"

	echo -e $Green "appName             :" "$appName" $Color_Off
	dstName="$packageSrcBase""/usr/bin/""$appName"
	echo -e $Green "srcName             :" "$srcName" $Color_Off
	echo -e $Green "dstName             :" "$dstName" $Color_Off
	mv $srcName $dstName
    if [ $? -ne 0 ]
    then
        echo -e $BRed "ERROR Failed to do rename of" "$srcName" "to" "$dstName" $Color_Off
        exit $ERROR_SH_FILE
    fi
	mkdir $packageSrcBase/DEBIAN
	# Create control file
	# appSize=`du -k "$dstName" | cut -f1`
	appSize=$(stat -c %s $dstName)
	let totalSize=$destopSize+$iconSize+$appSize
	echo -e $Green "Total Size          :" "$totalSize"" octets" $Color_Off	
	originStyle=$(uname -o)
	originName=$(lsb_release -d -s)
	OSOrigin="$originStyle"" ""$originName"
	echo -e $Green "OS Origin           :" "$OSOrigin" $Color_Off	

	TargetControlFile="$packageSrcBase""/DEBIAN/control"
	echo -e "Package: ""$appName" > "$TargetControlFile"
	echo -e "Version: ""$versionTemp" >> "$TargetControlFile"
	echo -e "Section: base" >> "$TargetControlFile"
	echo -e "Priority: optional" >> "$TargetControlFile"
	echo -e "Installed-Size: ""$appSize" >> "$TargetControlFile"
	echo -e "Origin: ""$OSOrigin" >> "$TargetControlFile"
	echo -e "Architecture: ""$arch" >> "$TargetControlFile"
	echo -e "Depends: bash" >> "$TargetControlFile"
	echo -e "Maintainer: Renaud Malaval <renaud.malaval@free.fr>" >> "$TargetControlFile"
	echo -e "Description: This application prepare .bmp file to be converted to .pic file for Apple IIGS." >> "$TargetControlFile"
	echo -e "Homepage: http://renaud.malaval.free.fr/index.html" >> "$TargetControlFile"

	# Create preinst file
	TargetPreinstFile="$packageSrcBase""/DEBIAN/preinst"
	echo -e "#!/bin/bash" > "$TargetPreinstFile"
	echo -e "# file name preinst" >> "$TargetPreinstFile"
	echo -e "# Pre-install script for ""$appName"". This removes old versions of ""$appName""." >> "$TargetPreinstFile"
	echo -e "" >> "$TargetPreinstFile"
	echo -e "echo \"Looking for old versions of ""$appName"" ..."\" >> "$TargetPreinstFile"
	echo -e "" >> "$TargetPreinstFile"
	echo -e "if [ -f \"/usr/bin/"$appName"\" ];then" >> "$TargetPreinstFile"
	echo -e "	sudo rm -f /usr/bin/""$appName" >> "$TargetPreinstFile"
    echo -e "	echo \"Removed old ""$appName"" from /usr/bin/ ..."\" >> "$TargetPreinstFile"
    echo -e "fi" >> "$TargetPreinstFile"
	echo -e "" >> "$TargetPreinstFile"
	echo -e "if [ -f \"/usr/share/applications/"$appName"".desktop"\" ];then" >> "$TargetPreinstFile"
	echo -e "	sudo rm -f /usr/share/applications/""$appName"".desktop" >> "$TargetPreinstFile"
    echo -e "	echo \"Removed old ""$appName"".desktop"" from /usr/share/applications/ ..."\" >> "$TargetPreinstFile"
    echo -e "fi" >> "$TargetPreinstFile"
	echo -e "" >> "$TargetPreinstFile"
	echo -e "if [ -f \"/usr/share/icons/"$appName"".png"\" ];then" >> "$TargetPreinstFile"
	echo -e "	sudo rm -f /usr/share/icons/""$appName"".png" >> "$TargetPreinstFile"
    echo -e "	echo \"Removed old ""$appName"".png"" from /usr/share/icons/ ..."\" >> "$TargetPreinstFile"
    echo -e "fi" >> "$TargetPreinstFile"
	echo -e "" >> "$TargetPreinstFile"
	echo -e "exit 0" >> "$TargetPreinstFile"
	echo -e "" >> "$TargetPreinstFile"

	# To check folder code is :
	# echo -e "if [ -d "/usr/share/""$appName" ];then" >> "$TargetPreinstFile"
    # echo -e "	sudo rm -rf /usr/share/""$appName" >> "$TargetPreinstFile"
	# echo -e "	echo \"Removed old ""$appName"" from /usr/share/ ..." >> "$TargetPreinstFile"
	# echo -e "fi" >> "$TargetPreinstFile" >> "$TargetPreinstFile"
	# echo -e "" >> "$TargetPreinstFile"

	# We need to change the owner:group for all files and permissions for the main file and the preinst file:
	sudo chown root:root -R "$packageSrcBase"
	sudo chmod 755 "$packageSrcBase""/usr/bin/""$appName"
	sudo chmod 755 "$packageSrcBase""/DEBIAN/preinst"	

	echo $USERNAME
	username=$()

	echo
	echo -e $BGreen "Package name        :" "$packageSrcBase"".deb" $Color_Off
	echo
	dpkg-deb -v --nocheck --build $packageSrcBase
    aError=$?
	if [ $aError -ne 0 ] || [ ! -f "$packageSrcBase"".deb" ]  
	then
		sudo chown $user_name:$user_name -R "$packageSrcBase"
		echo
		echo -e $BRed "dpkg-deb failed ! error =" "$aError"  $Color_Off
		exit $ERROR_SH_FAILED
	fi
	echo
	echo -e $BGreen "Build is done with success." $Color_Off
	echo

	echo -e $BGreen "Converting .deb to .rpm file" $Color_Off
	echo
	# -c "$packageSrcBase""/DEBIAN/preinst"
	sudo alien -r -k $packageSrcBase".deb" 
    if [ $? -ne 0 ]
    then
		sudo chown $user_name:$user_name -R "$packageSrcBase"
        echo -e $BRed "Failed to do convert .deb to .rpm ! error =" $? $Color_Off
        exit $ERROR_SH_FILE
    fi
	sudo chown $user_name:$user_name -R "$packageSrcBase"
	sudo chown $user_name:$user_name ./scbeditor2_2.2.9-27_amd64.deb
	sudo chown $user_name:$user_name ./scbeditor2-2.2.9-27.x86_64.rpm
	echo
	echo -e $BGreen "Convert is done with success." $Color_Off
	cd ..
    exit $NO_ERROR
else
    echo -e $BRed "Create a deb file is only on Linux Mint." $Color_Off
fi
