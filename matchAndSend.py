import BellRingMatch as m
import gmailAuto as g
import os

#Get "ralative path"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path_newForm = "Data/newForm.xls"
rel_path_oldForm = "Data/oldForm.xls"
rel_path_listeners = "Data/Listeners.xls"
# rel_path_newForm = "Example/newForm.xls"
# rel_path_oldForm = "Example/oldForm.xls"
abs_path_newForm = os.path.join(script_dir, rel_path_newForm)
abs_path_oldForm = os.path.join(script_dir, rel_path_oldForm)
abs_path_listeners = os.path.join(script_dir, rel_path_listeners)

#---------------------------------------------extract bell ringers and listeners------------------------------------------------------------
# bellRingers = m.read_xls('Data/newForm.xls')
bellRingers = m.read_new_ringer(abs_path_newForm, abs_path_oldForm)
listeners = m.read_xls(abs_path_listeners)
print("-->new bell ringers: ")
for i in bellRingers:
    i.print_person()
print("-->Listeners:")
for i in listeners:
    i.print_person()

#------------------------------------------------match bell rings and listeners---------------------------------------------------------------
matching_result_list = m.match_all(listeners, bellRingers)

#----------------------------------------------------------send gmail-------------------------------------------------------------------------

for matching_result in matching_result_list:
    #matching_resilt format :  [bell_ringer, matched_listener, time]
    bell_ringer = matching_result[0]
    listener = matching_result[1]
    time = matching_result[2]

    #generate email contents
    br_content, l_content, title = g.generate_email_content(bell_ringer, listener,time)

    #Send Emails
    print("-->Sending email to Bell Ringer: " + bell_ringer.name + " at " + bell_ringer.email + " ... ")
    g.sendGmail(br_content, bell_ringer.email, title)

    if l_content != -1:
        print("-->Sending email to Listener: " + listener.name + " at " + listener.email + " ... ")
        g.sendGmail(l_content, listener.email, title)
    else:
        print("Does not need to send email to Listener")


