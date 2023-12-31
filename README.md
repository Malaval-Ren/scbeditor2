
# **SCB Editor II**

![Alt text](scbeditor2_T_256x256.png "scbeditor2")

The application scbeditor2 for Python main project file, pyinstaller file and Linux file

The goal is to increase 5 files (XXX is the name of the project) :

- XXX_version.txt
- XXX.py
- XXX.desktop (if file exist)
- unitTestShell.bat (if file exist)
- XXX_osx.spec

For a Release delivered (git branch master) :

 major.minor.maintenance.build (example: 1.1.3.99)

For a Debug (git branch develop) :

 minor.maintenance.build (example: 1.3.99)

> note : XXX must be the same name of the folder and the main project file

&nbsp;

## **Versions**

- [Release](Evolution_Release.md) **NOT CREATED**
- [Quality](Quality_pylint_log.md)

&nbsp;

## **Documentations**

- [Software overview](Documents/scbeditor2.md)
- [Files overview](Documents/Catalog_Files.md)

&nbsp;

## **Usage is done from a bash script**

```bash
currentFolder=$(pwd)
pyInstall_Name=$(basename "$PWD")
pyInstall_fileVersion="./"$pyInstall_Name"_version.txt"

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
    if [ ! -d "$upfolderis""/scbeditor2""/" ]
    then
        cd ..
        upfolderis=$(pwd)
        increase_build_number_path=$upfolderis"/scbeditor2/scbeditor2/scbeditor2.py"
    else
        increase_build_number_path=$upfolderis"/scbeditor2/scbeditor2/scbeditor2.py"
    fi
    cd $currentFolder
    echo -e $Green "UP Folder           :" "$upfolderis" $Color_Off
    echo -e $Green "Release_num         :" "$release_num" $Color_Off
    echo -e $Green "Inc build part with :" "$increase_build_number_path" $Color_Off

    if [ -f "${increase_build_number_path}" ]
    then
        echo
        echo -e $Green "in file             :" $currentFolder"/"$pyInstall_Name"_version.txt" $Color_Off
        echo -e $Green "and in file         :" $currentFolder"/"$pyInstall_Name".py" $Color_Off
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
        exit $ERROR_SH_INC_VERSION
    fi
fi
echo
```

&nbsp;

## **Tools Mandatory**

- [Python](https://www.python.org/) with Tcl/Tk
  - Windows 10 : 3.12.1
  - [Linux Mint](https://linuxmint.com/) : default release installed with your distribution (min 3.12.1)  
    This package is mandatory : 'sudo apt-get install python3-tk'
  - Mac OSx 10.15.7 : 3.12.1
- Modules
  - pyinstaller
