@echo off
setlocal
if "%KSC_SERVER%"=="" set /p KSC_SERVER=Servidor KSC (ex.: https://ksc.exemplo.com:13299): 
if "%KSC_USER%"=="" set /p KSC_USER=Usuario KSC: 
if "%KSC_NEW_USER%"=="" set /p KSC_NEW_USER=Novo usuario interno: 
py add_internal_user.py -server "%KSC_SERVER%" -user "%KSC_USER%" -ksc_user -new_user "%KSC_NEW_USER%" %*
pause
