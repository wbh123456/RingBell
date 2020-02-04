@echo off 
chcp 65001
cd %~dp0

python form_extraction.py
del "Data\oldForm.xls"
rename "Data\newForm.xls" oldForm.xls
rename "Data\数据列表.xls" newForm.xls
python  matchAndSend.py
pause