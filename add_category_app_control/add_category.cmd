@echo off
setlocal
if "%KSC_SERVER%"=="" set /p KSC_SERVER=Servidor KSC (ex.: https://ksc.exemplo.com:13299): 
if "%KSC_USER%"=="" set /p KSC_USER=Usuario KSC: 
if "%KSC_CATEGORY%"=="" set "KSC_CATEGORY=IoC"
py add_category.py -server "%KSC_SERVER%" -user "%KSC_USER%" -ksc_user -category "%KSC_CATEGORY%" -file sha256.txt %*
pause
