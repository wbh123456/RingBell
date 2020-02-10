import BellRingMatch as m
import gmailAuto as g
import config
import os

developer_list = {"Aaron":"aaronwang0407@gmail.com", "Danny":"dannyding123456@gmail.com", "Jaya":"jessicahu819@hotmail.com"}

def matchAndSend():
    #Get "relative path"
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    if config.INTERNAL_TESTING:
        print("Getting forms from internal_testing_data/!")
        rel_path_newForm = "internal_testing_data/newForm.xls"
        rel_path_oldForm = "internal_testing_data/oldForm.xls"
        rel_path_listeners = "internal_testing_data/Listeners.xls"

    elif config.GET_TEST_FORMS:
        print("Getting test forms from examples!")
        rel_path_newForm = "example/newForm.xls"
        rel_path_oldForm = "example/oldForm.xls"
        rel_path_listeners = "example/Listeners.xls"

    else:
        rel_path_newForm = "Data/newForm.xls"
        rel_path_oldForm = "Data/oldForm.xls"
        rel_path_listeners = "Data/Listeners.xls"
    abs_path_newForm = os.path.join(script_dir, rel_path_newForm)
    abs_path_oldForm = os.path.join(script_dir, rel_path_oldForm)
    abs_path_listeners = os.path.join(script_dir, rel_path_listeners)

    #---------------------------------------------extract bell ringers and listeners------------------------------------------------------------
    # bellRingers = m.read_xls('Data/newForm.xls')
    bellRingers = m.read_new_ringer(abs_path_newForm, abs_path_oldForm)
    listeners = m.read_listener(abs_path_listeners)
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
        #matching_resilt format :  [bell_ringer, matched_listener, date, time]
        bell_ringer = matching_result[0]
        listener = matching_result[1]
        date = matching_result[2]
        time = matching_result[3]
        date_and_time = ""
        if date != -1:
            date_and_time = date + " " + time

        #generate email contents
        br_content, l_content, d_content, title = g.generate_email_content(bell_ringer, listener, date_and_time)

        #Send Emails
        if not config.DISABLE_EMAIL_SENDING:
            # To Bell Ringer
            print("-->Sending email to Bell Ringer: " + bell_ringer.name + " at " + bell_ringer.email + " ... ")
            g.sendGmail(br_content, bell_ringer.email, title)

            # To Listener
            if l_content != -1:
                print("-->Sending email to Listener: " + listener.name + " at " + listener.email + " ... ")
                g.sendGmail(l_content, listener.email, title)
            else:
                print("Does not need to send email to Listener")
            
            # To developers
            for item in developer_list.items():
                print("-->Sending result to Developer: " + item[0] + " at: " + item[1] + " ... ")
                g.sendGmail(d_content, item[1], title)

        else:
            print("Email sending not enabled!")

if __name__ == '__main__':
    config.config(["",""])
    matchAndSend()
