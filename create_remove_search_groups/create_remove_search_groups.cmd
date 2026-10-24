@echo off
setlocal
if "%KSC_SERVER%"=="" set /p KSC_SERVER=Servidor KSC (ex.: https://ksc.exemplo.com:13299): 
if "%KSC_USER%"=="" set /p KSC_USER=Usuario KSC: 
py create_remove_search_groups.py -server "%KSC_SERVER%" -user "%KSC_USER%" -ksc_user %*
pause
