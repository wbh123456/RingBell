import BellRingMatch as m
import gmailAuto as g
import config
import os
import environment
import pymongo

developer_list = {"Aaron":"aaronwang0407@gmail.com", "Danny":"dannyding123456@gmail.com", "Jaya":"jessicahu819@hotmail.com",
    "Tina": "yuto.dong@mail.utoronto.ca", "Junlin": "104431605@qq.com", "Livia": "kittylivia.li@mail.utoronto.ca", "William": "wm798222@gmail.com"}

def matchAndSend():
    #Get "relative path"
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    if config.INTERNAL_TESTING:
        print("Getting forms from internal_testing_data/!")
        rel_path_newForm = "internal_testing_data/newForm.xls"
        rel_path_oldForm = "internal_testing_data/oldForm.xls"
        rel_path_listeners = "internal_testing_data/Listeners.xls"

    elif config.MATCHING_ALGORITHM_TESTING:
        print("Getting forms from matching_algorithm_testing/!")
        rel_path_newForm = "matching_algorithm_testing_data/newForm.xls"
        rel_path_oldForm = "matching_algorithm_testing_data/oldForm.xls"
        rel_path_listeners = "matching_algorithm_testing_data/Listeners.xls"

    elif config.GET_EXAMPLE_FORMS:
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
    # Establish connection to database
    client = pymongo.MongoClient(environment.MONGO_URL)
    db = client.RingBellDB
    if config.MATCHING_ALGORITHM_TESTING:
        listener_collection = db['algorithm_testing_listener_collection']
        bellringer_collection = db['algorithm_testing_bellringer_collection']
    elif config.INTERNAL_TESTING:
        listener_collection = db['internal_testing_listener_collection']
        bellringer_collection = db['internal_testing_bellringer_collection']
    elif config.GET_EXAMPLE_FORMS:
        listener_collection = db['example_listener_collection']
        bellringer_collection = db['example_bellringer_collection']
    else:
        listener_collection = db['release_listener_collection']
        bellringer_collection = db['release_bellringer_collection']

    if config.ADD_LISTENERS:
        m.add_listeners_to_database(abs_path_listeners, listener_collection)

    # Get Listeners and BellRingers
    if config.MATCHING_ALGORITHM_TESTING:
        bellRingers = m.get_bellringer_from_database(bellringer_collection)
    else:
        bellRingers = m.get_new_bellringer(abs_path_newForm, bellringer_collection)
        # Update bell ringers to database
        if not config.DISABLE_ADD_NEW_BELLRINGER:
            m.add_bellringers_to_database(bellRingers, bellringer_collection)

    listeners = m.get_listeners_from_database(listener_collection)


    print("-->Bell Ringers: ")
    for i in bellRingers:
        i.print_person()
    print("-->Listeners:")
    for i in listeners:
        i.print_person()

    #------------------------------------------------match bell rings and listeners---------------------------------------------------------------
    matching_result_list = m.match_all(listeners, bellRingers, listener_collection)

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
        br_content, l_content, d_content, title = g.generate_email_content(bell_ringer, listener, date_and_time, config.INTERNAL_TESTING)

        #Send Emails
        if not config.DISABLE_EMAIL_SENDING:
            # To Bell Ringer first (This has the highest probability to fail)
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
