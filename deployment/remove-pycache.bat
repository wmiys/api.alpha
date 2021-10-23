:: ----------------------------------------------------------------------------------
:: Remove all the __pycache__ subdirectories out of the source code
:: ----------------------------------------------------------------------------------

:: CD to the src directory containing the application package
cd C:\xampp\htdocs\files\api.wmiys\src

:: Delete the files
FOR /d /r . %%d IN ("__pycache__") DO @IF EXIST "%%d" rd /s /q "%%d"

pause