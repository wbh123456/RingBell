import sys

def config(arg):
    global DISABLE_EMAIL_SENDING
    global GET_EXAMPLE_FORMS
    global DISABLE_FREEZING
    global MATCHING_ALGORITHM_TESTING
    global DISABLE_EXTRACT
    global ADD_LISTENERS
    global DISABLE_ADD_NEW_BELLRINGER
    global INTERNAL_TESTING

    # Default setting
    DISABLE_EMAIL_SENDING = True #Dangerous parameter, default to disabled
    GET_EXAMPLE_FORMS = False
    DISABLE_FREEZING = False
    DISABLE_EXTRACT = False
    ADD_LISTENERS = False
    DISABLE_ADD_NEW_BELLRINGER = False

    MATCHING_ALGORITHM_TESTING = False
    INTERNAL_TESTING = False

    length = len(arg)
    for position in range(1,length):
        # Set modes
        if arg[position] == "--release_mode":
            print("Running in release mode!")
            DISABLE_EMAIL_SENDING = False
            return
        elif arg[position] == "--matching_algorithm_testing_mode":
            print("Running in matching algorithm testing mode!")
            DISABLE_FREEZING = True
            MATCHING_ALGORITHM_TESTING = True
            DISABLE_EXTRACT = True
            DISABLE_ADD_NEW_BELLRINGER = True

        elif arg[position] == "--internal_testing_mode":
            print("Running in internal testing mode")
            INTERNAL_TESTING = True
            
        # Set parameters
        elif arg[position] == "--disable_email_sending":
            print("Disable email")
            DISABLE_EMAIL_SENDING = True
        elif arg[position] == "--enable_email_sending":
            print("ENABLE EMAIL SENDING!!!")
            DISABLE_EMAIL_SENDING = False
        elif arg[position] == "--disable_freezing":
            print("Disable freezing")
            DISABLE_FREEZING = True
        elif arg[position] == "--use_example":
            print("Use example")
            GET_EXAMPLE_FORMS = True
            DISABLE_EXTRACT = True
        elif arg[position] == "--disable_extract":
            print("Disable form extraction ")
            DISABLE_EXTRACT = True
        elif arg[position] == "--add_listeners":
            print("Adding listeners")
            ADD_LISTENERS = True
            DISABLE_EXTRACT = True
        elif arg[position] == "--run_atomically":
            print("Running atomically")
            DISABLE_FREEZING = True
            DISABLE_ADD_NEW_BELLRINGER = True

        # If not on the list
        else:
            raise ValueError('Invalid command line option', arg[position])
    return


if __name__ == "__main__":
    config(sys.argv)