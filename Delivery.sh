#!/bin/bash
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Build Python script program to an application
# create a backup folder
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

version='2.00'

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
ERROR_SH_SUB_ERROR=$(($ERROR_SH+8))
ERROR_SH_INC_VERSION=$(($ERROR_SH+9))

ERROR_GIT_init=$(($ERROR_GIT+1))

aError=$NO_ERROR

#Clear the terminal screen
printf "\033c"

sevenZipPath='/c/Program Files/7-Zip/7z.exe'
sevenZrPath='/usr/bin/7zr'
zipPath='/usr/bin/zip'

currentFolder=$(pwd)

pyInstall_Name=$(basename "$PWD")
pyInstallSpec_Windows="./"$pyInstall_Name"_win.spec"
pyInstallSpec_Linux='./'$pyInstall_Name'_x64.spec'
pyInstallSpec_MacOS="./"$pyInstall_Name"_osx.spec"
pyInstallSpec_Src=""

pyInstallSpec="./"$pyInstall_Name".spec"
pyInstall_fileVersion_lnx="./"$pyInstall_Name".desktop"
pyInstall_fileVersion_osx="./"$pyInstall_Name"_osx.spec"
pyInstall_fileVersion="./"$pyInstall_Name"_version.txt"
pyInstall_pycache="__pycache__"
pyInstall_pycache_sources="src/__pycache__"
pyInstall_build="build"
pyInstall_dist="dist"

pyInstall_getVersion="StringStruct(u'ProductVersion', u'"
pyInstall_version=""
pyInstall_Parameter=""

livraisons_folder="../Livraisons/"


# brew install gnu-sed gawk coreutils findutils

if [[ "$OSTYPE" == "msys" ]]
then
    python_version=$(python --version)
    pyinstaller_version=$(pyinstaller --version)
elif [[ "$OSTYPE" == "darwin"* ]]
then
    python_version=$(python3 --version)
    pyinstaller_version=$(pyinstaller -v)
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    python_version=$(python3 --version)
    pyinstaller_version=$(pyinstaller --version)
else
    echo -e $IRed "Unknown OS" $Color_Off
    exit $ERROR_SH_OS
fi

echo
echo -e $BGreen $pyInstall_Name $Color_Off
echo
echo -e $IGreen "Python version      :" "$python_version" $Color_Off
echo -e $IGreen "PyInstaller version :" "$pyinstaller_version" $Color_Off
echo
if [[ "$OSTYPE" == "msys" ]]
then
    echo -e $IGreen "User name           :" "$USERNAME" $Color_Off
elif [[ "$OSTYPE" == "darwin"* ]]
then
    echo -e $IGreen "User name           :" "$USER" $Color_Off
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    echo -e $IGreen "User name           :" "$USER" $Color_Off
else
    echo -e $IRed "Unknown OS" $Color_Off
    exit $ERROR_SH_OS
fi

echo -e $IGreen "OS type             :" "$OSTYPE" $Color_Off
echo -e $IGreen "Current folder      :" "$currentFolder" $Color_Off

# ##########################################################################################
# https://manytools.org/hacker-tools/ascii-banner/
#
#  ######                                                          
#  #     # #    # # #      #####        #####    ##   ##### ###### 
#  #     # #    # # #      #    #       #    #  #  #    #   #      
#  ######  #    # # #      #    #       #    # #    #   #   #####  
#  #     # #    # # #      #    #       #    # ######   #   #      
#  #     # #    # # #      #    #       #    # #    #   #   #      
#  ######   ####  # ###### #####        #####  #    #   #   ###### 
#
# ##########################################################################################
# Date of the day at format YYYY-MM-DD  WINDOWS
nouvelle_date=$(date +%F)
# Remplace value in file
if [[ "$OSTYPE" == "msys" ]]
then
    sed -i "s/\(StringStruct(u'BuildDate',[[:space:]]*u'\)[0-9\-]\+\('\)/\1$nouvelle_date\2/" "$pyInstall_fileVersion"
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    sed -i "s/\(StringStruct(u'BuildDate', u'\)[0-9-]*\('\)/\1$nouvelle_date\2/" "$pyInstall_fileVersion"
elif [[ "$OSTYPE" == "darwin"* ]]
then
    # Update the build date in-place
    gsed -i "s/\(StringStruct(u'BuildDate',[[:space:]]*u'\)[0-9\-]\+\('\)/\1$nouvelle_date\2/" "$pyInstall_fileVersion"
