pyinstaller -F form_extraction.py
move ".\dist\form_extraction.exe" ".\form_extraction.exe"
rmdir /S/Q dist
rmdir /S/Q build
del form_extraction.spec

pyinstaller -F matchAndSend.py
move ".\dist\matchAndSend.exe" ".\matchAndSend.exe"
rmdir /S/Q dist
rmdir /S/Q build
del matchAndSend.spec

pause