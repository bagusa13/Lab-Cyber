@echo off
title Inject Amlogic Bootloader ke MicroSD
color 0A

:: Check for Administrator privileges and self-elevate
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Meminta hak Administrator...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

echo ========================================================
echo    INJEKSI BOOTLOADER AMLOGIC S905X KE SECTOR 1 MICROSD
echo ========================================================
echo.

py "C:\Users\bagus\.gemini\antigravity\brain\b5fdc016-0425-43b7-867c-2d2aa1bb3075\scratch\burn_bootloader.py"

echo.
echo ========================================================
echo Selesai. Tekan sembarang tombol untuk menutup jendela ini.
pause >nul
