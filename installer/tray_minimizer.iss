; TrayMinimizer 인스톨러 (Inno Setup 6.3 이상)
;
; 빌드 방법:  installer.bat   (pyproject.toml 의 버전을 읽어 iscc 를 실행)
; 결과물:     installer\Output\TrayMinimizer_Setup_<버전>.exe
;
; 사전 조건:  PyInstaller onedir 빌드 결과가 out\tray_minimizer\ 에 있어야 한다.

#define AppName "TrayMinimizer"
; 버전은 pyproject.toml 이 기준이며, installer.bat 가 /DAppVersion 으로 전달한다.
#ifndef AppVersion
  #error AppVersion 이 정의되지 않았습니다. installer.bat 로 빌드하세요.
#endif
; PyInstaller 빌드 결과 폴더(프로젝트 루트 기준)와 실행 파일 이름. 빌드 이름이 다르면 수정한다.
#define DistDir "..\out\tray_minimizer"
#define AppExeName "tray_minimizer.exe"
; 설정 데이터 폴더(%APPDATA% 아래). app/config/settings_repository.py 의 경로와 같아야 한다.
#define DataDirName "TrayMinimizer"

; Inno Setup 에 한국어 번역 파일이 있을 때만 한국어를 추가한다.
#if FileExists(AddBackslash(CompilerPath) + "Languages\Korean.isl")
  #define HasKorean
#endif
#if FileExists(SourcePath + "..\ico\tray_minimizer.ico")
  #define HasSetupIcon
#endif

