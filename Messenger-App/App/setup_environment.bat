ECHO OFF
ECHO #-#-#-# UOD MESSENGER APP #-#-#-#
ECHO SETTING UP PYTHON VIRTUAL ENVIRONMENT

SET PYTHON_EXECUTABLE=notfound
FOR %%P IN ("python") DO (
    %%~P --version
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_EXECUTABLE=%%~P
        ECHO Python command found: %%~P
        GOTO :start_req_installation
    )
)

IF %PYTHON_EXECUTABLE%=notfound (
    ECHO Python is not installed on this machine?
)


:start_req_installation

if NOT EXIST v\Scripts\activate.bat (
    %PYTHON_EXECUTABLE% -m venv v
    ECHO INSTALLING REQUIREMENTS
    "v\Scripts\python" -m pip install --upgrade pip
    "v\Scripts\python" -m pip install -r requirements.txt

) ELSE (
    ECHO VIRTUAL ENVIRONMENT ALREADY PRESENT? MANUALLY INSTALL REQS OR DELETE AND RE-RUN THIS
)



