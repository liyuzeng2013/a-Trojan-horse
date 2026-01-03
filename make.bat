@echo off
color 0a
pyinstaller -F c.py
pyinstaller -F k.py
pyinstaller -F s.py
color 06
del /s /q build
del /q c.spec
del /q s.spec
del /q k.spec
color
pause