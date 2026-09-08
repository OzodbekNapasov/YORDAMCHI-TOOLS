@echo off
chcp 65001 >nul
title ATLAS - YouTube kunlik yuklash
cd /d "%~dp0"
python youtube_batch_upload.py --limit 6 --privacy public
