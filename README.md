
# **SCB Editor II**

![Alt text](scbeditor2_T_256x256.png "scbeditor2")    ![Alt text](./gplv3-127x51.png "license GPL v3")


_Creation: December 31th, 2023..2026, by Renaud Malaval_  
_Last review: January 3rd, 2026, by Renaud Malaval_

## **Features**

  This is an application to do modification of bmp file to prepare convertion to Apple IIGS pic format file.
  The goal is to increase the number of color used in your pic files with usage of **SCB**.
  This is an help for cross-dev on Linux Mint (Debian and Red Hat package), Mac OS Monterey, Windows.
  BMP file supported are 4 (converted to 8) and 8 bits / per pixels.
  When your bmp files is ready you could convert it with [convm](https://github.com/Malaval-Ren/ConvM)

  :warning: Before usage of **SCB Editor II**, make a backup of your bmp files!

> note : My first release was on Apple IIGS **S.C.B. Editor** version 1.5a
> You could found it in the image scbeditor.img.
> Pascal source code is loozed.

![Alt text](./Documents/presentation.png "SCBEditor II")

## **Documentations**

- [Software overview](Documents/manual.md)
- [Files overview](Documents/Catalog_Files.md)

## **Versions**

- [Quality repport](Quality_pylint_log.md)

## **Notes**

- Linux Mint Xia:
The **Debian** package .deb is created on Linux Mint Xia (v22.1)  
:warning: Not tested. The **Red Hat** package .rpm is converted by [Alien](https://joeyh.name/code/alien/)  

- Mac OSx86 Monterey :
[Homebrew](https://brew.sh/)  

- Windows 11 :
Check it before install it, please  
If your antivirus find some think, send me a mail, please  

- Windows 10 :
:warning: Microsoft Defender found **PUA:Win32/Packunwan** but I think that is an error  
Clamav, Malwarebytes, RogueKiller and Trellix don't found it on the exe file and on my hard drive  
Check it before install it, please  
If your antivirus find some think, send me a mail, please  

- Create Release :
A complete release could be created with "Delivery.sh"  
I'm using it currently for internal usage and testing  
I have to create an ".venv" environment to simplify it  

## **Tools**

- [Python](https://www.python.org/)
  - [Windows 11](https://www.microsoft.com/en-us/software-download/windows11) : 3.12.10 with Tkinter : 8.6.15
  - [Linux Mint v22.1](https://linuxmint.com/) : 3.12.3  with Tkinter : 8.6.15
  - [Mac OSx86 v12.7.6](https://apps.apple.com/fr/app/macos-monterey/id1576738294?mt=12) : 3.13.3 with Tkinter : 9.0.2
- [Python modules](https://pypi.org/)
  - [pip](https://pypi.org/project/pip/)
  - [pylint](https://pypi.org/project/pylint/)
  - [pyinstaller](https://pyinstaller.org/en/stable/)
  - [pillow](https://pypi.org/project/pillow/)
- [Homerew](https://brew.sh/) : A Package Manager for Mac OS
  - Midnight commander : brew install midnight-commander
  - nano : brew install nano
  - dos2unix : brew install dos2unix
  - create-dmg : brew install create-dmg
  - gnu tools : brew install gnu-sed gawk coreutils findutils
  - shell ask gpg code : brew install pinentry
- [Oracle VirtualBox](https://www.virtualbox.org/) : A full virtualization software for x86_64 hardware
- [Visual Studio Code](https://code.visualstudio.com/) : IDE (with somes extensions)
- [Mark Text](https://www.marktext.cc/) : A viewer for markdown file (.md)
- [GIT](https://git-scm.com/) : Distributed version control system
- [Sourcetree](https://sourcetreeapp.com/) : A beautiful Git GUI
- [Inno Setup](https://jrsoftware.org/isinfo.php) : Create on an installor for Windows
- [7-Zip](https://www.7-zip.org/) : A file archiver
- [GIMP](https://www.gimp.org/) : A picture editor
- [Image Magick Display](https://imagemagick.org/) : To convert .png to .icns
- [XnView](https://www.xnview.com/) : To view .icns Mac Os icon file on Windows
- [FlatIcon](https://www.flaticon.com) : Source of wonderful free pictures

## **Development**

### Linux

pip3 install -r requirements.txt

### Windows

pip install -r requirements.txt

### Mac OS

install Homebrew

brew install git
brew install midnight-commander
brew install python
brew install pillow
brew install pylint
brew install pyinstaller
brew install create-dmg
brew install imagemagick
brew install dos2unix
brew install gnu-sed gawk coreutils findutils

### Source code GIT

git clone https://github.com/Malaval-Ren/scbeditor2.git

>note : https://code.visualstudio.com/docs/python/environments

### Source code archive

Decompress the archive file (.zip, .tar.gz)

type command in a shell to start it :

```
python scbeditor2.py
```
or 
```
python3 scbeditor2.py
```

## **Build with Pyinstaller**

### Linux

On a Bash shell version 5.x

type command :
```bash
./Delivery.sh
```

### Mac OS

On a Bash shell version 5.x

type :
```bash
./Delivery.sh
```
### Windows

On a Bash shell version 5.x installed by GIT

Type command :
```bash
./Delivery.sh
```
