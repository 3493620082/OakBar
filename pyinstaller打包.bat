@echo off
chcp 65001 >nul
echo 开始打包...
pyinstaller -F -i OakBar.ico main.py --exclude-module all --hidden-import pygame-ce --hidden-import colorama
xcopy /E /I /Y "media" "dist\media"
xcopy /E /I /Y "save" "dist\save"
xcopy /E /I /Y "src" "dist\src"
echo 打包完成！可执行文件在dist目录中
pause