fi
echo -e $IGreen "Build date          :" "$nouvelle_date" $Color_Off

# ##########################################################################################
# https://manytools.org/hacker-tools/ascii-banner/
#
#  ###                                                              
#   #  #    #  ####     #    # ###### #####   ####  #  ####  #    # 
#   #  ##   # #    #    #    # #      #    # #      # #    # ##   # 
#   #  # #  # #         #    # #####  #    #  ####  # #    # # #  # 
#   #  #  # # #         #    # #      #####       # # #    # #  # # 
#   #  #   ## #    #     #  #  #      #   #  #    # # #    # #   ## 
#  ### #    #  ####       ##   ###### #    #  ####  #  ####  #    # 
#
# ##########################################################################################
# Utilise sed pour capturer les 4 numéros et increase last number by +1  WINDOWS
if [[ "$OSTYPE" == "msys" ]]
then
    sed -E -i'' -e '
    /^[[:space:]]*StringStruct\(u'\''ProductVersion'\'', u'\''[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'\''\)/ {
        s/^([[:space:]]*StringStruct\(u'\''ProductVersion'\'', u'\''[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)('\''\))/echo "\1$((\2+1))\3"/e
    }
    ' "$pyInstall_fileVersion"
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    sed -E -i'' -e '
    /^[[:space:]]*StringStruct\(u'\''ProductVersion'\'', u'\''[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'\''\)/ {
        s/^([[:space:]]*StringStruct\(u'\''ProductVersion'\'', u'\''[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)('\''\))/echo "\1$((\2+1))\3"/e
    }
    ' "$pyInstall_fileVersion"
elif [[ "$OSTYPE" == "darwin"* ]]
then
    gsed -E -i'' -e '
    /^[[:space:]]*StringStruct\(u'\''ProductVersion'\'', u'\''[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'\''\)/ {
        s/^([[:space:]]*StringStruct\(u'\''ProductVersion'\'', u'\''[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)('\''\))/echo "\1$((\2+1))\3"/e
    }
    ' "$pyInstall_fileVersion"
fi
# Get new version to display it
nouvelle_version=$(grep "StringStruct(u'ProductVersion'" "$pyInstall_fileVersion" | sed -E "s/.*u'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)'.*/\1/")
echo -e $IGreen "Version             :" "$nouvelle_version" $Color_Off

# Utilise sed pour capturer les 4 numéros et increase last number by +1  MAC OS X
if [[ "$OSTYPE" == "msys" ]]
then
    sed -E -i'' '
    /^[[:space:]]*version='\''[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'\''/ {
    s/^([[:space:]]*version='\''[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)('\''.*)/echo "\1$((\2+1))\3"/e
    }
    ' "$pyInstall_fileVersion_osx"
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    sed -E -i'' '
    /^[[:space:]]*version='\''[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'\''/ {
    s/^([[:space:]]*version='\''[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)('\''.*)/echo "\1$((\2+1))\3"/e
    }
    ' "$pyInstall_fileVersion_osx"
elif [[ "$OSTYPE" == "darwin"* ]]
then
    gsed -E -i'' '
    /^[[:space:]]*version='\''[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'\''/ {
    s/^([[:space:]]*version='\''[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)('\''.*)/echo "\1$((\2+1))\3"/e
    }
    ' "$pyInstall_fileVersion_osx"
fi

# Utilise sed pour incrémenter la dernière partie (après le tiret)  Linux
if [[ "$OSTYPE" == "msys" ]]
then
    sed -E -i'' '
    /^Version=[0-9]+\.[0-9]+\.[0-9]+-[0-9]+/ {
    s/^(Version=[0-9]+\.[0-9]+\.[0-9]+-)([0-9]+)/echo "\1$((\2+1))"/e
    }
    ' "$pyInstall_fileVersion_lnx"
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    sed -E -i'' '
    /^Version=[0-9]+\.[0-9]+\.[0-9]+-[0-9]+/ {
    s/^(Version=[0-9]+\.[0-9]+\.[0-9]+-)([0-9]+)/echo "\1$((\2+1))"/e
    }
    ' "$pyInstall_fileVersion_lnx"
elif [[ "$OSTYPE" == "darwin"* ]]
then
    gsed -E -i'' '
    /^Version=[0-9]+\.[0-9]+\.[0-9]+-[0-9]+/ {
    s/^(Version=[0-9]+\.[0-9]+\.[0-9]+-)([0-9]+)/echo "\1$((\2+1))"/e
    }
    ' "$pyInstall_fileVersion_lnx"
fi

# git update file in local
# git add $pyInstall_fileVersion_lnx
# git add $pyInstall_fileVersion_osx
# git add $pyInstall_fileVersion
# git commit -m "update BuildDate and ProductVersion field"
echo


# store arguments in a special array 
args=("$@") 
# get number of elements 
ELEMENTS=${#args[@]}
borne=$((ELEMENTS-1))
# echo each element in array  
# echo "Parameter(s) :"
oldparameter=""
release_num=""
for (( i=0; i<$ELEMENTS; i++));
do
    parameter=${args[${i}]}
    # echo " #"$i" : "$parameter
    if [ "$parameter" == "-ev" ] && [ $i -eq $borne ]
    then
        release_num="justBuild"
    else
        if [ "$parameter" != "-ev" ]
        then
            release_num=$release_num" "$parameter
        fi
    fi
done
# echo

if [ "$release_num" == "" ];
then
    echo -e $BGreen "Don't increase release version" $Color_Off
else
    increase_build_number_path=""
    cd ..
    upfolderis=$(pwd)
    if [[ ! -d "$upfolderis""/eversioning""/" ]]
    then
        cd ..
        upfolderis=$(pwd)
        increase_build_number_path=$upfolderis"/eversioning/eversioning/eversioning.py"
        if [[ ! -f "${increase_build_number_path}" ]]
        then
            increase_build_number_path=$upfolderis"/eversioning/eversioning.py"
        fi
    else
        increase_build_number_path=$upfolderis"/eversioning/eversioning/eversioning.py"
        if [[ ! -f "${increase_build_number_path}" ]]
        then
            increase_build_number_path=$upfolderis"/eversioning/eversioning.py"
        fi        
    fi
    cd $currentFolder
    echo -e $Green "UP Folder           :" "$upfolderis" $Color_Off
    echo -e $Green "Release_num         :" "$release_num" $Color_Off
    echo -e $Green "Inc build part with :" "$increase_build_number_path" $Color_Off

    if [[ -f "${increase_build_number_path}" ]]
    then
        echo
        echo -e $Green "in file             :" $currentFolder"/"$pyInstall_Name"_version.txt" $Color_Off
        echo -e $Green "and in file         :" $currentFolder"/"$pyInstall_Name".desktop" $Color_Off
        echo -e $Green "and in file         :" $currentFolder"/"$pyInstall_Name"_osx.spec" $Color_Off
        echo
        if [ "$release_num" == "justBuild" ]
        then
            cmd_content="${increase_build_number_path}"" ""${pyInstall_fileVersion}"
        else
            cmd_content="${increase_build_number_path}"" ""${pyInstall_fileVersion}"" ""$release_num"
        fi
        echo -e $Green "Call                :" "$cmd_content" $Color_Off
        temp=$(python $cmd_content)
        if [ $? -eq 0 ]
        then
            echo -e $Green "$temp" $Color_Off
        else
            exit $ERROR_SH_INC_VERSION
        fi
    else
        echo -e $IRed "eversioning not Found" $Color_Off 
        exit $ERROR_SH_INC_VERSION
    fi
fi
echo

if [[ -f "${pyInstall_fileVersion}" ]]
then
    pyInstall_version="_v""$nouvelle_version"
    echo -e $IGreen "Version             :" "$pyInstall_version" $Color_Off
fi

echo
if [[ -f "$pyInstallSpec" ]]
then
    echo -e $IGreen "Delete spec file    :" "$pyInstallSpec" $Color_Off
    rm -f $pyInstallSpec
    echo
fi

# ##########################################################################################
# https://manytools.org/hacker-tools/ascii-banner/
#
#   ######        ###                                                                                                                            
#   #     # #   #  #  #    #  ####  #####   ##   #      #      ###### #####        #####    ##   #####    ##   #    # ###### ##### ###### #####  
#   #     #  # #   #  ##   # #        #    #  #  #      #      #      #    #       #    #  #  #  #    #  #  #  ##  ## #        #   #      #    # 
#   ######    #    #  # #  #  ####    #   #    # #      #      #####  #    #       #    # #    # #    # #    # # ## # #####    #   #####  #    # 
#   #         #    #  #  # #      #   #   ###### #      #      #      #####        #####  ###### #####  ###### #    # #        #   #      #####  
#   #         #    #  #   ## #    #   #   #    # #      #      #      #   #        #      #    # #   #  #    # #    # #        #   #      #   #  
#   #         #   ### #    #  ####    #   #    # ###### ###### ###### #    #       #      #    # #    # #    # #    # ######   #   ###### #    # 
#
# ##########################################################################################
if [[ "$OSTYPE" == "msys" ]]
then
    # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
    echo -e $IGreen "spec file           :" "$pyInstallSpec_Windows" $Color_Off
    echo
    echo -e $Green "Build Python App for WINDOWS" $Color_Off
    if [[ -f "$pyInstallSpec_Windows" ]]
    then
        pyInstallSpec_Src=$pyInstallSpec_Windows
        # pyInstall_Parameter="-y --clean --log-level DEBUG "$pyInstallSpec
        pyInstall_Parameter="-y --clean --log-level DEBUG "$pyInstallSpec
    else
        echo -e $IRed "File does not exist :" $pyInstallSpec_Windows $Color_Off
        exit $ERROR_SH_OS    
    fi
elif [[ "$OSTYPE" == "darwin"* ]]
then
    # Mac OSX
    echo -e $IGreen "new spec file from  :" "$pyInstallSpec_MacOS" $Color_Off
    echo
    echo -e $Green "Build Python App for MAC OS X" $Color_Off
    if [[ -f "$pyInstallSpec_MacOS" ]]
    then
        pyInstallSpec_Src=$pyInstallSpec_MacOS
        # --version-file ""'$pyInstall_fileVersion'"
        # pyInstall_Parameter="-y -i appIcon_T_512x512.icns "${pyInstall_Name}".py"
        pyInstall_Parameter="-y --clean --log-level DEBUG "$pyInstallSpec
    else
        echo -e $IRed "File does not exist :" $pyInstallSpec_MacOS $Color_Off
        exit $ERROR_SH_OS    
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    # Linux
    echo -e $IGreen "spec file           :" "$pyInstallSpec_Linux" $Color_Off
    echo
    echo -e $Green "Build Python App for LINUX" $Color_Off
    if [[ -f "$pyInstallSpec_Linux" ]]
    then
        pyInstallSpec_Src=$pyInstallSpec_Linux
        pyInstall_Parameter="-y --clean --log-level DEBUG "$pyInstallSpec
        # pyInstall_Parameter="--onefile -y --clean --log-level DEBUG "$pyInstallSpec
    else
        echo -e $IRed "File does not exist :" $pyInstallSpec_Linux $Color_Off
        exit $ERROR_SH_OS    
    fi
else
    echo -e $IRed "Unknown OS :" "$OSTYPE" $Color_Off
    exit $ERROR_SH_OS
fi

echo
echo -e $IGreen "Copy file           :" "$pyInstallSpec_Src" " TO " "$pyInstallSpec" $Color_Off
# CP with option force; preserve attributes; recursive
cp -fp "$pyInstallSpec_Src" "$pyInstallSpec"
if [[ ! -f "$pyInstallSpec" ]]
then
    echo -e $BRed "Missing spec file :" "$pyInstallSpec" $Color_Off
    exit $ERROR_SH_FILE
fi

# Cleaning Folder
echo
if [[ ! -d ${pyInstall_pycache} ]]
then
    echo -e $Green "Create folder       :" "$pyInstall_pycache" $Color_Off
    mkdir -p ${pyInstall_pycache}
else
    echo -e $Green "Delete folder       :" "$pyInstall_pycache" $Color_Off
    rm -frd ${pyInstall_pycache}
    mkdir -p ${pyInstall_pycache}
fi

if [[ ! -d ${pyInstall_pycache_sources} ]]
then
    echo -e $Green "Create folder       :" "$pyInstall_pycache_sources" $Color_Off
    mkdir -p ${pyInstall_pycache_sources}
else
    echo -e $Green "Delete folder       :" "$pyInstall_pycache_sources" $Color_Off
    rm -frd ${pyInstall_pycache_sources}
    mkdir -p ${pyInstall_pycache_sources}
fi

if [[ ! -d ${pyInstall_build} ]]
then
    echo -e $Green "Create folder       :" "$pyInstall_build" $Color_Off
    mkdir -p ${pyInstall_build}
else
    echo -e $Green "Delete folder       :" "$pyInstall_build" $Color_Off
    rm -frd ${pyInstall_build}
    mkdir -p ${pyInstall_build}
fi

# ##########################################################################################
# https://manytools.org/hacker-tools/ascii-banner/
#
#  #                                                             ######        ###                                                        
#  #         ##   #    # #    #  ####  #    # # #    #  ####     #     # #   #  #  #    #  ####  #####   ##   #      #      ###### #####  
#  #        #  #  #    # ##   # #    # #    # # ##   # #    #    #     #  # #   #  ##   # #        #    #  #  #      #      #      #    # 
#  #       #    # #    # # #  # #      ###### # # #  # #         ######    #    #  # #  #  ####    #   #    # #      #      #####  #    # 
#  #       ###### #    # #  # # #      #    # # #  # # #  ###    #         #    #  #  # #      #   #   ###### #      #      #      #####  
#  #       #    # #    # #   ## #    # #    # # #   ## #    #    #         #    #  #   ## #    #   #   #    # #      #      #      #   #  
#  ####### #    #  ####  #    #  ####  #    # # #    #  ####     #         #   ### #    #  ####    #   #    # ###### ###### ###### #    # 
#
# ##########################################################################################
echo
echo -e $IGreen "pyinstaller "$pyInstall_Parameter $Color_Off
echo
PYTHONOPTIMIZE=1 pyinstaller ${pyInstall_Parameter}
echo
if [ $? -eq 0 ]
then
    echo -e $Green "PyInstaller build is done" $Color_Off
    echo
    if [[ "$OSTYPE" == "msys" ]]
    then
        if [ -d ${pyInstall_dist} ] && [ ${pyInstall_version} != "" ]
        then
            echo -e $Green "Rename application   : " $pyInstall_dist"/"$pyInstall_Name".exe" " to " $pyInstall_dist"/"$pyInstall_Name$pyInstall_version".exe"  $Color_Off
            if [[ ! -f $pyInstall_dist"/"$pyInstall_Name".exe" ]]
            then
                echo
                echo -e $BRed "pyinstaller failed ! error =" $?  $Color_Off
                exit $ERROR_SH_FAILED
            fi
            i_number_of_picture=$(pyi-archive_viewer -l "$pyInstall_dist"/"$pyInstall_Name".exe | grep png | grep -c "^")
            if [ $i_number_of_picture -ne 15 ]
            then
                echo
                echo -e $BRed "bad number of pictures =" $i_number_of_picture  $Color_Off
                exit $ERROR_SH_FAILED
            fi
            mv $pyInstall_dist"/"$pyInstall_Name".exe" $pyInstall_dist"/"$pyInstall_Name$pyInstall_version".exe"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]
    then
        if [ -d ${pyInstall_dist} ] && [ ${pyInstall_version} != "" ]
        then
            # ls -alg ./dist
            echo -e $Green "Rename application   : " "./"$pyInstall_dist"/"$pyInstall_Name " to " "./"$pyInstall_dist"/"$pyInstall_Name$pyInstall_version  $Color_Off
            # Application (application/x-shellscript)
            if [[ ! -f "./"$pyInstall_dist"/"$pyInstall_Name ]]
            then
                echo -e $Yellow "Not found" "./"$pyInstall_dist"/"$pyInstall_Name $Color_Off
                echo -e $BRed "pyinstaller failed ! error =" $?  $Color_Off
                exit $ERROR_SH_FAILED
            fi
            i_number_of_picture=$(pyi-archive_viewer -l "$pyInstall_dist"/"$pyInstall_Name" | grep png | grep -c "^")
            if [ $i_number_of_picture -ne 16 ]
            then
                echo
                echo -e $BRed "bad number of pictures =" $i_number_of_picture  $Color_Off
                exit $ERROR_SH_FAILED
            fi
            mv "./"$pyInstall_dist"/"$pyInstall_Name "./"$pyInstall_dist"/"$pyInstall_Name$pyInstall_version

            echo -e $BGreen "Generate .DEB file" $Color_Off
            dos2unix ./deb_create.sh
            echo
            ./deb_create.sh
            if [ $? -ne 0 ]
            then
                exit $ERROR_SH_SUB_ERROR
            fi
            echo
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]
    then
        apps='./dist/'$pyInstall_Name'.app' 
        if [ -d $apps ]
        then
            # Mac OSX
            echo -e $BGreen "Prepare folder dmgContent" $Color_Off
            cd ./dist
            mkdir ./dmgContent
            echo
            cp -Rfp ./$pyInstall_Name.app ./dmgContent/
            cd ..
            echo -e $Green "Generate .DMG file" $Color_Off
            dos2unix ./dmg_create.sh
            echo
            ./dmg_create.sh
            if [ $? -ne 0 ]
            then
                exit $ERROR_SH_SUB_ERROR
            fi
            # echo -e $Green "Exit dmg_create.sh" $Color_Off
            cd ./dist
            rm -R ./dmgContent
            rm -R ./$pyInstall_Name.app
            cd ..
            echo
            echo -e $Green "DMG file is OK" $Color_Off
            echo   
        else
            ls -alGh ./dist
            echo -e $BRed "Application not found" $Color_Off
            exit $ERROR_SH_FILE
        fi
    fi

    echo
    if [[ "$OSTYPE" == "msys" ]]
    then
        # ##########################################################################################
        # https://manytools.org/hacker-tools/ascii-banner/
        #
        #   #####                                       #     #                                                                                                  
        #  #     # #####  ######   ##   ##### ######    #  #  # # #    # #####   ####  #    #  ####     # #    #  ####  #####   ##   #      #      ###### #####  
        #  #       #    # #       #  #    #   #         #  #  # # ##   # #    # #    # #    # #         # ##   # #        #    #  #  #      #      #      #    # 
        #  #       #    # #####  #    #   #   #####     #  #  # # # #  # #    # #    # #    #  ####     # # #  #  ####    #   #    # #      #      #####  #    # 
        #  #       #####  #      ######   #   #         #  #  # # #  # # #    # #    # # ## #      #    # #  # #      #   #   ###### #      #      #      #####  
        #  #     # #   #  #      #    #   #   #         #  #  # # #   ## #    # #    # ##  ## #    #    # #   ## #    #   #   #    # #      #      #      #   #  
        #   #####  #    # ###### #    #   #   ######     ## ##  # #    # #####   ####  #    #  ####     # #    #  ####    #   #    # ###### ###### ###### #    #
        #
        # ##########################################################################################

        # Generate window install with Inno Setup
        if [[ -f "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ]]
        then
            if [[ -f "./Innosetup_create_install.iss" ]]
            then
                echo -e $BGreen "Create Inno Setup installer application" $Color_Off
                echo
                "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "./Innosetup_create_install.iss"
                if [ $? -eq 0 ]
                then
                    if [[ -f "./"$pyInstall_build"/scbeditor2_install.exe" ]]
                    then            
                        mv "./"$pyInstall_build"/scbeditor2_install.exe" "./"$pyInstall_dist"/scbeditor2_install.exe"
                        if [[ -f "./dist/scbeditor2_install.exe" ]]
                        then
                            echo
                            echo -e $Green "Inno Setup installator is created" $Color_Off
                        fi
                    else
                        echo -e $Yellow "Inno Setup "$pyInstall_build"/scbeditor2_install.exe NOT FOUND" $Color_Off
                        exit $ERROR_SH_FILE
                    fi
                else
                    echo -e $BRed "Inno Setup "$pyInstall_build" of install : FAILED on error= " $? $Color_Off
                    exit $ERROR_SH_FILE
                fi
            else
                echo -e $BRed "Inno Setup projet file 'Innosetup_create_install.iss' not present" $Color_Off
                exit $ERROR_SH_FILE                
            fi
        else
            echo -e $BRed "Inno Setup not installed" $Color_Off
            exit $ERROR_SH_FILE
        fi
    fi

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    #   #####                                                                                    
    #  #     # #####  ######   ##   ##### ######      ##   #####   ####  #    # # #    # ######  
    #  #       #    # #       #  #    #   #          #  #  #    # #    # #    # # #    # #       
    #  #       #    # #####  #    #   #   #####     #    # #    # #      ###### # #    # #####   
    #  #       #####  #      ######   #   #         ###### #####  #      #    # # #    # #       
    #  #     # #   #  #      #    #   #   #         #    # #   #  #    # #    # #  #  #  #       
    #   #####  #    # ###### #    #   #   ######    #    # #    #  ####  #    # #   ##   ###### 
    #
    # ##########################################################################################
    # Create the backup folder of delivery 
    echo
    if [ ! -d $livraisons_folder ]
    then
        echo -e $Green "Create folder :" $livraisons_folder $Color_Off    
        mkdir $livraisons_folder
    fi
    targetDir=$livraisons_folder$pyInstall_Name$pyInstall_version
    if [ -d $targetDir ]
	then
        targetDir=$livraisons_folder$pyInstall_Name$pyInstall_version"_SAV"
	fi

    if [ ! -d $targetDir ]
    then
        echo -e $BGreen "Create backup folder :" $targetDir $Color_Off
        mkdir $targetDir
        echo
        sAppName="$currentFolder""/""$pyInstall_dist""/""$pyInstall_Name""$pyInstall_version"
        # echo -e $Green  "sAppName             :" $sAppName $Color_Off

        # Copy the original IIGS application 
        cp -fp "scbeditor.img" "$targetDir"

        cp -fp *.icns "$targetDir"
        cp -fp *.desktop "$targetDir"
        cp -fp *.code-workspace "$targetDir"
        # copy icons in folder /images/. They are integrated in the application by pyInnstaller.
        mkdir -p "$targetDir""/images/"
        find ./images/ -type f -name "*.png" -exec cp {} "$targetDir""/images/" \;   
        # copy manual in folder /Documents.
        cp -fR "./Documents" "$targetDir""/Documents/"
        # copy code source in folder /Documents.
        mkdir -p "$targetDir""/src/"
        find ./src/ -type f -name "*.py" -exec cp {} "$targetDir""/src/" \;   

        cp -fp "README.md" "$targetDir"
        cp -fp "LICENSE" "$targetDir"
        cp -fp "GNU_GPLv3.txt" "$targetDir"
        cp -fp "requirements.txt" "$targetDir"
        cp -fp ".desktop" "$targetDir"

        # history of the development of the project
        if [[ -f "Evolution_Release.md" ]]
        then
            cp -fp "Evolution_Release.md" "$targetDir"
        fi
        # Copy Icon for application
        cp -fp appIcon_x64_T_256x256.gif "$targetDir"
        cp -fp appIcon_T_512x512.ico "$targetDir"
        cp -fp appIcon_T_512x512.icns "$targetDir"
        # Copy Windows Folder icon on my personnal PC only
		if [[ -f "desktop.ini" ]]
		then
			cp -fp desktop.ini "$targetDir"
			cp -fp ScbEditorII_T_512x512.ico "$targetDir"
		fi
        # Copy Python source code
        cp -fp "$pyInstall_Name"".py" "$targetDir"
    	cp -fp *.desktop "$targetDir"
    	cp -fp *.png "$targetDir"
        cp -fp "$pyInstall_Name""_version.txt" "$targetDir"
        cp -fp *.spec "$targetDir"
        rm -f "$currentFolder""/""$targetDir""/""$pyInstall_Name"".spec"
        # Copy script for platforms
        cp -fp *.sh "$targetDir"
        # Copy Quality
        cp -fp Quality_pylint_log.md "$targetDir"
		if [[ -f "unitTestShell.bat" ]]
		then        
            cp -fp unitTestShell.bat "$targetDir"
        fi
        # Copy Inno Setup
        cp Innosetup_* "$targetDir"
        # Compress folder
        echo
        if [[ -f $sevenZipPath ]]
        then
            echo -e $Green "7ZIP backup folder to : " $targetDir".7z" $Color_Off
            # echo -e $Green "$sevenZipPath" a -t7z -mx9 -mmt4 -r -bt $currentFolder"/"$targetDir".7z" $currentFolder"/"$targetDir $Color_Off
            "$sevenZipPath" a -t7z -mx9 -mmt4 -r -bt "$currentFolder""/""$targetDir"".7z" "$currentFolder""/"$targetDir
        elif [[ -f $sevenZrPath ]]
        then
            echo -e $Green "P7ZIP backup folder :" $Color_Off
            sDest=$currentFolder'/'$targetDir".7z"
            sSrc=$currentFolder'/'$targetDir
            echo -e $Green "  from  =" ${sSrc} $Color_Off
            echo -e $Green "  to    =" ${sDest} $Color_Off
            echo
            sleep 1
            # echo -e $Green ${sevenZrPath} a -t7z -mx9 -mmt4 -r -bt ${sDest} ${sSrc} $Color_Off
            ${sevenZrPath} a -t7z -mx9 -mmt4 -bt "$sDest" "$sSrc"
        elif [[ -f $zipPath ]]
        then
            echo -e $Green "ZIP backup folder to : " "$targetDir"".zip" $Color_Off
            sDest=$currentFolder'/'$targetDir".zip"
            sSrc=$currentFolder'/'$targetDir
            echo -e $Green "  from  =" ${sSrc} $Color_Off
            echo -e $Green "  to    =" ${sDest} $Color_Off
            echo
            sleep 1
            # echo -e $Green ${zipPath} -9 -r ${sDest} ${sSrc} $Color_Off
            "$zipPath" -9 -r "$sDest" "$sSrc"
        else
            echo -e $BYellow "No compress application is present" $Color_Off
        fi

        # Create archive to Linux format 
    	echo
        echo -e $Green "TAR archive folder to : " "$targetDir"".tar.gz" $Color_Off
        echo
        tar -czvf "$targetDir".tar.gz "$targetDir"
    else
        echo -e $BYellow "Folder :" $targetDir "already exist." $Color_Off
    fi

    # Cleaning folder
    echo
    echo -e $BGreen "Cleaning" $Color_Off
    echo
    if [[ -f "$pyInstallSpec" ]]
    then
        echo -e $Green "Delete spec file                :" "$pyInstallSpec" $Color_Off
        rm -f $pyInstallSpec
    fi
    echo -e $Green "Delete files and sub folder in  : ./""$pyInstall_build""/" $Color_Off
    echo
    cd "./"$pyInstall_build
    rm -rf ./**
    cd ..

	echo
	echo -e $BGreen "Total build is done with success." $Color_Off
	echo
else
    echo -e $BRed "PyInstaller failed ! error =" $?  $Color_Off
fi

sleep 1  #Wait 1 seconds

exit $NO_ERROR
