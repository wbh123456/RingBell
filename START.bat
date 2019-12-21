@echo on 
chcp 65001
form_extraction.exe
del "Data\oldForm.xls"
rename "Data\newForm.xls" oldForm.xls
rename "Data\数据列表.xls" newForm.xls
matchAndSend.exe