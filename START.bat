@echo on 
java -jar form_extraction/onetime_auto_browsing.jar
del "Data\oldForm.xls"
rename "Data\newForm.xls" oldForm.xls
copy "C:\Users\Aaron yoga\Downloads\数据列表.xls" "Data/"
del "C:\Users\Aaron yoga\Downloads\数据列表.xls"
rename "Data\数据列表.xls" newForm.xls
python matchAndSend.py
pause