[Setup]
; 같은 앱으로 인식하기 위한 고유 ID. 한 번 배포한 뒤에는 바꾸지 않는다.
AppId={{B3F1C2A4-7D58-4E0B-9A63-5C2E8F41D7A9}
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={autopf}\{#AppName}
DisableProgramGroupPage=yes
; 1. 라이선스 동의 페이지 (동의해야 다음으로 진행)
LicenseFile=..\LICENSE
; 2. 시작 시 "모든 사용자용 / 현재 사용자용" 선택 창 표시. 설치 경로 지정 페이지는 기본 제공.
;    모든 사용자용 선택 시에만 관리자 권한을 요청한다.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; '설치된 앱' 목록 등록(제거 정보)과 아이콘
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
#ifdef HasSetupIcon
SetupIconFile=..\ico\tray_minimizer.ico
#endif
OutputDir=Output
OutputBaseFilename=TrayMinimizer_Setup_{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=auto

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
#ifdef HasKorean
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
#endif

[CustomMessages]
english.StartMenuIcon=Add to the &Start menu
english.DeleteDataOption=Also delete the settings data created by {#AppName}
english.StartUninstall=Uninstall
english.CancelButton=Cancel
korean.CancelButton=취소
english.UninstallOptionsTitle=Uninstall options
english.UninstallOptionsDesc=Choose what to remove, then click Uninstall.
korean.UninstallOptionsTitle=제거 옵션
korean.UninstallOptionsDesc=삭제할 항목을 선택한 뒤 '제거'를 누르세요.
english.AppRunning={#AppName} is currently running.%nQuit it from its tray icon (right-click > Exit) and run the uninstaller again.
korean.AppRunning={#AppName}이(가) 실행 중입니다.%n트레이 아이콘 우클릭 > 종료로 앱을 끝낸 뒤 제거를 다시 실행해 주세요.
english.AppRunningSetup={#AppName} is currently running.%nQuit it from its tray icon (right-click > Exit) and run the installer again.
korean.AppRunningSetup={#AppName}이(가) 실행 중입니다.%n트레이 아이콘 우클릭 > 종료로 앱을 끝낸 뒤 설치를 다시 실행해 주세요.
korean.StartMenuIcon=시작 메뉴에 앱 등록(&S)
korean.DeleteDataOption={#AppName}에서 생성한 설정 데이터도 함께 삭제
korean.StartUninstall=제거

; 3. 바탕 화면 아이콘 / 시작 메뉴 등록 체크박스
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"
Name: "startmenuicon"; Description: "{cm:StartMenuIcon}"

[Files]
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

; {autodesktop}/{autoprograms} 는 설치 모드에 따라 모든 사용자용/현재 사용자용 위치로 바뀐다.
[Icons]
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: startmenuicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent

[Code]
{ 언인스톨러 창에 "설정 데이터도 삭제" 체크박스를 두고, 제거 완료 후 선택에 따라 데이터를 삭제한다.
  무인(silent) 제거에서는 창이 없으므로 데이터를 삭제하지 않는다. }
{ 언인스톨러 스크립트에는 Application.ProcessMessages 가 없으므로 Win32 API 로 메시지를 직접 처리한다.
  MSG 구조체의 내용은 읽지 않으므로 32/64비트 어느 쪽 크기보다 큰 불투명 버퍼로 선언한다. }
type
  TMessageBuffer = record
    Data: array[0..7] of Int64;
  end;

function PeekMessageW(var Msg: TMessageBuffer; Wnd: HWND;
  MsgFilterMin, MsgFilterMax, RemoveMsg: UINT): BOOL;
  external 'PeekMessageW@user32.dll stdcall uninstallonly';
function TranslateMessage(var Msg: TMessageBuffer): BOOL;
  external 'TranslateMessage@user32.dll stdcall uninstallonly';
function DispatchMessageW(var Msg: TMessageBuffer): LongInt;
  external 'DispatchMessageW@user32.dll stdcall uninstallonly';

const
  PM_REMOVE = 1;

{ 대기 중에도 창이 그려지고 버튼 클릭이 처리되도록 쌓인 메시지를 모두 처리한다. }
procedure PumpMessages();
var
  Msg: TMessageBuffer;
begin
  while PeekMessageW(Msg, 0, 0, 0, PM_REMOVE) do
  begin
    TranslateMessage(Msg);
    DispatchMessageW(Msg);
  end;
end;

var
  OptionsPage: TNewNotebookPage;       { 1페이지: 제거 옵션(체크박스) }
  ProgressPage: TNewNotebookPage;      { 2페이지: 기본 제거 진행 화면 }
  ProgressPageName: string;            { 진행 화면의 원래 제목/설명(전환 시 복원) }
  ProgressPageDesc: string;
  DeleteDataCheck: TNewCheckBox;
  StartButton: TNewButton;
  StartClicked: Boolean;
  CancelClicked: Boolean;
  DeleteData: Boolean;

function DataDirPath(): string;
begin
  Result := ExpandConstant('{userappdata}\{#DataDirName}');
end;

{ '제거'을 누르면 선택을 저장하고 제거 진행 페이지로 넘어간다. }
procedure StartButtonClick(Sender: TObject);
begin
  DeleteData := DeleteDataCheck.Checked;
  StartButton.Visible := False;
  { 제거가 시작되면 중간에 취소할 수 없으므로 취소 버튼도 숨긴다. }
  UninstallProgressForm.CancelButton.Visible := False;
  UninstallProgressForm.PageNameLabel.Caption := ProgressPageName;
  UninstallProgressForm.PageDescriptionLabel.Caption := ProgressPageDesc;
  UninstallProgressForm.InnerNotebook.ActivePage := ProgressPage;
  StartClicked := True;
end;

{ 옵션 페이지에서 '취소'를 누르면 대기를 끝내고 제거를 중단하도록 표시한다(중단은 CurUninstallStepChanged 에서). }
procedure OptionsCancelClick(Sender: TObject);
begin
  CancelClicked := True;
end;

{ 실행 파일 이름으로 프로세스를 찾는다(tasklist 결과에 이름이 있으면 find 가 0 을 반환). }
function IsAppRunning(): Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec(ExpandConstant('{cmd}'),
                 '/C tasklist /FI "IMAGENAME eq {#AppExeName}" /NH | find /I "{#AppExeName}" >nul',
                 '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
            and (ResultCode = 0);
end;

{ 앱이 실행 중이면 경고 후 인스톨러를 종료한다(False 반환 시 설치가 중단된다). }
function InitializeSetup(): Boolean;
begin
  Result := not IsAppRunning();
  if not Result then
    MsgBox(CustomMessage('AppRunningSetup'), mbError, MB_OK);
end;

{ 앱이 실행 중이면 경고 후 언인스톨러를 종료한다(False 반환 시 제거가 중단된다). }
function InitializeUninstall(): Boolean;
begin
  Result := not IsAppRunning();
  if not Result then
    MsgBox(CustomMessage('AppRunning'), mbError, MB_OK);
end;

{ 제거 창에 '제거 옵션' 페이지를 추가하고 먼저 보여준다. 기본 진행 화면은 2페이지로 그대로 둔다. }
procedure InitializeUninstallProgressForm();
begin
  if UninstallSilent or not DirExists(DataDirPath()) then
    Exit;

  { 기본 진행 페이지와 제목/설명을 기억해 둔다(페이지를 바꾸기 전에 읽어야 한다). }
  ProgressPage := UninstallProgressForm.InnerNotebook.ActivePage;
  ProgressPageName := UninstallProgressForm.PageNameLabel.Caption;
  ProgressPageDesc := UninstallProgressForm.PageDescriptionLabel.Caption;

  OptionsPage := TNewNotebookPage.Create(UninstallProgressForm);
  OptionsPage.Notebook := UninstallProgressForm.InnerNotebook;
  OptionsPage.Align := alClient;

  DeleteDataCheck := TNewCheckBox.Create(UninstallProgressForm);
  DeleteDataCheck.Parent := OptionsPage;
  DeleteDataCheck.Left := ScaleX(38);
  DeleteDataCheck.Top := ScaleY(8);
  DeleteDataCheck.Width := OptionsPage.Width;
  DeleteDataCheck.Caption := CustomMessage('DeleteDataOption');
  DeleteDataCheck.Checked := False;

  { 기본 취소 버튼을 보이게 하고, 그 왼쪽에 '제거' 버튼을 둔다. }
  UninstallProgressForm.CancelButton.Caption := CustomMessage('CancelButton');
  UninstallProgressForm.CancelButton.Enabled := True;
  UninstallProgressForm.CancelButton.Visible := True;
  UninstallProgressForm.CancelButton.OnClick := @OptionsCancelClick;

  StartButton := TNewButton.Create(UninstallProgressForm);
  StartButton.Parent := UninstallProgressForm;
  StartButton.Left := UninstallProgressForm.CancelButton.Left -
    UninstallProgressForm.CancelButton.Width - ScaleX(8);
  StartButton.Top := UninstallProgressForm.CancelButton.Top;
  StartButton.Width := UninstallProgressForm.CancelButton.Width;
  StartButton.Height := UninstallProgressForm.CancelButton.Height;
  StartButton.Caption := CustomMessage('StartUninstall');
  StartButton.Default := True;
  StartButton.OnClick := @StartButtonClick;

  UninstallProgressForm.PageNameLabel.Caption := CustomMessage('UninstallOptionsTitle');
  UninstallProgressForm.PageDescriptionLabel.Caption := CustomMessage('UninstallOptionsDesc');
  UninstallProgressForm.InnerNotebook.ActivePage := OptionsPage;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usUninstall:
      { 사용자가 체크박스를 선택하고 '제거'나 '취소'를 누를 때까지 실제 제거를 보류한다. }
      if Assigned(StartButton) then
      begin
        while not (StartClicked or CancelClicked) do
        begin
          PumpMessages();
          Sleep(20);
        end;
        { 아직 아무것도 삭제하지 않은 시점이므로 조용히 중단한다. }
        if CancelClicked then
          Abort;
      end;
    usPostUninstall:
      if DeleteData and DirExists(DataDirPath()) then
        DelTree(DataDirPath(), True, True, True);
  end;
end;
