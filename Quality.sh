#!/bin/bash
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Does quality analyse of all *.py file in a project with tool Pylint
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

version='1.29'

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

aError=$NO_ERROR

#Clear the terminal screen
printf "\033c"

currentFolder=$(pwd)

pyInstall_Name=$(basename "$PWD")

pyInstall_getVersion="StringStruct(u'ProductVersion', u'"
pyInstall_version=""
pyInstall_Parameter=""
pylint_log="Quality_pylint_log.md"
pylint_rules="# pylint: disable="
pylint_tmp="Quality_pylint_log.txt"

if [[ "$OSTYPE" == "msys" ]]
then
	temp=$(python --version)
	refLineLen=${#temp}
	refLineLen=$refLineLen-7
    python_version=${temp:7:$refLineLen}
    pyinstaller_version=$(pyinstaller --version)
	# Get from string multi line the version
	temp=$(pylint --version)
	firstLine=$(sed -n "1{p;q}" <<<"$temp")
	refLineLen=${#firstLine}
	refLineLen=$refLineLen-7
	pylint_version=${temp:7:$refLineLen}
	temp=$(perl -v)
	perl_version=${temp:44:6}
	bash_version="${BASH_VERSION}"
	os_version="${OSTYPE}"
elif [[ "$OSTYPE" == "darwin"* ]]
then
    python_version=$(python3 --version)
    pyinstaller_version=$(pyinstaller -v)
	temp=$(pylint --version)
	# Get from string the version
	pylint_version=${temp:7:6}
	temp=$(perl -v)
	perl_version=${temp:44:6}
	bash_version="${BASH_VERSION}"
	os_version="${OSTYPE}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    python_version=$(python3 --version)
    pyinstaller_version=$(pyinstaller --version)
	# Get from string multi line the version
	temp=$(pylint --version)
	firstLine=$(sed -n "1{p;q}" <<<"$temp")
	refLineLen=${#firstLine}
	refLineLen=$refLineLen-7
	pylint_version=${temp:7:$refLineLen}
	temp=$(perl -v)
	perl_version=${temp:44:6}
	bash_version="${BASH_VERSION}"
	if [ -f /etc/os-release ]
	then
		. /etc/os-release
		os_version="${NAME} ${VERSION}"
	else
		temp=$(lsb_release -d | cut -f2)
		if [ -! z "${temp}" ]
		then
			os_version=$temp
		else
			os_version="${BASH_VERSION}"
		fi
	fi
else
    echo -e $IRed "Unknown OS" $Color_Off
    exit $ERROR_SH_OS
fi

echo -e "# **Quality of :** **"$pyInstall_Name"**"> "$pylint_log"
echo -e "" >> "$pylint_log"
echo -e "## *""Context""*" >> "$pylint_log"
echo -e "" >> "$pylint_log"
echo -e "date : " $(date) >> "$pylint_log"
echo -e "" >> "$pylint_log"
echo -e "| *Tools* | *version* |" >> "$pylint_log"
echo -e "| -------------- | -------------------------------- |" >> "$pylint_log"
echo -e "| Python |" "$python_version"" |" >> "$pylint_log"
echo -e "| PyInstaller |" "$pyinstaller_version"" |" >> "$pylint_log"
echo -e "| Pylint |" "$pylint_version"" |" >> "$pylint_log"
echo -e "| Perl |" "$perl_version"" |" >> "$pylint_log"
echo -e "| Bash |" "$bash_version"" |" >> "$pylint_log"
echo -e "| System |" "$os_version"" |" >> "$pylint_log"

echo -e $BGreen $pyInstall_Name $Color_Off
echo -e $Green "Date                :" $(date) $Color_Off
echo -e $Green "Python version      :" "$python_version" $Color_Off
echo -e $Green "PyInstaller version :" "$pyinstaller_version" $Color_Off
echo -e $Green "Pylint version      :" "$pylint_version" $Color_Off
echo -e $Green "perl version        :" "$perl_version" $Color_Off
echo -e $Green "bash version        :" "$bash_version" $Color_Off

echo
if [[ "$OSTYPE" == "msys" ]]
then
    echo -e $Green "User name           :" "$USERNAME" $Color_Off
elif [[ "$OSTYPE" == "darwin"* ]]
then
    echo -e $Green "User name           :" "$USER" $Color_Off
elif [[ "$OSTYPE" == "linux-gnu"* ]]
then
    echo -e $Green "User name           :" "$USER" $Color_Off
else
    echo -e $BRed "Unknown OS" $Color_Off
    exit $ERROR_SH_OS
fi

echo -e $Green "OS Type             :" "$os_version" $Color_Off
echo -e $Green "Current Folder      :" "$currentFolder" $Color_Off
echo

pyInstall_fileVersion="./"$pyInstall_Name"_version.txt"
echo -e $Green "Get version from    :" $pyInstall_fileVersion $Color_Off

if [ -f "$pyInstall_fileVersion" ]
then
    temp=$(grep -F "$pyInstall_getVersion" "$pyInstall_fileVersion")
    # echo -e $Green "grep line result    :" "'""$temp""'" $Color_Off
    tempNoSpace=$(echo $temp | tr -d ' ')
    # echo -e $Green "result no space     :" "$tempNoSpace" $Color_Off
    refLineLen=${#pyInstall_getVersion}
    # echo -e $Green "refLineLen          :" "$refLineLen" $Color_Off
    refLineLen=$refLineLen-1
    # echo -e $Green "refLineLen-1        :" "$refLineLen" $Color_Off
	for (( i = $refLineLen; i < ${#tempNoSpace}; ++i)); do
	    # echo -e $Green "${tempNoSpace:$i:1}" $Color_Off
		if [[ ${tempNoSpace:$i:1} != ")" ]]
		then
			tempver=$tempver${tempNoSpace:$i:1}
		else
			break
		fi
	done

	if [[ ${tempver:0:1} != "'" ]]
	then
	    # echo -e $Green "last char is a cote" $Color_Off
		if [[ "$OSTYPE" == "darwin"* ]]
		then
			v2=${tempver:0:$((${#tempver} - 1))}
			tempver=$v2
		else
			tempver=${tempver::-1}
		fi
	fi
	# echo -e "version : ""$tempver""\n" >> "$pylint_log"
	echo -e "| **Project** |  |" >> "$pylint_log"	
	echo -e "| "$pyInstall_Name" |" "$tempver"" |" >> "$pylint_log"
	echo -e "" >> "$pylint_log"
	echo -e $Green "Version             :" $BGreen"$tempver" $Color_Off
	echo
else
	echo
fi

# zone for test

# exit $NO_ERROR

# Declare an array variable of folder to do nothing
declare -a folder_ignore=( "./.git/" "./.venv/" "./.vscode/" "./build/" "./images/" "./Documents/" )

# Work start here
echo -e $BGreen "Pylint analyse files :" $Color_Off
echo
filecount=0
notetotal=0.0
tempval=0.0
for i in $(find . -type f \( -iname "*.py" ! -iname "__*.py" \) ); 
do
	# Loop through each folder_ignore we does nothink
	drop_it=0
	for folder in "${folder_ignore[@]}"
	do
		if [[ "$i" =~ "$folder" ]]
		then
			drop_it=1
			break
		fi
	done

	if [ $drop_it -eq 0 ]
	then
		echo -e $BGreen " ""$i" $Color_Off
		# pylint --rcfile=pylint_config -E $i
		echo -e "&nbsp;\n" >> "$pylint_log"
		echo -e "## *""$i""*" >> "$pylint_log"
		echo -e "" >> "$pylint_log"
		temp=$(grep -F "$pylint_rules" "$i")
		if [[ ! "$temp" == "" ]]
		then
			echo
			# echo -e "temp          :" "$temp"
			PylintWarningArr=()
			while read -r line; do
				PylintWarningArr+=("$line")
			done <<< "$temp"

			# Do a layout to display Pylint rule one by lines in .md 
			totalnumberofrules=$(echo ${PylintWarningArr[@]} | grep -o '# ' | wc -l)
			for k in "${PylintWarningArr[@]}"
			do
				tempNoSpace=$(echo $k | tr -s '# ' '  ')
				echo -e $Green "$tempNoSpace" $Color_Off
				if [ $totalnumberofrules -gt 1 ]
				then
					spaces="  "
				else
					spaces=""
				fi
				echo -e ">""$tempNoSpace""$spaces" >> "$pylint_log"
			done

			# Qdd separator if error are present
			numberOfLine="${#PylintWarningArr[@]}"
			borne=0
			# echo -e $Green "numberOfLine :" "$numberOfLine" $Color_Off		
			# echo -e $Green "borne        :" "$borne" $Color_Off		
			if [ "$numberOfLine" -gt "$borne" ]
			then
				echo
				echo -e "  " >> "$pylint_log"
			fi
			# echo
		fi

		# Do the Pylint analyse
		pylint $i > "$pylint_tmp"
		pylint_error=$?

		# Do a layout to display element name with only 3 * in .md 
		# echo -e $Green "pylint_tmp           :" "$pylint_tmp" $Color_Off
		numberoflines=$(wc -l < "$pylint_tmp")
		# echo -e $Green "numberoflines        :" "$numberoflines" $Color_Off
		firstline=$(head -1 < "$pylint_tmp")
		# echo -e $Green "firstline            :" "$firstline" $Color_Off
		short="${firstline:0:14}"
		# echo -e $Green "short                :" "$short" $Color_Off
		if [ "$short" == "************* " ]
		then
			firstline=${firstline:10}
			firstline=$firstline"  "
			# echo -e $Green "firstline            :" "$firstline" $Color_Off
			echo -e "$firstline" >> "$pylint_log"
			echo -e "" >> "$pylint_log"
			# echo -e $Green "numberoflines +      :" "$numberoflines" $Color_Off
			let "numberoflines -= 1"
			let "numberoflines *= -1"
			# echo -e $Green "numberoflines +      :" "$numberoflines" $Color_Off
			# Do a layout to display Pylint info in .md 
			tagpart=$(tail $numberoflines < "$pylint_tmp" )
			# echo -e $Green "tagpart              :" $Color_Off
			# echo -e $Green "$tagpart" $Color_Off
			echo -e "$tagpart" >> "$pylint_log"
			echo -e "" >> "$pylint_log"
		else
			# echo -e $Green "numberoflines -      :" "$numberoflines" $Color_Off
			let "numberoflines -= 1"
			let "numberoflines *= -1"
			# echo -e $Green "numberoflines -      :" "$numberoflines" $Color_Off
			# Do a layout to display Pylint info in .md 
			tagpart=$(tail $numberoflines < "$pylint_tmp" )
			# echo -e $Green "tagpart              :" $Color_Off
			# echo -e $Green "$tagpart" $Color_Off
			echo -e "$tagpart" >> "$pylint_log"
			echo -e "" >> "$pylint_log"
		fi
		rm "$pylint_tmp"


		# Get last line of log file to display it and compute note 
		tag=$(tail -2 < "$pylint_log" )
		# echo -e $Green "tag                  :" $Color_Off
		# echo -e $Green "$tag" $Color_Off
		if [[ "$OSTYPE" == "darwin"* ]]
		then
			v2=${tag:0:$((${#tag} - 1))}
			echo -e $Green '\t '$v2 $Color_Off
		else
			echo -e $Green '\t '${tag::-1} $Color_Off
		fi
		# Get from line the note
		newnote=${tag:28:5}
		# echo -e $Green "newnote              :" "$newnote" $Color_Off	
		lastchar=${newnote: -1}
		if [ $lastchar == '/' ]
		then
			if [[ "$OSTYPE" == "darwin"* ]]
			then
				v2=${newnote:0:$((${#newnote} - 1))}
				newnote=$v2
			else
				newnote=${newnote::-1}
			fi
		fi
		tempval=$(perl -E "say $notetotal+$newnote")
		notetotal=$tempval
		if [ $pylint_error -ne 0 ]
		then
			if [ $pylint_error -eq 1 ]
			then
				echo -e $Red '\t '"errors type = fatal message" $Color_Off
			elif [ $pylint_error -eq 2 ]
			then
				echo -e $Yellow '\t '"errors type = error message" $Color_Off
			elif [ $pylint_error -eq 4 ]
			then
				echo -e $Purple '\t '"errors type = warning message" $Color_Off
			elif [ $pylint_error -eq 8 ]
			then
				echo -e $Green '\t '"errors type = refactor message" $Color_Off
			elif [ $pylint_error -eq 16 ]
			then
				echo -e $Cyan '\t '"errors type = convention message" $Color_Off
			else
				echo -e $White '\t '"errors type =" "$pylint_error" "(usage error)" $Color_Off
			fi
		fi
		echo
		# note : does nothing : somefile,colorized
		# pylint --output-format=json:somefile,colorized $i >> "$pylint_log"".json"
		let "filecount += 1"
	fi

done

echo -e $BGreen "Pylint files analyzed = ""$filecount"  $Color_Off
echo
medium=$(perl -E "say $notetotal/$filecount")
mediumcut=${medium:0:5}
echo -e $BGreen "Quality medium note  = ""$mediumcut"" / 10"  $Color_Off

echo -e "&nbsp;\n" >> "$pylint_log"
echo -e "## **Quality** :" >> "$pylint_log"
echo -e "**note = ""$mediumcut"" / 10**" >> "$pylint_log"
echo -e "" >> "$pylint_log"

# echo -e "&nbsp;\n" >> "$pylint_log"
# echo -e "## **Tools** :" >> "$pylint_log"
# echo -e "  | *name* | *version* |" >> "$pylint_log"
# echo -e "  | ----- | :---: |" >> "$pylint_log"
# echo -e "  | **Python** | ""$python_version"" |" >> "$pylint_log"
# echo -e "  | **PyInstaller** | ""$pyinstaller_version"" |" >> "$pylint_log"
# echo -e "  | **Pylint** | ""$pylint_version"" |" >> "$pylint_log"
# echo -e "  | **Perl** | ""$perl_version"" |" >> "$pylint_log"
# echo -e "  | **Bash** | ""$bash_version"" |" >> "$pylint_log"

sleep 1  #Wait 1 seconds

exit $NO_ERROR
