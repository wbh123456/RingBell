import BellRingMatch as m
import gmailAuto as g

#---------------------------------------------extract bell ringers and listeners------------------------------------------------------------
# bellRingers = m.read_xls('Data/newForm.xls')
bellRingers = m.read_new_ringer('Data/newForm.xls', 'Data/oldForm.xls')
listeners = m.read_xls("Data/Listeners.xls")
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
    title = 'Your matching result from Bell Ringer'

    br_email = bell_ringer.email
    l_email = listener.email
    #generate email contents
    br_content, l_content = g.generate_email_content(bell_ringer, listener,time)

    #Send Emails
    print("-->Sending email to Bell Ringer: " + bell_ringer.name + " at " + br_email + " ... ")
    g.sendGmail(br_content, br_email, title)

    print("-->Sending email to Listener: " + listener.name + " at " + l_email + " ... ")
    if l_content != -1:
        g.sendGmail(l_content, l_email, title)
    else:
        print("Does not need to send email to Listener")


