@echo off
setlocal
if "%KSC_SERVER%"=="" set /p KSC_SERVER=Servidor KSC (ex.: https://ksc.exemplo.com:13299): 
if "%KSC_USER%"=="" set /p KSC_USER=Usuario KSC: 
if "%KSC_TASK%"=="" set /p KSC_TASK=Nome da tarefa: 
py enumerating_tasks_querying_task_running_task.py -server "%KSC_SERVER%" -user "%KSC_USER%" -ksc_user -task "%KSC_TASK%" %*
pause
