; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "scbeditor2"
#define MyAppVersion "2.8.15.107"
#define MyAppPublisher "Disk Crack band"
#define MyAppExeName MyAppName + "_v" + MyAppVersion + ".exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{FDCC3A87-5C4D-413B-BD67-CD9B181C557A}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion=1.0.3.0
;AppVerName={#MyAppName} {#MyAppVersion}
AppCopyright=Copyright @ 2023..2024 {#MyAppPublisher}, Renaud Malaval
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=GNU_GPLv3.txt
InfoBeforeFile=Innosetup_begin.txt
InfoAfterFile=Innosetup_end.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=build
OutputBaseFilename=scbeditor2_install
SetupIconFile="appIcon_T_512x512.ico"
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

