@echo off
chcp 65001 >nul
echo 开始打包...
pyinstaller -F -i OakBar.ico main.py --exclude-module all --hidden-import pygame-ce --hidden-import colorama
echo 正在复制资源文件夹到 dist 目录...
xcopy /E /I /Y "media" "dist\media"
xcopy /E /I /Y "save" "dist\save"
xcopy /E /I /Y "src" "dist\src"
echo 正在清理冗余文件...
:: 删除 build 文件夹（/S 删除子目录，/Q 静默删除不提示）
rd /S /Q "build"
:: 删除 main.spec 文件（/F 强制删除，/Q 静默删除）
del /F /Q "main.spec"
echo 打包完成！可执行文件在dist目录中
pause