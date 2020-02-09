import sys

def config(arg):
    global DISABLE_EMAIL_SENDING
    global GET_TEST_FORMS
    global DISABLE_FREEZING

    length = len(arg) - 1
    if (length >= 1):
        if arg[1] == "--release_mode":
            print("Running in release mode!")
            DISABLE_EMAIL_SENDING = False
            GET_TEST_FORMS = False
            DISABLE_FREEZING = False
            return
        elif arg[1] == "--disable_email_sending":
            print("Running with email sending disabled!")
            DISABLE_EMAIL_SENDING = True
            GET_TEST_FORMS = False
            DISABLE_FREEZING = False
            return
        elif arg[1] == "--disable_freezing":
            print("Running with freezing disabled!")
            DISABLE_EMAIL_SENDING = False
            GET_TEST_FORMS = False
            DISABLE_FREEZING = True
            return
        elif arg[1] == "--test_examples":
            print("Running in test_examples mode!")
            DISABLE_EMAIL_SENDING = True
            GET_TEST_FORMS = True
            DISABLE_FREEZING = False
            return
        elif arg[1] == "--test_examples_with_email":
            print("Running in test_examples mode with sending email enabled!")
            DISABLE_EMAIL_SENDING = False
            GET_TEST_FORMS = True
            DISABLE_FREEZING = False
            return

    print("No arguments, running with all set to True!")
    DISABLE_EMAIL_SENDING = True
    GET_TEST_FORMS = True
    DISABLE_FREEZING = True
    return


if __name__ == "__main__":
    config(sys.argv)