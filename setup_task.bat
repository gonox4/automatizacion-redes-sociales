@echo off
schtasks /create /tn "SocialMediaBot" /tr "c:\Users\Usuario\.gemini\antigravity\scratch\automatizacion-redes-sociales\run_bot.bat" /sc daily /st 10:00 /f
if %errorlevel% eq 0 (
    echo Tarea 'SocialMediaBot' programada exitosamente para las 10:00 AM diariamente.
) else (
    echo Hubo un error al programar la tarea.
)
pause
