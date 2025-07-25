#!/bin/bash
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Create a xxxx.dmg file for project application installation
#
# from : https://github.com/create-dmg/create-dmg
#
# Copyright (C) 2020-2025 Renaud Malaval <renaud.malaval@free.fr>
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

version='1.33'

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

ERROR_GIT_init=$(($ERROR_GIT+1))

aError=$NO_ERROR

if [[ "$OSTYPE" != "darwin"* ]]
then
    echo -e $BRed "Create a dmg file is only on Mac OS X" $Color_Off
    exit $ERROR_SH_OS
fi

#Clear the terminal screen
# printf "\033c"
pyInstall_Name=$(basename "$PWD")
pyInstall_getVersion="StringStruct(u'ProductVersion', u'"
pyInstall_version=""

echo
echo -e $BGreen "Get version from    :" "./""$pyInstall_Name""_version.txt" $Color_Off
echo

pyInstall_fileVersion="./"$pyInstall_Name"_version.txt"
if [ -f "$pyInstall_fileVersion" ]
then
    the_version=$(grep "StringStruct(u'ProductVersion'" "$pyInstall_fileVersion" | sed -E "s/.*u'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)'.*/\1/")
    pyInstall_version="_v""$the_version"
    echo -e $BGreen "Version found is    :" "$pyInstall_version" $Color_Off
    echo
else
    echo -e $BRed "File version not found    : " "$pyInstall_fileVersion" $Color_Off
    exit $ERROR_SH_FILE
fi

if [[ "$pyInstall_version" == "" ]]
then
    echo -e $BRed "Version not found in file : " "$pyInstall_fileVersion" $Color_Off
    exit $ERROR_SH_FILE
fi

# --background "installer_background.png" \
test -f $pyInstall_Name$pyInstall_version".dmg" && rm $pyInstall_Name$pyInstall_version".dmg"

create-dmg \
    --volname "${pyInstall_Name}${pyInstall_version}" \
    --volicon "dmg_icon_T_512x512.icns" \
    --background "dmg_LGM-612x408.png" \
    --window-pos 200 120 \
    --window-size 612 408 \
    --icon-size 128 \
    --eula "./GNU_GPLv3.txt" \
    --icon "${pyInstall_Name}.app" 144 158 \
    --hide-extension "${pyInstall_Name}.app" \
    --hdiutil-verbose \
    --app-drop-link 468 158 \
    "./dist/${pyInstall_Name}${pyInstall_version}.dmg" \
    "./dist/dmgContent/"

echo
if [ $? -eq 0 ]
then
    echo -e $BGreen "✅ create-dmg is done" $Color_Off
else
    echo -e $BRed "❌ create-dmg failed ! error =" $?  $Color_Off
    error= $?
fi

exit $error
