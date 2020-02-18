import sys

def config(arg):
    global DISABLE_EMAIL_SENDING
    global GET_EXAMPLE_FORMS
    global DISABLE_FREEZING
    global INTERNAL_TESTING
    global DISABLE_EXTRACT

    # Default setting
    DISABLE_EMAIL_SENDING = True #Dangerous parameter, default to disabled
    GET_EXAMPLE_FORMS = False
    DISABLE_FREEZING = False
    DISABLE_EXTRACT = False

    INTERNAL_TESTING = False

    length = len(arg)
    for position in range(1,length):
        # Set modes
        if arg[position] == "--release_mode":
            print("Running in release mode!")
            DISABLE_EMAIL_SENDING = False
            GET_EXAMPLE_FORMS = False
            DISABLE_FREEZING = False
            INTERNAL_TESTING = False
            DISABLE_EXTRACT = False
            return
        elif arg[position] == "--internal_testing_mode":
            print("Running in internal testing mode!")
            print("Files will be extracted from testing files!")
            DISABLE_EMAIL_SENDING = True
            GET_EXAMPLE_FORMS = False
            DISABLE_FREEZING = False
            INTERNAL_TESTING = True
            DISABLE_EXTRACT = False
            return
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

        # If not on the list
        else:
            raise ValueError('Invalid command line option', arg[position])
    return


if __name__ == "__main__":
    config(sys.argv)