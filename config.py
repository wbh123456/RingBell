import sys

def config(arg):
    global DISABLE_EMAIL_SENDING
    global GET_TEST_FORMS
    global DISABLE_FREEZING
    global INTERNAL_TESTING

    length = len(arg) - 1
    if (length >= 1):
        if arg[1] == "--release_mode":
            print("Running in release mode!")
            DISABLE_EMAIL_SENDING = False
            GET_TEST_FORMS = False
            DISABLE_FREEZING = False
            INTERNAL_TESTING = False
            return
        elif arg[1] == "--internal_testing_mode":
            print("Running in internal testing mode!")
            print("Files will be extracted from testing files!")
            DISABLE_EMAIL_SENDING = True
            GET_TEST_FORMS = False
            DISABLE_FREEZING = False
            INTERNAL_TESTING = True
            return
        elif arg[1] == "--disable_email_sending":
            print("Running with email sending disabled!")
            DISABLE_EMAIL_SENDING = True
            GET_TEST_FORMS = False
            DISABLE_FREEZING = False
            INTERNAL_TESTING = False
            return
        elif arg[1] == "--disable_freezing":
            print("Running with freezing disabled!")
            DISABLE_EMAIL_SENDING = False
            GET_TEST_FORMS = False
            DISABLE_FREEZING = True
            INTERNAL_TESTING = False
            return
        elif arg[1] == "--test_examples":
            print("Running in test_examples mode!")
            DISABLE_EMAIL_SENDING = True
            GET_TEST_FORMS = True
            DISABLE_FREEZING = False
            INTERNAL_TESTING = False
            return
        elif arg[1] == "--test_examples_with_email":
            print("Running in test_examples mode with sending email enabled!")
            DISABLE_EMAIL_SENDING = False
            GET_TEST_FORMS = True
            DISABLE_FREEZING = False
            INTERNAL_TESTING = False
            return

    print("No arguments, disable email, freezing and get forms from examples!")
    DISABLE_EMAIL_SENDING = True
    GET_TEST_FORMS = True
    DISABLE_FREEZING = True
    INTERNAL_TESTING = False
    return


if __name__ == "__main__":
    config(sys.argv)